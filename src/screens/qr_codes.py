from pathlib import Path
from tkinter import Button
from .screen import Screen

ASSETS_PATH = Path(__file__).parent.parent / "assets" / "qr_codes_assets"


class QRCodes(Screen):
    def _build(self, controller):
        img3 = self._photo(ASSETS_PATH / "image_3.png")
        self._image(88.0, 90.0, image=img3)

        img4 = self._photo(ASSETS_PATH / "image_4.png")
        self._image(421.0, 360.0, image=img4)

        img5 = self._photo(ASSETS_PATH / "image_5.png")
        self._image(859.0, 360.0, image=img5)

        self._text(
            335.0, 551.0, anchor="nw",
            text="Website", fill="#F5F0E6", font=("Montserrat", 40 * -1),
        )
        self._text(
            788.0, 557.0, anchor="nw",
            text="Waiver", fill="#F5F0E6", font=("Montserrat", 40 * -1),
        )

        btn_img = self._photo(ASSETS_PATH / "image_6.png")
        btn = Button(
            self.canvas, image=btn_img, bg="#153246",
            command=lambda: controller.back_to_main(),
            relief="flat",
        )
        self._window(53.0, 55.0, btn)
