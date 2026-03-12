import serial.tools.list_ports

SHARED_VID = 0x1A86
TRAFFIC_LOCATION = "1-1.1.2"


def get_usb_ids():
    reader_usb_id = None
    traffic_usb_id = None
    for p in serial.tools.list_ports.comports():
        if p.vid == SHARED_VID:
            if p.location == TRAFFIC_LOCATION:
                traffic_usb_id = p.device
            else:
                reader_usb_id = p.device
    return reader_usb_id, traffic_usb_id
