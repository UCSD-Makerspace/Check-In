import logging
from dataclasses import dataclass

import serial.tools.list_ports

READER_AND_TRAFFIC_LIGHT_VID = 0x1A86
TRAFFIC_LIGHT_LOCATION = "1-1.1.2"
BARCODE_VID = 0x9901


@dataclass
class UsbIds:
    reader: str | None
    traffic_light: str | None
    barcode: str | None


def get_usb_ids() -> UsbIds:
    reader = None
    traffic_light = None
    barcode = None
    for p in serial.tools.list_ports.comports():
        logging.debug("USB port: %s vid=%s desc=%s", p.device, hex(p.vid) if p.vid else None, p.description)
        if p.vid == READER_AND_TRAFFIC_LIGHT_VID:
            if p.location == TRAFFIC_LIGHT_LOCATION:
                traffic_light = p.device
            else:
                reader = p.device
        elif p.vid == BARCODE_VID:
            barcode = p.device
    logging.info("USB detected — reader: %s, traffic_light: %s, barcode: %s", reader, traffic_light, barcode)
    return UsbIds(reader, traffic_light, barcode)
