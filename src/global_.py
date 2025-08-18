from sheets import SheetManager
from frontend.traffic import TrafficLight

#############################################################
# Declare all globals, and try to connect the google sheets #
# Also places the sheets in accessible global arrays        #
#############################################################


def init(traffic_usb_id=None):
    global rfid, sheets, app, traffic_light
    sheets = SheetManager()
    traffic_light = TrafficLight(traffic_usb_id)


def setRFID(new_rfid):
    global rfid
    rfid = new_rfid


def setApp(new_app):
    global app
    app = new_app
