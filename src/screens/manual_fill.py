from pathlib import Path
from tkinter import Button, Entry, StringVar, END
from .screen import Screen
from utils import Utils
import logging
import timeit

ASSETS_PATH = Path(__file__).parent.parent / "assets" / "manual_fill_assets"


#######################################################
# This is the frame where users will type information #
#######################################################

class ManualFill(Screen):
    def _build(self, controller):
        self.first_name = StringVar()
        self.last_name = StringVar()
        self.email = StringVar()
        self.pid = StringVar()

        img2 = self._photo(ASSETS_PATH / "image_2.png")
        self._image(640.0, 76.0, image=img2)

        img3 = self._photo(ASSETS_PATH / "image_3.png")
        self._image(640.0, 430.0, image=img3)

        img4 = self._photo(ASSETS_PATH / "image_4.png")
        self._image(605.0, 77.0, image=img4)

        img5 = self._photo(ASSETS_PATH / "image_5.png")
        self._image(1010.0, 77.0, image=img5)

        img6 = self._photo(ASSETS_PATH / "image_6.png")
        self._image(640.0, 542.0, image=img6)

        img7 = self._photo(ASSETS_PATH / "image_7.png")
        self._image(640.0, 440.0, image=img7)

        img8 = self._photo(ASSETS_PATH / "image_8.png")
        self._image(640.0, 339.0, image=img8)

        img9 = self._photo(ASSETS_PATH / "image_9.png")
        self._image(640.0, 239.0, image=img9)

        self._text(
            250.0, 45.0, anchor="nw",
            text="Account Status:", fill="#F5F0E6", font=("Montserrat", 40 * -1),
        )
        self._text(
            670.0, 45.0, anchor="nw",
            text="Waiver Status:", fill="#F5F0E6", font=("Montserrat", 40 * -1),
        )
        self._text(
            565.0, 177.0, anchor="nw",
            text="First Name", fill="#F5F0E6", font=("Montserrat", 24 * -1),
        )
        self._text(
            565.0, 278.0, anchor="nw",
            text="Last Name", fill="#F5F0E6", font=("Montserrat", 24 * -1),
        )
        self._text(
            595.0, 379.0, anchor="nw",
            text="Email", fill="#F5F0E6", font=("Montserrat", 24 * -1),
        )
        self._text(
            605.0, 480.0, anchor="nw",
            text="PID", fill="#F5F0E6", font=("Montserrat", 24 * -1),
        )

        btn_img = self._photo(ASSETS_PATH / "button_1.png")
        btn = Button(
            self.canvas, image=btn_img,
            borderwidth=0, highlightthickness=0,
            command=self._call_account_creation, relief="flat",
        )
        self._window(465.0, 598.0, btn, width=349, height=71)

        self.first_name_entry = Entry(self.canvas, textvariable=self.first_name, width=40, font=52)
        self._window(420.0, 227.0, self.first_name_entry)

        self.last_name_entry = Entry(self.canvas, textvariable=self.last_name, width=40, font=52)
        self._window(420.0, 327.0, self.last_name_entry)

        self.email_entry = Entry(self.canvas, textvariable=self.email, width=40, font=52)
        self._window(420.0, 428.0, self.email_entry)

        self.pid_entry = Entry(self.canvas, textvariable=self.pid, width=40, font=52)
        self._window(420.0, 530.0, self.pid_entry)

    def getEntries(self):
        return [
            self.first_name.get(),
            self.last_name.get(),
            self.email.get(),
            self.pid.get(),
        ]

    def clearEntries(self):
        self.first_name_entry.delete(0, END)
        self.last_name_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.pid_entry.delete(0, END)

    def updateEntries(self, fname, lname, email, pid):
        self.first_name_entry.insert(0, fname)
        self.last_name_entry.insert(0, lname)
        self.email_entry.insert(0, email)
        self.pid_entry.insert(0, pid)

    def _call_account_creation(self):
        util = Utils()
        data = self.getEntries()
        self.clearEntries()
        try:
            delay = timeit.timeit(
                lambda: util.createAccount(data[0], data[1], data[2], data[3], ManualFill),
                number=1,
            )
            logging.debug(f"Time to create account: {delay}")
        except Exception:
            logging.warning("Error occurred trying to create a user account", exc_info=True)
