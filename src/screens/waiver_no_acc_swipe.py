from pathlib import Path
from tkinter import Button
from .screen import Screen
ASSETS_PATH = Path(__file__).parent.parent / "assets" / "waiver_no_acc_swipe_assets"


class WaiverNoAccSwipe(Screen):
    def _build(self, controller):
        img2 = self._photo(ASSETS_PATH / "image_2.png")
        self._image(640.0, 76.0, image=img2)

        img3 = self._photo(ASSETS_PATH / "image_3.png")
        self._image(640.0, 430.0, image=img3)

        img4 = self._photo(ASSETS_PATH / "image_4.png")
        self._image(576.0, 65.0, image=img4)

        img5 = self._photo(ASSETS_PATH / "image_5.png")
        self._image(1030.0, 65.0, image=img5)

        self._text(
            420.0, 350.0, anchor="nw",
            text="Please scan your ID barcode",
            fill="#F5F0E6", font=("Montserrat", 48 * -1),
        )
        self._text(
            215.0, 45.0, anchor="nw",
            text="Account Status:", fill="#F5F0E6", font=("Montserrat", 40 * -1),
        )
        self._text(
            690.0, 45.0, anchor="nw",
            text="Waiver Status:", fill="#F5F0E6", font=("Montserrat", 40 * -1),
        )

        btn_img = self._photo(ASSETS_PATH / "button_1.png")
        btn = Button(
            self.canvas, image=btn_img,
            borderwidth=0, highlightthickness=0,
            command=lambda: self._go_to_manual_fill(controller), relief="flat",
        )
        self._window(465.0, 554.0, btn, width=349, height=71)

    def _go_to_manual_fill(self, controller):
        controller.go_to_manual_fill()
