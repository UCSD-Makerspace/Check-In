import threading

from controllers.api_controller import ApiController
from hardware.traffic_light import TrafficLight


class TrafficLightController:
    def __init__(self, light: TrafficLight):
        self._light = light

    @property
    def connected(self) -> bool:
        return self._light.connected

    def drive(self, color: str) -> None:
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
            target=ApiController.set_traffic_light,
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
