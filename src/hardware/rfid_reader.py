from threading import Thread
from os.path import exists
import logging
import serial
import sys
import time

from adafruit_pn532.uart import PN532_UART

expected_characters = 14


class Reader(Thread):
    def __init__(self, usb_id="/dev/ttyUSB0"):
        super().__init__()
        self._usb_id = usb_id
        self._pn532 = None
        self._pending_tag = None
        if usb_id is None:
            logging.error("No card reader USB ID configured, exiting")
            sys.exit(1)
        if not exists(usb_id):
            logging.error("Card reader not found at %s, exiting", usb_id)
            sys.exit(1)
        self._init_pn532()
        logging.info("Card reader init finished")

    def _init_pn532(self):
        uart = serial.Serial(self._usb_id, baudrate=115200, timeout=0.1)
        self._pn532 = PN532_UART(uart, debug=False)
        self._pn532.SAM_configuration()

    def reconnect(self):
        if not exists(self._usb_id):
            return False
        try:
            self._init_pn532()
            return True
        except Exception:
            self._pn532 = None
            return False

    def get_ser_in_waiting(self):
        try:
            uid = self._pn532.read_passive_target(timeout=0.1)
        except Exception as e:
            raise OSError(f"PN532 error: {e}")
        if uid:
            self._pending_tag = "".join(f"{b:02X}" for b in uid)
            time.sleep(0.01) # let any remaining in-flight bytes arrive
            self._pn532._uart.reset_input_buffer() # and flush them
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

    def can_scan_again(self, lastTime):
        return time.time() - lastTime > 3
