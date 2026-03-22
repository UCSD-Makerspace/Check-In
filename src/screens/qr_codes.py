from pathlib import Path
from tkinter import Button
from .base import Screen

ASSETS_PATH = Path(__file__).parent.parent / "assets" / "qr_codes"
SHARED_PATH = Path(__file__).parent.parent / "assets" / "shared"


class QRCodes(Screen):
    def _build(self, controller):
        logo = self._photo(SHARED_PATH / "button_generic.png")
        self._image(88.0, 90.0, image=logo)

        qr_website_img = self._photo(ASSETS_PATH / "qr_website.png")
        self._image(421.0, 360.0, image=qr_website_img)

        qr_waiver_img = self._photo(ASSETS_PATH / "qr_waiver.png")
        self._image(859.0, 360.0, image=qr_waiver_img)

        self._text(
            421.0, 571.0, anchor="center",
            text="Website", fill="#F5F0E6", font=("Montserrat", 40 * -1),
        )
        self._text(
            859.0, 571.0, anchor="center",
            text="Waiver", fill="#F5F0E6", font=("Montserrat", 40 * -1),
        )

        btn_img = self._photo(SHARED_PATH / "icon_home.png")
        btn = Button(
            self.canvas, image=btn_img, bg="#153246",
            command=lambda: controller.back_to_main(),
            relief="flat",
        )
        self._window(53.0, 55.0, btn)
