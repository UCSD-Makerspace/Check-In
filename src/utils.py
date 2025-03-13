from datetime import datetime
import logging
import time
import global_
import tkinter
from gui import *
from UserThank import *

######################################################
# Utilities that I couldn't get to fit anywhere else #
######################################################


class utils:
    def __init__(self) -> None:
        pass

    def emailCheck(self, email):
        # Checks if the email is an @
        # and checks if it has a .
        # if not, return invalid
        # otherwise return good

        validations = (
            (lambda s: "@" in s, "Email is invalid"),
            (lambda s: "." in s, "Email is invalid"),
        )

        for valid, message in validations:
            if not valid(email):
                return message

        return "good"

    def nameCheck(self, name):
        if len(name) == 0:
            return "Name was not entered"

        return "good"

    def IDVet(self, id_check):
        if any(i.isalpha() for i in id_check):
            return "bad"

        if len(id_check) >= 16:
            return "bad"

        return "good"

    def getDatetime(self):
        return datetime.now().strftime("%m/%d/%Y %H:%M:%S")

    def createAccount(self, name, email, pid, affiliation, ManualFill):
        logging.info("Creating account")
        emailValid = self.emailCheck(email)
        nameValid = self.nameCheck(name)

        for validation in (emailValid, nameValid):
            if validation != "good":
                invalidID = tkinter.Label(
                    global_.app.get_frame(ManualFill), text=validation
                )
                invalidID.pack(pady=20)
                invalidID.after(3000, lambda: invalidID.destroy())
                return "bad"

        inProgress = tkinter.Label(
            global_.app.get_frame(ManualFill),
            text="Account creation in progress!",
            font=("Arial", 25),
        )
        inProgress.pack(pady=40)
        global_.app.update()
        logging.info(f"Creating user account for {name}")

        new_row = [
            name,
            self.getDatetime(),
            global_.rfid,
            pid,
            affiliation,
            email,
            True
        ]
        new_a = [
            self.getDatetime(),
            int(time.time()),
            name,
            global_.rfid,
            "New User",
            email,
            pid,
            "",
            affiliation
        ]

        no_wifi = Label(
            global_.app.get_frame(ManualFill),
            text="ERROR! Connection cannot be established, please let staff know.",
            font=("Arial", 25),
        )

        retries = 1
        while retries < 6:
            try:
                user_db = global_.sheets.get_user_db()
                user_db.append_row(new_row)
                global_.sheets.get_user_db_data(force_update=True)
                global_.sheets.get_activity_db().append_row(new_a)
                break
            except Exception as e:
                logging.warning(
                    "Exception occurred while in account creation", exc_info=True
                )
                no_wifi.pack(pady=20)
                global_.app.update()
                time.sleep(retries)
                retries += 1

        no_wifi.destroy()

        if retries == 6:
            global_.app.show_frame(MainPage)
            inProgress.destroy()
            return

        global_.app.get_frame(UserThank).displayName(name, MainPage)
        inProgress.destroy()
