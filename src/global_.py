from sheets import SheetManager
from traffic import TrafficLight

#############################################################
# Declare all globals, and try to connect the google sheets #
# Also places the sheets in accessible global arrays        #
#############################################################


def init():
    global rfid, sheets, app, traffic_light
    sheets = SheetManager()
    traffic_light = TrafficLight("/dev/tty.usbserial-10")


def setRFID(new_rfid):
    global rfid
    rfid = new_rfid


def setApp(new_app):
    global app
    app = new_app
