from datetime import datetime
from gspread_formatting import *
from fabman import *
import json
import time
import global_
import tkinter
from gui import *
from UserThank import *
import threading
from get_info_from_pid import contact_client

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

    def get_current_term() -> str:
        month = datetime.today().month
        year = datetime.today().year % 100
        if month in [1,2,3]:
            return f"WI{year}"
        elif month in [4,5,6]:
            return f"SP{year}"
        elif month in [7,8]:
            return f"SU{year}"
        else:
            return f"FA{year}"

    # Helper function to return true if user matches waiver by ID or email, false otherwise
    def check_waiver_match(self, curr_user, waiver_data) -> bool:
        if not waiver_data:
            logging.warning("Waiver data is empty or None in check_waiver_match")
            return False
        
        user_id = curr_user["Student ID"].strip().lower()
        user_email = curr_user["Email Address"].strip().lower()

        if user_id.startswith("a"):
            user_id = user_id[1:]

        for waiver in waiver_data:
            waiver_id = waiver.get("A_Number", "").strip().lower()
            waiver_email = waiver.get("Email", "").strip().lower()

            if waiver_id.startswith("a"):
                waiver_id = waiver_id[1:]

            if user_id == waiver_id or user_email == waiver_email:
                return True
            
        logging.warning(f"Waiver match failed for user_id={user_id}, email={user_email}")
        return False

    def check_user_payment(self, curr_user: dict, payment_data: list) -> bool:
        if not curr_user:
            logging.warning("check_user_payment called with no valid user")
       
        curr_term = self.get_current_term()
        local_paid_term = curr_user.get("Last Paid Term", "").strip().upper()

        user_id = curr_user.get("Student ID", "").strip().lower().lstrip("a")
        user_email = curr_user.get("Email Address", "").strip().lower()
        latest_paid_term = local_paid_term

        for row in payment_data:
            term = row.get("Type", "").strip().upper()
            pay_id = row.get("Student ID", "").strip().lower().lstrip("a")
            pay_email = row.get("Email Address", "").strip().lower()

            if (user_id and user_id == pay_id) or (user_email and user_email == pay_email):
                if term and term > latest_paid_term:
                    latest_paid_term = term

            if latest_paid_term != local_paid_term:
                logging.info(f"Updating local payment term for {curr_user.get('Name')} from {local_paid_term} to {latest_paid_term}")
                curr_user["Last Paid Term"] = latest_paid_term

            if latest_paid_term == curr_term:
                return True
            else:
                logging.info(f"User {curr_user.get("Name")} has not paid for {curr_term}")
                return False

    def createAccount(self, fname, lname, email, pid, ManualFill):
        user_data = {}
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

        # Open and write to local database on account creation
        try:
            with open("assets/local_user_db.json", "r", encoding="utf-8") as f:
                user_data = json.load(f)
        except FileNotFoundError:
            logging.error("Local user database not found. Please run export_user_db.py to create it.")
    
        contact = contact_client()
        user_info = contact.get_student_info_pid(pid)
        if user_info:
            firstEnrTerm = user_info[4]
            lastEnrTerm = user_info[5]
        else:
            firstEnrTerm = None
            lastEnrTerm = None

        user_data[global_.rfid] = {
            "Name": full_name,
            "Timestamp": self.getDatetime(),
            "Student ID": pid,
            "Email Address": email,
            "Waiver Signed": " ",
            "firstEnrTrm": firstEnrTerm,
            "lastEnrTrm": lastEnrTerm,
            "lastCheckIn": None,
            "Last Paid Term": None,    
        }
        with open("assets/local_user_db.json", "w", encoding="utf-8") as f:
                        json.dump(user_data, f, indent=2)
        logging.info(f"Local user database updated with {full_name} on account creation")

        new_a = [
            self.getDatetime(),
            int(time.time()),
            full_name,
            global_.rfid,
            "New User",
            "",
            firstEnrTerm,
            lastEnrTerm,
        ]

        no_wifi = Label(
            global_.app.get_frame(ManualFill),
            text="ERROR! Connection cannot be established, please let staff know.",
            font=("Arial", 25),
        )

        retries = 1
        while retries < 6:
            try:
                fabman_thread = threading.Thread(
                    target=fab.createFabmanAccount,
                    args=(fname, lname, email, global_.rfid),
                )
                fabman_thread.start()

                user_db = global_.sheets.get_user_db()
                user_db.append_row(new_row)

                global_.sheets.get_user_db_data(force_update=True)

                name_cell = user_db.find(full_name, in_column=1)
                s_name_cell = str(name_cell.address)
                s_name_cell = s_name_cell[1 : len(s_name_cell)]

                update_range = "I" + s_name_cell + ":AA" + s_name_cell
                set_data_validation_for_cell_range(
                    user_db, update_range, validation_rule
                )

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

        w_data = global_.sheets.get_waiver_db_data()
        toGoTo = AccNoWaiverSwipe
        for i in w_data:
            if str(i["A_Number"])[1:] == pid[1:]:
                logging.info(
                    "User " + full_name + " made an account but had signed the waiver"
                )
                toGoTo = MainPage

        global_.app.get_frame(UserThank).displayName(full_name, toGoTo)
        inProgress.destroy()