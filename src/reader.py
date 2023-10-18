from threading import Thread
from os.path import exists
from datetime import datetime
import serial
import time
import requests

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
        print("reader __init__ finished")

    def loadScanner(self):
        file_exists = exists("/dev/ttyUSB0")
        if file_exists:
            self.tty = "/dev/ttyUSB0"
        else:
            print("Scanner not connected")
            quit()

    def getSerInWaiting(self):
        return self.ser.in_waiting

    def readSerial(self):
        self.ser.read(self.ser.in_waiting)

    def grabRFID(self):
        print("RFID data incoming. Bytes in waiting: " + str(self.ser.in_waiting))
        tagBytes = self.ser.read(14)
        self.ser.read(self.ser.in_waiting)
        RFID = tagBytes.decode().replace("\r\n", "")
        print("Parsed tag: " + RFID)
        return str(RFID)

    def checkRFID(self, tag):
        # Varifies rfid tag

        if self.ser.in_waiting >= expected_characters:
            second_tag = self.grabRFID()
            print(f"Comparing {tag} and {second_tag}")
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
