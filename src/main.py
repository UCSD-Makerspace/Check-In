import sys
import logging
import argparse
import os
from sys import stdout

from PyQt6.QtWidgets import QApplication

from window import CheckInWindow
from dispatcher import MainThreadDispatcher
from controllers.navigation_controller import NavigationController
from controllers.barcode_scanner_controller import BarcodeScannerController
from hardware.barcode_scanner import BarcodeScanner
from controllers.check_in_controller import CheckInController
from controllers.account_controller import AccountController
from controllers.rfid_reader_controller import RfidReaderController
from hardware.rfid_reader import Reader
from screens.create_account_manual import CreateAccountManual
from screens.create_account_no_pid import CreateAccountNoPid
from screens.create_account_review import CreateAccountReview
from screens.check_in_manual import CheckInManual
from hardware.usb_ports import get_usb_ids
from app_context import AppContext
from api.client import check_api_health


def clear_and_return(ctx: AppContext):
    ctx.nav.back_to_main()
    ctx.nav.get_frame(CreateAccountManual).clear_entries()
    ctx.nav.get_frame(CreateAccountNoPid).clear_entries()
    ctx.nav.get_frame(CreateAccountReview).clear_entries()
    ctx.nav.get_frame(CheckInManual).clear_entries()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Makerspace Check-in System",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase verbosity (print debug info)")
    parser.add_argument("-d", "--dev", action="store_true", help="Enable dev mode with on-screen navigation overlay")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, stream=stdout)
    else:
        logging.basicConfig(level=logging.INFO)

    dev_mode = args.dev or os.environ.get("DEV_MODE") == "1"

    # QApplication must be created before any QWidget or QObject subclass
    app = QApplication(sys.argv)

    # Restore default SIGINT so Ctrl+C terminates the process
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    usb = get_usb_ids()
    check_api_health()
    ctx = AppContext.create(usb.traffic_light)
    ctx.dispatcher = MainThreadDispatcher()

    window = CheckInWindow()
    nav = NavigationController(window, ctx, dev_mode=dev_mode)
    ctx.window = window
    ctx.nav = nav
    ctx.check_in = CheckInController(ctx)
    ctx.account = AccountController(ctx)
    ctx.traffic_light.request_off()

    window.set_escape_handler(lambda: clear_and_return(ctx))

    reader = Reader(usb.reader)
    card_reader = RfidReaderController(ctx)
    card_reader.start(reader)

    if usb.barcode:
        barcode_scanner = BarcodeScanner(usb.barcode)
        barcode_controller = BarcodeScannerController(ctx)
        barcode_controller.start(barcode_scanner)
    else:
        logging.warning("No barcode scanner found, barcode scanning disabled")

    logging.info("Made it to app start")
    window.start()
    sys.exit(0)
