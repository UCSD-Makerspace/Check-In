from datetime import datetime
from gspread_formatting import *
from fabman import *
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

    def nameCheck(self, fname, lname):
        if len(fname) == 0 or len(lname) == 0:
            return "Name was not entered"

        return "good"

    def IDCheck(self, user_id):
        if len(user_id) <= 2:
            return "PID was not entered"
        return "good"

    def IDVet(self, id_check):
        for c in id_check:
            if c == "+":
                return "bad"

        if "\r" in id_check:
            return "bad"

        if len(id_check) > 0:
            if id_check[0] == "?":
                return "bad"

        if id_check.isalpha():
            return "bad"

        return "good"

    def getDatetime(self):
        return datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")

    def createAccount(self, fname, lname, email, pid, ManualFill):

        validation_rule = DataValidationRule(
            BooleanCondition("BOOLEAN", ["TRUE", "FALSE"]),
        )

        idValid = self.IDCheck(pid)
        emailValid = self.emailCheck(email)
        nameValid = self.nameCheck(fname, lname)

        for validation in (idValid, emailValid, nameValid):
            if validation != "good":
                invalidID = tkinter.Label(
                    self.app.get_frame(ManualFill), text=validation
                )
                invalidID.pack(pady=20)
                invalidID.after(3000, lambda: invalidID.destroy())
                return
        inProgress = tkinter.Label(
            global_.app.get_frame(ManualFill),
            text="Account creation in progress!",
            font=("Arial", 25),
        )
        inProgress.pack(pady=40)
        global_.app.update()
        fab = fabman()
        full_name = fname + " " + lname
        print(f"Creating user account for {full_name}")
        try:
            fab.createFabmanAccount(fname, lname, email, global_.rfid)
        except:
            print("An ERROR has occurred making a fabman account")
        new_row = [
            full_name,
            self.getDatetime(),
            global_.rfid,
            pid,
            "",
            email,
            " ",
            " ",
        ]
        new_a = [
            self.getDatetime(),
            int(time.time()),
            full_name,
            global_.rfid,
            "New User",
            "",
            "",
            "",
        ]

        user_db = global_.sheets.get_user_db()
        user_db.append_row(new_row)

        # FIXME: user_db and others are not being used properly

        name_cell = user_db.find(full_name)
        s_name_cell = str(name_cell.address)
        s_name_cell = s_name_cell[1 : len(s_name_cell)]
        update_range = "I" + s_name_cell + ":AA" + s_name_cell
        set_data_validation_for_cell_range(user_db, update_range, validation_rule)
        global_.sheets.get_activity_db().append_row(new_a)

        w_data = global_.sheets.get_waiver_db_data()
        toGoTo = AccNoWaiverSwipe
        for i in w_data:
            if str(i["A_Number"])[1:] == pid[1:]:
                print(
                    "User " + full_name + " made an account but had signed the waiver"
                )
                toGoTo = MainPage

        global_.app.get_frame(UserThank).displayName(full_name, toGoTo)
        inProgress.destroy()
