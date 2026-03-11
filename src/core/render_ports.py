import serial.tools.list_ports

TRAFFIC_LIGHT_VID = 123 # TODO: switched this to dummy vid as system needs rewrite since it overlaps reader vid
READER_VID = 6790

def get_usb_ids():
    reader_usb_id = None
    traffic_usb_id = None
    for p in serial.tools.list_ports.comports():
        if p.vid == READER_VID:
            reader_usb_id = p.device
        elif p.vid == TRAFFIC_LIGHT_VID:
            traffic_usb_id = p.device
    return reader_usb_id, traffic_usb_id