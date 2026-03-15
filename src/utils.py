from datetime import datetime
import time
import global_
import tkinter
from screens.MainPage import MainPage
from screens.AccNoWaiverSwipe import AccNoWaiverSwipe
from screens.UserThank import UserThank
import logging

######################################################
# Utilities that I couldn't get to fit anywhere else #
######################################################


class utils:
    def __init__(self) -> None:
        pass

    def emailCheck(self, email):
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
        if len(user_id) <= 2 or len(user_id) > 12:
            return "PID was not entered correctly"
        return "good"

    def IDVet(self, id_check):
        if any(i.isalpha() for i in id_check):
            return "bad"

        if len(id_check) >= 16:
            return "bad"

        return "good"

    def getDatetime(self):
        return datetime.now().strftime("%m/%d/%Y %H:%M:%S")

    def createAccount(self, fname, lname, email, pid, ManualFill):
        start = time.perf_counter()
        idValid = self.IDCheck(pid)
        emailValid = self.emailCheck(email)
        nameValid = self.nameCheck(fname, lname)

        canvas = global_.app.canvas

        for validation in (idValid, emailValid, nameValid):
            if validation != "good":
                invalidID = tkinter.Label(
                    canvas, text=validation, bg="#153246", fg="white", font=("Arial", 20)
                )
                invalidID.place(relx=0.5, rely=0.83, anchor="center")
                invalidID.after(3000, lambda: invalidID.destroy())
                return

        end1 = time.perf_counter()
        logging.debug(f"Time to validate info: {end1 - start}")

        inProgress = tkinter.Label(
            canvas,
            text="Account creation in progress!",
            bg="#153246", fg="white", font=("Arial", 25),
        )
        inProgress.place(relx=0.5, rely=0.87, anchor="center")
        global_.app.update()

        full_name = fname + " " + lname
        logging.info(f"Creating user account for {full_name}")

        no_wifi = tkinter.Label(
            canvas,
            text="ERROR! Connection cannot be established, please let staff know.",
            bg="#153246", fg="white", font=("Arial", 25),
        )

        end2 = time.perf_counter()
        logging.debug(f"Time to structure row entries: {end2 - end1}")

        retries = 1
        while retries < 6:
            try:
                result = global_.sheets.create_account(fname, lname, email, pid, global_.rfid)
                end3 = time.perf_counter()
                logging.debug(f"Time to create account: {end3 - end2}")

                if result is None:
                    raise Exception("Account creation returned no result")

                break
            except Exception as e:
                logging.warning("Exception occurred while in account creation")
                logging.exception("Exception occurred while in account creation")
                no_wifi.place(relx=0.5, rely=0.91, anchor="center")
                global_.app.update()
                time.sleep(retries)
                retries += 1

        no_wifi.destroy()

        if retries == 6:
            global_.app.show_frame(MainPage)
            inProgress.destroy()
            return

        end4 = time.perf_counter()
        logging.debug(f"Total time to send data: {end4 - end2}")

        checkin_result = global_.sheets.checkin_by_uuid(global_.rfid)
        toGoTo = AccNoWaiverSwipe if checkin_result.get("status") == "no_waiver" else MainPage

        end5 = time.perf_counter()
        logging.debug(f"Time to check waiver via check-in: {end5 - end4}")

        global_.app.get_frame(UserThank).displayName(full_name, toGoTo)
        inProgress.destroy()
