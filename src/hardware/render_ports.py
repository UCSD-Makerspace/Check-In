from dataclasses import dataclass

import serial.tools.list_ports

SHARED_VID = 0x1A86
TRAFFIC_LOCATION = "1-1.1.2"


@dataclass
class UsbIds:
    reader: str | None
    traffic_light: str | None


def get_usb_ids() -> UsbIds:
    reader = None
    traffic_light = None
    for p in serial.tools.list_ports.comports():
        if p.vid == SHARED_VID:
            if p.location == TRAFFIC_LOCATION:
                traffic_light = p.device
            else:
                reader = p.device
    return UsbIds(reader, traffic_light)
