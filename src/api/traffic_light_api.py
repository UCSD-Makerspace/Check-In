import threading

from api.sheets import SheetManager
from hardware.traffic_light import TrafficLight


class TrafficLightApi:
    def __init__(self, light: TrafficLight, sheets: SheetManager):
        self._light = light
        self._sheets = sheets

    @property
    def connected(self) -> bool:
        return self._light.connected

    def drive(self, color: str) -> None:
        """Directly set the physical traffic light without posting to the API."""
        if color == "red":
            self._light.set_red()
        elif color == "green":
            self._light.set_green()
        elif color == "yellow":
            self._light.set_yellow()
        else:
            self._light.set_off()

    def _post(self, color: str) -> None:
        threading.Thread(
            target=self._sheets.set_traffic_light,
            args=(color,),
            daemon=True,
        ).start()

    def request_red(self) -> None:
        self._post("red")

    def request_green(self) -> None:
        self._post("green")

    def request_yellow(self) -> None:
        self._post("yellow")

    def request_off(self) -> None:
        self._post("off")
