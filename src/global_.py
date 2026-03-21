import threading
from sheets import SheetManager
from traffic import TrafficLight

rfid = ""
sheets = None
app = None
traffic_light = None


class _TrafficProxy:
    def __init__(self, light, sheets_mgr):
        self._light = light
        self._sheets = sheets_mgr

    @property
    def connected(self):
        return self._light.ser is not None

    def _post(self, color):
        threading.Thread(
            target=self._sheets.set_traffic_light,
            args=(color,),
            daemon=True,
        ).start()

    def set_red(self):
        self._post("red")

    def set_green(self):
        self._post("green")

    def set_yellow(self):
        self._post("yellow")

    def set_off(self):
        self._post("off")


def init(traffic_usb_id=None):
    global sheets, traffic_light
    sheets = SheetManager()
    traffic_light = _TrafficProxy(TrafficLight(traffic_usb_id), sheets)
