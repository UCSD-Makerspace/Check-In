import threading

from api.sheets import SheetManager
from hardware.traffic import TrafficLight


class TrafficLightApi:
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
