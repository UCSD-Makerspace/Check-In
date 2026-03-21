import threading

from sheets import SheetManager
from traffic import TrafficLight


class _TrafficProxy:
    def __init__(self, light: TrafficLight, sheets: SheetManager):
        self._light = light
        self._sheets = sheets

    @property
    def connected(self) -> bool:
        return self._light.ser is not None

    def _post(self, color: str) -> None:
        threading.Thread(
            target=self._sheets.set_traffic_light,
            args=(color,),
            daemon=True,
        ).start()

    def set_red(self) -> None:
        self._post("red")

    def set_green(self) -> None:
        self._post("green")

    def set_yellow(self) -> None:
        self._post("yellow")

    def set_off(self) -> None:
        self._post("off")


class AppContext:
    def __init__(self, sheets: SheetManager, traffic_light: _TrafficProxy):
        self.sheets = sheets
        self.traffic_light = traffic_light
        self.window = None
        self.nav = None
        self._rfid_lock = threading.Lock()
        self._rfid: str = ""

    @property
    def rfid(self) -> str:
        with self._rfid_lock:
            return self._rfid

    @rfid.setter
    def rfid(self, value: str) -> None:
        with self._rfid_lock:
            self._rfid = value

    @classmethod
    def create(cls, traffic_usb_id=None) -> "AppContext":
        sheets = SheetManager()
        light = TrafficLight(traffic_usb_id)
        proxy = _TrafficProxy(light, sheets)
        return cls(sheets, proxy)
