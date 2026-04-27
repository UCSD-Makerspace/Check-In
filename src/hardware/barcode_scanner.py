import serial
import logging
from os.path import exists


class BarcodeScanner:
    def __init__(self, usb_id):
        self._usb_id = usb_id
        self._ser = None
        self._connect()

    def _connect(self):
        self._ser = serial.Serial(self._usb_id, baudrate=9600, timeout=0.1)
        self._ser.reset_input_buffer()
        logging.info("Barcode scanner connected at %s", self._usb_id)

    def reconnect(self):
        if not exists(self._usb_id):
            return False
        try:
            self._connect()
            return True
        except Exception:
            self._ser = None
            return False

    def read_barcode(self):
        line = self._ser.read_until(b"\r")
        if not line:
            return None
        barcode = line.decode("ascii", errors="ignore").strip()
        barcode = barcode.strip("ABCDabcd")  # TODO: not sure if there is a better way to handle this
        return barcode if barcode else None

    def is_valid(self, barcode):
        if not barcode:
            return False
        if len(barcode) > 32:
            return False
        return True
