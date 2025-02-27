from py122u import error, nfc
from typing import List
import logging

class RFID122U:
    def __init__(self):
        self.reader = nfc.Reader()

    def convert_uid_to_hex(uid: List) -> str:
        hex_id = ""
        for block in uid:
            hex_id += f"{block:02x}".upper()
        return hex_id

    def getRFID(self):
        try:
            self.reader.connect()
            data = self.reader.get_uid()
            # reader.print_data(data)
            return RFID122U.convert_uid_to_hex(data)
        except (error.NoCommunication, error.InstructionFailed, error.NoReader) as e:
            if e == error.NoCommunication:
                logging.info("Card not detected.")
            elif e == error.InstructionFailed:
                logging.info("Card released too early!")
            elif e == error.NoCommunication:
                logging.warning("Card reader disconnected!")
            return " "
