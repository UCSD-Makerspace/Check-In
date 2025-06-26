import serial.tools.list_ports

TRAFFIC_LIGHT_VID = 6790
READER_VID = 4292

def get_usb_ids():
    reader_usb_id = None
    traffic_usb_id = None
    for p in serial.tools.list_ports.comports():
        if p.vid == READER_VID:
            reader_usb_id = p.device
        elif p.vid == TRAFFIC_LIGHT_VID:
            traffic_usb_id = p.device
    return reader_usb_id, traffic_usb_id