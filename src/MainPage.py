# Part of this file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path
from tkinter import *


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/main_page_assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class MainPage(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.photoList = []
        self.loadWidgets(controller)

    def loadWidgets(self, controller):
        from QRCodes import QRCodes
        from CheckInNoId import CheckInNoId

        canvas = Canvas(
            self,
            bg="#153246",
            height=720,
            width=1280,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )

        canvas.place(x=0, y=0)
        image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))

        self.photoList.append(image_image_1)

        image_1 = canvas.create_image(640.0, 360.0, image=image_image_1)

        image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))

        self.photoList.append(image_image_2)

        image_2 = canvas.create_image(639.333984375, 359.333984375, image=image_image_2)

        canvas.create_text(
            336.0,
            602.0,
            anchor="nw",
            text="Please tap ID on the reader to start",
            fill="#F5F0E6",
            font=("Montserrat", 32 * -1),
        )

        canvas.create_text(
            67.0,
            270.0,
            anchor="nw",
            text="Entrepreneurship Center",
            fill="#F5F0E6",
            font=("Montserrat", 80 * -1, "bold"),
        )

        canvas.create_text(
            77.0,
            377.66796875,
            anchor="nw",
            text="Welcome Desk",
            fill="#F5F0E6",
            font=("Montserrat", 73 * -1),
        )

        image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))

        self.photoList.append(image_image_3)

        image_3 = canvas.create_image(88.0, 90.0, image=image_image_3)

        button_image_1 = PhotoImage(file=relative_to_assets("image_4.png"))

        self.photoList.append(button_image_1)

        button_1 = Button(
            self,
            image=button_image_1,
            bg="#153246",
            command=lambda: controller.show_frame(QRCodes),
            relief="flat",
            highlightthickness=0,
            bd=0,
        )

        button_1.place(x=53.0, y=55.0)

        button_2 = Button(
            self,
            image=image_image_3,
            text="No\nID",
            compound="center",
            bg="#153246",
            fg="white",
            command=lambda: controller.show_frame(CheckInNoId),
            relief="flat",
            highlightthickness=0,
            bd=0,
            font=("Montserrat", 36 * -1),
        )

        button_2.place(x=1130.0, y=40.0)
