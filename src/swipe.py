from tkinter import *
from ManualFill import *
from NoAccNoWaiverSwipe import *
from WaiverNoAccSwipe import *
from AccNoWaiverSwipe import *
from get_info_from_pid import *
from utils import *
import global_

############################################
# This class helps handle reading magswipe #
############################################

swipe_error_shown = False


class swipe:
    def __init__(self):
        global id_string
        id_string = ""

    def keyboardPress(self, key):
        util = utils()
        global id_string, swipe_error_shown
        if (global_.app.get_curr_frame() != NoAccNoWaiverSwipe) and (
            global_.app.get_curr_frame() != WaiverNoAccSwipe
        ):
            # If one of the swipe pages is not on top
            # Then don't do anything
            return

        check = util.IDVet(id_string)
        if check == "bad":
            id_string = ""
            if not swipe_error_shown:
                swipe_error_shown = True
                id_error = tkinter.Label(
                    global_.app.get_frame(NoAccNoWaiverSwipe),
                    text="Error, please swipe again",
                )
                id_error.pack(pady=40)
                id_error_2 = tkinter.Label(
                    global_.app.get_frame(WaiverNoAccSwipe),
                    text="Error, please swipe again",
                )
                id_error_2.pack(pady=40)
                id_error.after(1500, lambda: self.destroySwipeError(id_error))
                id_error_2.after(1500, lambda: self.destroySwipeError(id_error_2))
            return

        id_string = id_string + key.char
        logging.debug("The array is now: " + str(id_string))
        if (key.char == "?") and (len(id_string) == 37):
            self.swipeCard(id_string)

    def pullUser(self, ID, u_type):
        # This function takes in the User's ID and
        # if they are a Student or Staff
        # and runs David's query funciton accordingly
        # It returns a list containing:
        # [fname, lname, [emails]]
        u_info = []

        logging.info(f"Card ID read is: {ID}. Trying to pull user...")

        contact = contact_client()
        try:
            if u_type == "Staff":
                u_info = contact.get_staff_info("A" + ID)
            elif u_type == "Student":
                u_info = contact.get_student_info("A" + ID)
        except Exception as e:
            logging.warning(
                "An exception has ocurred with pulling user information", exc_info=True
            )
            return

        logging.info(f"Info pull succeeded:\n{u_info}")
        return u_info

    def swipeCard(self, id_string):
        # Grabs the input from the global swipe entry
        # Deletes text from the entry box
        # Checks if any of the ID is a letter
        # If so return
        # Calls magswipe() on the entered string

        u_info = self.magSwipe(id_string)

        u_type = u_info[0]
        u_id = u_info[1]
        u_id = u_id.replace("+E?", "")[:9]

        # u_data is a list containing the user type and their ID
        u_data = self.pullUser(u_id, u_type)
        if u_data == False:
            logging.info("Student search returned False, returning...")
            return
        if u_type == "Student":
            u_id = "A" + u_id

        manfill = global_.app.get_frame(ManualFill)
        manfill.clearEntries()

        email_to_use = u_data[2][0]
        for email in u_data[2]:
            if email.endswith("@ucsd.edu"):
                email_to_use = email

        u_id = u_id.replace("+E?", "")[:9]

        logging.info(f"Filling data with {u_data[0]} {u_data[1]} {email_to_use} {u_id}")
        manfill.updateEntries(u_data[0], u_data[1], email_to_use, u_id)

        global_.app.show_frame(ManualFill)

        id_string = ""

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
