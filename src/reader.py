from threading import Thread
from os.path import exists
import logging
import serial
import time

expected_characters = 14
timeout = 1

##################################################################
# This class helps read information from RFID using serial ports #
##################################################################


class Reader(Thread):
    def __init__(self):
        super().__init__()
        self.tty = ""
        self.loadScanner()
        self.ser = serial.Serial(self.tty, 115200)
        logging.info("Card reader init finished")

    def loadScanner(self):
        if exists("/dev/ttyUSB0"):
            self.tty = "/dev/ttyUSB0"
        elif exists("/dev/ttyUSB1"):
            self.tty = "/dev/ttyUSB1"
        else:
            logging.warning("Scanner not connected")
            quit()

    def getSerInWaiting(self):
        return self.ser.in_waiting

    def readSerial(self):
        self.ser.read(self.ser.in_waiting)

    def grabRFID(self):
        logging.debug(
            "RFID data incoming. Bytes in waiting: " + str(self.ser.in_waiting)
        )
        tagBytes = self.ser.read(14)
        self.ser.read(self.ser.in_waiting)
        RFID = tagBytes.decode(encoding="latin-1").replace("\r\n", "")
        logging.info("Parsed tag: " + RFID)
        return str(RFID)

    def checkRFID(self, tag):
        # Verifies rfid tag

        if self.ser.in_waiting >= expected_characters:
            second_tag = self.grabRFID()
            logging.debug(f"Comparing {tag} and {second_tag}")
            if tag != second_tag:
                reason = "The two scanned tags did not match"
        elif len(tag) != expected_characters:
            reason = "Tag was not the expected number of chars"
        else:
            reason = "good"

        return reason

    def canScanAgain(self, lastTime):
        return time.time() - lastTime > 3

    def getRFID(self):
        return self.tag
