from datetime import datetime
import logging
import time
import global_
import tkinter
from gui import *
from UserThank import *
from UserWelcome import UserWelcome
from CheckInReason import CheckInReason

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

        # Check if user already exists with this PID
        user_data = global_.sheets.get_user_db_data()
        existing_user = None
        for user in user_data:
            if user["Email Address"] == email:
                existing_user = user
                break

        if existing_user:
            # Update existing user with NFID
            new_row = [
                existing_user["Name"],
                self.getDatetime(),
                global_.rfid,  # Link the NFID to the existing account
                existing_user["Student ID"],
                existing_user["Affiliation"],
                existing_user["Email Address"],
                existing_user["Entrepreneurship Center?"]
            ]
        else:
            # Create new user
            new_row = [
                name,
                self.getDatetime(),
                global_.rfid,
                pid,
                affiliation,
                email,
                True # Account created at entrepreneurship center, not basement
            ]

        new_a = [
            self.getDatetime(),
            int(time.time()),
            name if not existing_user else existing_user["Name"],
            global_.rfid,
            "New User" if not existing_user else "User Checkin",
            email if not existing_user else existing_user["Email Address"],
            pid if not existing_user else existing_user["Student ID"],
            "",
            affiliation if not existing_user else existing_user["Affiliation"]
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
                if existing_user:
                    # Find and update the existing user's row
                    for i, row in enumerate(user_data):
                        if row["Student ID"].lstrip("Aa") == pid.lstrip("Aa"):
                            user_db.update_cell(i + 2, 3, global_.rfid)  # Update NFID
                            break
                else:
                    user_db.append_row(new_row)
                global_.sheets.get_user_db_data(force_update=True)
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

        activity_log = global_.sheets.get_activity_db()
        activity_log.append_row(new_a)
        global_.traffic_light.set_green()
        global_.app.get_frame(UserWelcome).displayName(name if not existing_user else existing_user["Name"])
        inProgress.destroy()
