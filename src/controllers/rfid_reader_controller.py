import time
import socket
import logging
from threading import Thread

from PyQt6.QtCore import QTimer

from controllers.api_controller import ApiController
from views.create_account_manual import CreateAccountManual


class RfidReaderController:
    def __init__(self, ctx):
        self.ctx = ctx
        self._no_wifi_shown = False

    def start(self, reader):
        thread = Thread(target=self._run, args=(reader,))
        thread.start()
        if self.ctx.traffic_light.connected:
            poller = Thread(target=self._poll_traffic_light, daemon=True)
            poller.start()

    def _run(self, reader):
        logging.info("Now reading ID cards")
        last_tag = 0
        last_time = 0
        scanner_error = False
        while True:
            if scanner_error:
                time.sleep(1.0)
                if reader.reconnect():
                    logging.info("Card reader reconnected")
                    scanner_error = False
                continue

            try:
                in_waiting = reader.get_ser_in_waiting()
            except OSError as e:
                if not scanner_error:
                    logging.error("Card reader disconnected, disabling until reconnection: %s", e)
                    scanner_error = True
                continue

            if in_waiting >= 14:
                if not self._is_connected():
                    logging.info("ERROR wifi is not connected")
                    if not self._no_wifi_shown:
                        self._no_wifi_shown = True
                        self.ctx.dispatcher.call.emit(self._show_wifi_error)
                    continue

                self.ctx.dispatcher.call.emit(
                    lambda: self.ctx.nav.get_frame(CreateAccountManual).clear_entries()
                )
                tag = reader.grab_rfid()

                if " " in tag:
                    continue

                if tag == last_tag and not reader.can_scan_again(last_time):
                    logging.debug("Suppressing repeat scan")
                    continue

                s_reason = reader.check_rfid(tag)

                if s_reason != "good":
                    logging.debug(s_reason)
                    continue
                else:
                    logging.debug("RFID Check Succeeded")

                self.ctx.rfid = tag
                self.ctx.check_in.handle_by_uuid(tag)

                last_tag = tag
                last_time = time.time()

    def _poll_traffic_light(self):
        last_color = None
        while True:
            time.sleep(0.1)
            color = ApiController.get_traffic_light()
            if color != last_color:
                last_color = color
                self.ctx.traffic_light.drive(color)

    def _show_wifi_error(self):
        self.ctx.nav.show_status(
            "ERROR! Connection cannot be established, please let staff know."
        )
        QTimer.singleShot(4000, self._clear_wifi_error)

    def _clear_wifi_error(self):
        self.ctx.nav.hide_status()
        self._no_wifi_shown = False

    def _is_connected(self, host="8.8.8.8", port=53, timeout=3):
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except socket.error:
            return False
