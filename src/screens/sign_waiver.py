from pathlib import Path
from tkinter import Button
from .base import Screen

ASSETS_PATH = Path(__file__).parent.parent / "assets" / "sign_waiver"
SHARED_PATH = Path(__file__).parent.parent / "assets" / "shared"


class SignWaiver(Screen):
    def _build(self, controller):
        outline1_img = self._photo(ASSETS_PATH / "outline_1.png")
        self._image(1042.0, 359.0, image=outline1_img)

        outline2_img = self._photo(ASSETS_PATH / "outline_2.png")
        self._image(408.0, 76.0, image=outline2_img)

        outline3_img = self._photo(ASSETS_PATH / "outline_3.png")
        self._image(408.0, 429.0, image=outline3_img)

        icon_checked = self._photo(SHARED_PATH / "icon_checked_box.png")
        self._image(395.0, 70.0, image=icon_checked)

        icon_unchecked = self._photo(SHARED_PATH / "icon_unchecked_box.png")
        self._image(750.0, 70.0, image=icon_unchecked)

        qr_waiver_img = self._photo(ASSETS_PATH / "qr_waiver.png")
        self._image(1042.0, 328.0, image=qr_waiver_img)

        self._text(
            37.0, 45.0, anchor="nw",
            text="Account Status:", fill="#F5F0E6", font=("Montserrat", 40 * -1),
        )
        self._text(
            430.0, 45.0, anchor="nw",
            text="Waiver Status:", fill="#F5F0E6", font=("Montserrat", 40 * -1),
        )
        self._text(
            45.0, 270.0, anchor="nw",
            text="Please scan the QR code\non the right and sign our \n     waiver",
            fill="#F5F0E6", font=("Montserrat", 48 * -1),
        )

        btn_img = self._photo(ASSETS_PATH / "button_done_scanning.png")
        btn = Button(
            self.canvas, image=btn_img,
            borderwidth=0, highlightthickness=0,
            command=lambda: controller.back_to_main(), relief="flat",
        )
        self._window(875.0, 581.0, btn, width=344, height=71)
