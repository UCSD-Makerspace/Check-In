from datetime import datetime
from gspread_formatting import *
from fabman import *
import time
import global_
import tkinter
from gui import *
from UserThank import *
import threading

import timeit

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
        return datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")

    def createAccount(self, fname, lname, email, pid, ManualFill):
        start = time.perf_counter()
        validation_rule = DataValidationRule(
            BooleanCondition("BOOLEAN", ["TRUE", "FALSE"]),
        )

        idValid = self.IDCheck(pid)
        emailValid = self.emailCheck(email)
        nameValid = self.nameCheck(fname, lname)

        for validation in (idValid, emailValid, nameValid):
            if validation != "good":
                invalidID = tkinter.Label(
                    global_.app.get_frame(ManualFill), text=validation
                )
                invalidID.pack(pady=20)
                invalidID.after(3000, lambda: invalidID.destroy())
                return

        end1 = time.perf_counter()
        logging.debug(f"Time to validate info: {end1 - start}")

        inProgress = tkinter.Label(
            global_.app.get_frame(ManualFill),
            text="Account creation in progress!",
            font=("Arial", 25),
        )
        inProgress.pack(pady=40)
        global_.app.update()
        fab = fabman()
        full_name = fname + " " + lname
        logging.info(f"Creating user account for {full_name}")

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

        no_wifi = Label(
            global_.app.get_frame(ManualFill),
            text="ERROR! Connection cannot be established, please let staff know.",
            font=("Arial", 25),
        )

        end2 = time.perf_counter()
        logging.debug(f"Time to structure row entries: {end2 - end1}")

        retries = 1
        while retries < 6:
            try:
                fabman_thread = threading.Thread(
                    target=fab.createFabmanAccount,
                    args=(fname, lname, email, global_.rfid),
                )
                fabman_thread.start()

                user_db = global_.sheets.get_user_db()

                end3 = time.perf_counter()
                logging.debug(f"Time to pull user db: {end3 - end2}")

                user_db.append_row(new_row)
                end4 = time.perf_counter()
                logging.debug(f"Time to add row to gsheets: {end4 - end3}")

                global_.sheets.get_user_db_data(force_update=True)
                end5 = time.perf_counter()
                logging.debug(f"Time to force update gsheets: {end5 - end4}")

                name_cell = user_db.find(full_name, in_column=1)
                s_name_cell = str(name_cell.address)
                s_name_cell = s_name_cell[1 : len(s_name_cell)]

                end6 = time.perf_counter()
                logging.debug(f"Time to find user: {end6 - end5}")

                update_range = "I" + s_name_cell + ":AA" + s_name_cell
                set_data_validation_for_cell_range(
                    user_db, update_range, validation_rule
                )

                end7 = time.perf_counter()
                logging.debug(f"Time to set data validation: {end7 - end6}")

                def update_activity():
                    delay = timeit.timeit(
                        lambda: global_.sheets.get_activity_db().append_row(new_a), 
                        number=1
                    )
                    logging.debug(f"Time to add activity to gsheets (threaded): {delay}")

                add_row_thread = threading.Thread(
                    target=update_activity
                )
                add_row_thread.start()

                break
            except Exception as e:
                logging.warning("Exception occurred while in account creation")
                logging.exception("Exception occurred while in account creation")
                no_wifi.pack(pady=20)
                global_.app.update()
                time.sleep(retries)
                retries += 1

        no_wifi.destroy()

        if retries == 6:
            global_.app.show_frame(MainPage)
            inProgress.destroy()
            return

        end8 = time.perf_counter()
        logging.debug(f"Total time to send data: {end8 - end2}")

        w_data = global_.sheets.get_waiver_db_data()
        toGoTo = AccNoWaiverSwipe
        for i in w_data:
            if str(i["A_Number"])[1:] == pid[1:]:
                logging.info(
                    "User " + full_name + " made an account but had signed the waiver"
                )
                toGoTo = MainPage

        end9 = time.perf_counter()
        logging.debug(f"Time to check waiver data: {end9 - end8}")

        global_.app.get_frame(UserThank).displayName(full_name, toGoTo)
        inProgress.destroy()
