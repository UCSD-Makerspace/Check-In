import time
import socket
import logging
from tkinter import Label
from threading import Thread
from screens.manual_fill import ManualFill


class CardReaderController:
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
                time.sleep(0.1)
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
                        no_wifi = Label(
                            self.ctx.window.canvas,
                            text="ERROR! Connection cannot be established, please let staff know.",
                            bg="#153246", fg="white", font=("Arial", 25),
                        )
                        no_wifi.place(relx=0.5, rely=0.1, anchor="center")
                        no_wifi.after(4000, lambda: self._destroy_wifi_error(no_wifi))
                    continue

                self.ctx.nav.get_frame(ManualFill).clear_entries()
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
            color = self.ctx.sheets.get_traffic_light()
            if color != last_color:
                last_color = color
                self.ctx.traffic_light.drive(color)

    def _is_connected(self, host="8.8.8.8", port=53, timeout=3):
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except socket.error:
            return False

    def _destroy_wifi_error(self, label):
        label.destroy()
        self._no_wifi_shown = False
