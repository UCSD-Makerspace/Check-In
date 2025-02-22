from py122u import nfc, error
import logging
import time
from typing import List
# https://downloads.acs.com.hk/drivers/en/API-ACR122U-2.02.pdf

reader = nfc.Reader()

def convert_uid_to_hex(uid: List) -> str:
    

while True:
    try:
        reader.connect()
        reader.print_data(reader.get_uid())
    except error.NoCommunication:
        logging.info("No NFC card detected!")
    time.sleep(0.5)
# reader.info()
