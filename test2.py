from py122u import nfc, error
import logging
import time
from typing import List
# https://downloads.acs.com.hk/drivers/en/API-ACR122U-2.02.pdf

reader = nfc.Reader()

def convert_uid_to_hex(uid: List) -> str:
    hex_id = ""
    for block in uid:
        hex_id += f"{block:02x}".upper()
    return hex_id


while True:
    try:
        reader.connect()
        data = reader.get_uid()
        # reader.print_data(data)
        uid_hex = convert_uid_to_hex(data)
    except (error.NoCommunication, error.InstructionFailed) as e:
        logging.info("No NFC card detected!")
    time.sleep(0.5)
# reader.info()
