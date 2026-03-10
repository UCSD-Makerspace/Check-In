from pathlib import Path
from tkinter import Button
from screen import Screen
import global_

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/main_page_assets")


class MainPage(Screen):
    def _build(self, controller):
        from QRCodes import QRCodes
        from CheckInNoId import CheckInNoId

        logo = self._photo(ASSETS_PATH / "image_3.png")
        self._image(88.0, 90.0, image=logo)

        self._text(
            336.0, 602.0, anchor="nw",
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

        btn1_img = self._photo(ASSETS_PATH / "image_4.png")
        btn1 = Button(
            self.canvas, image=btn1_img, bg="#153246",
            command=lambda: controller.show_frame(QRCodes),
            relief="flat", highlightthickness=0, bd=0,
        )
        self._window(53.0, 55.0, btn1)

        btn2 = Button(
            self.canvas, image=logo, text="No\nID", compound="center",
            bg="#153246", fg="white",
            command=lambda: self._go_to_no_id(controller),
            relief="flat", highlightthickness=0, bd=0,
            font=("Montserrat", 36 * -1),
        )
        self._window(1130.0, 40.0, btn2)

    def _go_to_no_id(self, controller):
        from CheckInNoId import CheckInNoId
        no_id = global_.app.get_frame(CheckInNoId)
        no_id.clearEntries()
        controller.show_frame(CheckInNoId)
