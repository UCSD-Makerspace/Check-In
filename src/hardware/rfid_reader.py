from threading import Thread
from os.path import exists
import logging
import serial
import sys
import time

from adafruit_pn532.uart import PN532_UART

expected_characters = 14


class Reader(Thread):
    def __init__(self, usb_id):
        super().__init__()
        self._usb_id = usb_id
        self._pn532 = None
        self._pending_tag = None
        if not usb_id or not exists(usb_id):
            logging.error("Card reader not found at %s, exiting", usb_id)
            sys.exit(1)
        for attempt in range(1, 6):
            try:
                self._init_pn532()
                logging.info("Card reader init finished")
                break
            except Exception as e:
                logging.warning("Card reader init attempt %d/5 failed: %s", attempt, e)
                if attempt == 5:
                    logging.error("Card reader failed to initialize after 5 attempts, exiting")
                    sys.exit(1)
                time.sleep(attempt * 0.5)

    def _init_pn532(self):
        if self._pn532 is not None:
            try:
                self._pn532._uart.close()
            except Exception as e:
                logging.warning("Failed to close card reader serial port: %s", e)
            self._pn532 = None
        uart = serial.Serial(self._usb_id, baudrate=115200, timeout=0.1)
        try:
            uart.reset_input_buffer()
            uart.reset_output_buffer()
            time.sleep(0.1)
            self._pn532 = PN532_UART(uart, debug=False)
        except Exception:
            uart.close()
            raise

    def reconnect(self):
        if not exists(self._usb_id):
            return False
        try:
            self._init_pn532()
            return True
        except Exception as e:
            logging.warning("Card reader reconnect attempt failed: %s", e)
            self._pn532 = None
            return False

    def get_ser_in_waiting(self):
        try:
            uid = self._pn532.read_passive_target(timeout=0.1)
        except Exception as e:
            raise OSError(f"PN532 error: {e}")
        if uid:
            self._pending_tag = "".join(f"{b:02X}" for b in uid)
            time.sleep(0.01)
            self._pn532._uart.reset_input_buffer()
            return expected_characters
        self._pending_tag = None
        return 0

    def grab_rfid(self):
        tag = self._pending_tag
        self._pending_tag = None
        logging.info("Parsed tag: " + str(tag))
        return str(tag)

    def check_rfid(self, tag):
        if not tag or len(tag) != expected_characters:
            return "Tag was not the expected number of chars"
        return "good"

    def can_scan_again(self, last_time):
        return time.time() - last_time > 3
