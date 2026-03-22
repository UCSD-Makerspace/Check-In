from pathlib import Path
from tkinter import Button
from .base import Screen

ASSETS_PATH = Path(__file__).parent.parent / "assets" / "create_account_barcode"
SHARED_PATH = Path(__file__).parent.parent / "assets" / "shared"


class CreateAccountBarcode(Screen):
    def _build(self, controller):
        logo = self._photo(SHARED_PATH / "button_generic.png")
        self._image(88.0, 90.0, image=logo)

        home_img = self._photo(SHARED_PATH / "icon_home.png")
        home_btn = Button(
            self.canvas, image=home_img, bg="#153246",
            command=lambda: controller.back_to_main(),
            relief="flat", highlightthickness=0, bd=0,
        )
        self._window(53.0, 55.0, home_btn)

        outline1_img = self._photo(ASSETS_PATH / "outline_1.png")
        self._image(640.0, 76.0, image=outline1_img)

        outline2_img = self._photo(ASSETS_PATH / "outline_2.png")
        self._image(640.0, 430.0, image=outline2_img)

        icon_unchecked = self._photo(SHARED_PATH / "icon_unchecked_box.png")
        self._image(576.0, 65.0, image=icon_unchecked)

        icon_checked = self._photo(SHARED_PATH / "icon_checked_box.png")
        self._image(1030.0, 65.0, image=icon_checked)

        self._text(
            640.0, 374.0, anchor="center",
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

        btn_img = self._photo(ASSETS_PATH / "button_fill_manually.png")
        btn = Button(
            self.canvas, image=btn_img,
            borderwidth=0, highlightthickness=0,
            command=lambda: controller.go_to_create_account_manual(), relief="flat",
        )
        self._window(465.0, 554.0, btn, width=349, height=71)
