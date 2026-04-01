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
        """Read one barcode from the scanner. Returns stripped string or None."""
        # Use read_until(\r) to handle scanners that terminate with CR only
        line = self._ser.read_until(b"\r")
        if not line:
            return None
        barcode = line.decode("ascii", errors="ignore").strip()
        # Strip Codabar start/stop characters (A, B, C, D) from both ends
        barcode = barcode.strip("ABCDabcd")
        return barcode if barcode else None

    def is_valid(self, barcode):
        if not barcode:
            return False
        if len(barcode) > 32:
            return False
        return True
