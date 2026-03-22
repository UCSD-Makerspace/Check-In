import threading

from api.client import ApiClient
from api.traffic_light_api import TrafficLightApi
from hardware.traffic_light import TrafficLight


class AppContext:
    def __init__(self, sheets: ApiClient, traffic_light: TrafficLightApi):
        self.sheets = sheets
        self.traffic_light = traffic_light
        self.window = None
        self.nav = None
        self.check_in = None
        self.account = None
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
        sheets = ApiClient()
        light = TrafficLight(traffic_usb_id)
        traffic = TrafficLightApi(light, sheets)
        return cls(sheets, traffic)
