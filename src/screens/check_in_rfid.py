from pathlib import Path
from tkinter import Button
from .base import Screen
from .qr_codes import QRCodes

ASSETS_PATH = Path(__file__).parent.parent / "assets" / "check_in_rfid"
SHARED_PATH = Path(__file__).parent.parent / "assets" / "shared"


class CheckInRFID(Screen):
    def _build(self, controller):

        logo = self._photo(SHARED_PATH / "button_generic.png")
        self._image(88.0, 90.0, image=logo)

        self._text(
            640.0, 618.0, anchor="center",
            text="Please tap ID on the black box to start",
            fill="#F5F0E6", font=("Montserrat", 32 * -1),
        )
        self._text(
            67.0, 270.0, anchor="nw",
            text="UCSD Makerspace",
            fill="#F5F0E6", font=("Montserrat", 113 * -1, "bold"),
        )
        self._text(
            77.0, 377.66796875, anchor="nw",
            text="Welcome Desk",
            fill="#F5F0E6", font=("Montserrat", 73 * -1),
        )

        btn1_img = self._photo(ASSETS_PATH / "icon_check_in.png")
        btn1 = Button(
            self.canvas, image=btn1_img, bg="#153246",
            command=lambda: controller.show_frame(QRCodes),
            relief="flat", highlightthickness=0, bd=0,
        )
        self._window(53.0, 55.0, btn1)

        btn2 = Button(
            self.canvas, image=logo, text="No\nID", compound="center",
            bg="#153246", fg="white",
            command=lambda: controller.go_to_no_id(),
            relief="flat", highlightthickness=0, bd=0,
            font=("Montserrat", 36 * -1),
        )
        self._window(1130.0, 40.0, btn2)
