import tkinter
from screens.manual_fill import ManualFill
from screens.no_acc_no_waiver_swipe import NoAccNoWaiverSwipe
from screens.waiver_no_acc_swipe import WaiverNoAccSwipe
from screens.acc_no_waiver_swipe import AccNoWaiverSwipe
from screens.check_in_no_id import CheckInNoId
from get_info_from_pid import contact_client
from utils import Utils
import global_
import logging

############################################
# This class helps handle reading magswipe #
############################################

swipe_error_shown = False


class Swipe:
    def __init__(self):
        global id_string
        id_string = ""

    def keyboardPress(self, key):
        util = Utils()
        global id_string, swipe_error_shown
        curr_frame = global_.app.get_curr_frame()

        if curr_frame not in (NoAccNoWaiverSwipe, WaiverNoAccSwipe, CheckInNoId):
            return

        id_string += key.char
        logging.debug("The array is now: " + repr(str(id_string)))

        if id_string.endswith("\r"):
            if util.IDVet(id_string) == "bad":
                id_string = ""
                if not swipe_error_shown:
                    swipe_error_shown = True
                    canvas = global_.app.canvas
                    id_error = tkinter.Label(
                        canvas, text="Error, please scan again",
                        bg="#153246", fg="white", font=("Arial", 20),
                    )
                    id_error.place(relx=0.5, rely=0.85, anchor="center")
                    id_error_2 = id_error  # single label serves both swipe screens
                    id_error.after(1500, lambda: self.destroySwipeError(id_error))
                    id_error_2.after(1500, lambda: self.destroySwipeError(id_error_2))
                return

            self.swipeCard(id_string)
            id_string = ""

    def pullUser(self, barcode, u_type):
        # This function takes in the User's ID and
        # if they are a Student or Staff
        # and runs David's query funciton accordingly
        # It returns a list containing:
        # [fname, lname, [emails]]
        u_info = []

        logging.info(f"Card barcode read is: {barcode}. Trying to pull user...")

        contact = contact_client()
        try:
            if u_type == "Staff":
                u_info = contact.get_staff_info(barcode)
            elif u_type == "Student":
                u_info = contact.get_student_info(barcode)
        except Exception as e:
            logging.warning(
                "An exception has ocurred with pulling user information", exc_info=True
            )
            return None
        if not u_info:
            logging.info("Student search returned False, returning...")
            return
        
        logging.info(f"Info pull succeeded:\n {u_info[0]}, {u_info[1]}, {u_info[3]}")
        return u_info

    def swipeCard(self, id_string):
        # Grabs the input from the global swipe entry
        # Deletes text from the entry box
        # Checks if any of the ID is a letter
        # If so return
        # Calls magswipe() on the entered string

        user_card_number = id_string.strip()

        # u_info = self.magSwipe(id_string)

        # u_type = u_info[0]
        # u_id = u_info[1]
        # u_id = u_id.replace("+E?", "")[:9]

        # u_data is a list containing the user type and their ID
        u_data = self.pullUser(user_card_number, "Student")
        if not u_data:
            logging.info("Student search returned False, returning...")
            return
        # if u_type == "Student":
        #     u_id = "A" + u_id
        if global_.app.get_curr_frame() == CheckInNoId:
            global_.app.get_frame(CheckInNoId).clearEntries()
            global_.app.get_frame(CheckInNoId).updateEntries(u_data[3])
            return

        email_to_use = "" if len(u_data[2]) == 0 else u_data[2][0]
        for email in u_data[2]:
            if email.endswith("@ucsd.edu"):
                email_to_use = email

        manfill = global_.app.get_frame(ManualFill)
        manfill.clearEntries()
        logging.info(
            f"Filling data with {u_data[0]} {u_data[1]} {email_to_use} {u_data[3]}"
        )
        manfill.updateEntries(u_data[0], u_data[1], email_to_use, u_data[3])

        global_.app.show_frame(ManualFill)

    def magSwipe(self, ID):
        # Makes a new empty string
        # Takes only chars 3-11 from the card swipe text
        # Returns student or staff ID

        u_type = ""

        if ID[2] == "9":
            u_type = "Student"
        elif ID[2] == "0":
            u_type = "Staff"

        s = ""
        for c in range(3, 11):
            s += ID[c]
        return [u_type, s]

    def destroySwipeError(self, id_error):
        global swipe_error_shown
        id_error.destroy()
        swipe_error_shown = False
