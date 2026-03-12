from sheets import SheetManager
from traffic import TrafficLight


class _TrafficProxy:
    def __init__(self, light, sheets_mgr):
        self._light = light
        self._sheets = sheets_mgr

    @property
    def connected(self):
        return self._light.ser is not None

    def set_red(self):
        self._light.set_red()
        self._sheets.set_traffic_light("red")

    def set_green(self):
        self._light.set_green()
        self._sheets.set_traffic_light("green")

    def set_yellow(self):
        self._light.set_yellow()
        self._sheets.set_traffic_light("yellow")

    def set_off(self):
        self._light.set_off()
        self._sheets.set_traffic_light("off")


def init(traffic_usb_id=None):
    global rfid, sheets, app, traffic_light
    sheets = SheetManager()
    traffic_light = _TrafficProxy(TrafficLight(traffic_usb_id), sheets)


def setRFID(new_rfid):
    global rfid
    rfid = new_rfid


def setApp(new_app):
    global app
    app = new_app
