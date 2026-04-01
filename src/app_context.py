import threading

from controllers.traffic_light_controller import TrafficLightController
from hardware.traffic_light import TrafficLight


class AppContext:
    def __init__(self, traffic_light: TrafficLightController):
        self.traffic_light = traffic_light
        self.window = None
        self.nav = None
        self.check_in = None
        self.account = None
        self.dispatcher = None
        self.has_barcode_scanner = False
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
        light = TrafficLight(traffic_usb_id)
        traffic = TrafficLightController(light)
        return cls(traffic)
