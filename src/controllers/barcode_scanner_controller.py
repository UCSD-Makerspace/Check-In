import logging
import time
from threading import Thread

from screens.check_in_manual import CheckInManual
from screens.create_account_barcode import CreateAccountBarcode
from screens.create_account_manual import CreateAccountManual


class BarcodeScannerController:
    def __init__(self, ctx):
        self.ctx = ctx

    def start(self, scanner):
        thread = Thread(target=self._run, args=(scanner,), daemon=True)
        thread.start()

    def _run(self, scanner):
        logging.info("Now reading barcodes")
        scanner_error = False
        try:
            while True:
                if scanner_error:
                    time.sleep(0.5)
                    if scanner.reconnect():
                        logging.info("Barcode scanner reconnected")
                        scanner_error = False
                    continue

                try:
                    barcode = scanner.read_barcode()
                except OSError as e:
                    logging.error("Barcode scanner disconnected: %s", e)
                    scanner_error = True
                    continue

                if barcode is None:
                    continue

                logging.debug("Raw barcode received: %r", barcode)

                if not scanner.is_valid(barcode):
                    logging.warning("Invalid barcode rejected: %r", barcode)
                    continue

                logging.info("Barcode scanned: %r", barcode)
                curr_frame = self.ctx.nav.get_curr_frame()

                if curr_frame == CheckInManual:
                    self.ctx.dispatcher.call.emit(
                        lambda b=barcode: self.ctx.check_in.handle_by_pid(b)
                    )
                elif curr_frame in (CreateAccountBarcode, CreateAccountManual):
                    self.ctx.dispatcher.call.emit(
                        lambda b=barcode: self.ctx.account.go_to_review_from_barcode(b)
                    )
                else:
                    logging.debug("Barcode scanned on unhandled screen: %s", curr_frame)
        except Exception as e:
            logging.exception("Barcode scanner thread crashed: %s", e)
