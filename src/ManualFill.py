# Part of this file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer

from pathlib import Path
from tkinter import *
from tkinter import ttk
from utils import *
import logging

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/manual_fill_assets")

AFFILIATIONS = [
    "UC San Diego Undergraduate Student",
    "UC San Diego Graduate Student",
    "UC San Diego Post-Doc",
    "UC San Diego Faculty",
    "UC San Diego Staff",
    "UC San Diego Alumni",
    "Mentor",
    "Industry",
    "Community Member",
]


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


#######################################################
# This is the frame where users will type information #
#######################################################


class ManualFill(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.photoList = []
        self.entryList = []
        self.name = StringVar()
        self.email = StringVar()
        self.pid = StringVar()
        self.affiliation = StringVar()

        self.name_entry = 0
        self.email_entry = 0
        self.pid_entry = 0
        self.affiliation_entry = 0

        self.loadWidgets(controller)

    def loadWidgets(self, controller):
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

        image_2 = canvas.create_image(640.0, 76.0, image=image_image_2)

        image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))

        self.photoList.append(image_image_3)

        image_3 = canvas.create_image(640.0, 430.0, image=image_image_3)

        canvas.create_text(
            250.0,
            45.0,
            anchor="nw",
            text="Account Status:",
            fill="#F5F0E6",
            font=("Montserrat", 40 * -1),
        )

        canvas.create_text(
            670.0,
            45.0,
            anchor="nw",
            text="Waiver Status:",
            fill="#F5F0E6",
            font=("Montserrat", 40 * -1),
        )

        image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))

        self.photoList.append(image_image_4)

        image_4 = canvas.create_image(605.0, 77.0, image=image_image_4)

        image_image_5 = PhotoImage(file=relative_to_assets("image_5.png"))

        self.photoList.append(image_image_5)

        image_5 = canvas.create_image(1010.0, 77.0, image=image_image_5)

        image_image_6 = PhotoImage(file=relative_to_assets("image_6.png"))

        self.photoList.append(image_image_6)

        image_6 = canvas.create_image(640.0, 542.0, image=image_image_6)

        image_image_7 = PhotoImage(file=relative_to_assets("image_7.png"))

        self.photoList.append(image_image_7)

        image_7 = canvas.create_image(640.0, 440.0, image=image_image_7)

        image_image_8 = PhotoImage(file=relative_to_assets("image_8.png"))

        self.photoList.append(image_image_8)

        image_8 = canvas.create_image(640.0, 339.0, image=image_image_8)

        image_image_9 = PhotoImage(file=relative_to_assets("image_9.png"))

        self.photoList.append(image_image_9)

        image_9 = canvas.create_image(640.0, 239.0, image=image_image_9)

        canvas.create_text(
            520.0,
            177.0,
            anchor="nw",
            text="First and Last Name*",
            fill="#F5F0E6",
            font=("Montserrat", 24 * -1),
        )

        canvas.create_text(
            602.0,
            278.0,
            anchor="nw",
            text="Email*",
            fill="#F5F0E6",
            font=("Montserrat", 24 * -1),
        )

        canvas.create_text(
            615.0,
            379.0,
            anchor="nw",
            text="PID",
            fill="#F5F0E6",
            font=("Montserrat", 24 * -1),
        )

        canvas.create_text(
            583.0,
            480.0,
            anchor="nw",
            text="Affliation*",
            fill="#F5F0E6",
            font=("Montserrat", 24 * -1),
        )

        button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))

        self.photoList.append(button_image_1)

        self.button_1 = Button(
            self,
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.callAccountCreation(),
            relief="flat",
        )
        self.button_1.place(x=465.0, y=598.0, width=349.0, height=71.0)

        self.name_entry = Entry(
            self, textvariable=self.name, width=45, font=52, justify="center"
        )

        self.name_entry.place(x=420.0, y=227.0)

        self.email_entry = Entry(
            self, textvariable=self.email, width=45, font=52, justify="center"
        )

        self.email_entry.place(x=420.0, y=327.0)

        self.pid_entry = Entry(
            self, textvariable=self.pid, width=45, font=52, justify="center"
        )

        self.pid_entry.place(x=420.0, y=428.0)

        self.affiliation.set(AFFILIATIONS[0])

        self.affiliation_entry = self.affiliation_entry = ttk.Combobox(
            self,
            textvariable=self.affiliation,
            values=AFFILIATIONS,
            state="readonly",
            width=40,
            font=52,
        )

        self.affiliation_entry.config(width=40, font=52, justify="center")

        self.affiliation_entry.place(x=420.0, y=530.0)

    def getEntries(self):
        del self.entryList[:]
        self.entryList.append(self.name.get())
        self.entryList.append(self.email.get())
        self.entryList.append(self.pid.get())
        self.entryList.append(self.affiliation.get())
        return self.entryList

    def clearEntries(self):
        self.name_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.pid_entry.delete(0, END)
        self.affiliation.set(AFFILIATIONS[0])

    def updateEntries(self, fname, lname, email, pid):
        self.name_entry.insert(0, fname + " " + lname)
        self.email_entry.insert(0, email)
        self.pid_entry.insert(0, pid)

    def callAccountCreation(self):
        util = utils()
        data = self.getEntries()
        try:
            response = util.createAccount(
                data[0], data[1], data[2], data[3], ManualFill
            )
            if response != "bad":
                self.clearEntries()
        except Exception as e:
            logging.warning(
                "Error occurred trying to create a user account", exc_info=True
            )
