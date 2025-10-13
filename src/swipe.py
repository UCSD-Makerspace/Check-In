from tkinter import *
from ManualFill import *
from NoAccNoWaiverSwipe import *
from WaiverNoAccSwipe import *
from AccNoWaiverSwipe import *
from CheckInNoId import *
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
        self.last_barcode = None
        self.last_scan = 0
        self.scan_cooldown = 1.0
        self.is_processing = False

    def keyboardPress(self, key):
        util = utils()
        global id_string, swipe_error_shown
        
        if self.is_processing:
            return
        
        curr_frame = global_.app.get_curr_frame()
        if curr_frame not in (NoAccNoWaiverSwipe, WaiverNoAccSwipe, CheckInNoId):
            return
        
        try:
            focused_widget = global_.app.focus_get()
            if focused_widget and isinstance(focused_widget, (Entry, Text)):
                focused_widget.master.focus_set()
        except:
            pass
        
        id_string += key.char
        logging.debug("The array is now: " + repr(str(id_string)))
        
        if id_string.endswith("\r"):
            if util.IDVet(id_string) == "bad":
                id_string = ""
                if not swipe_error_shown:
                    swipe_error_shown = True
                    id_error = tkinter.Label(
                        global_.app.get_frame(NoAccNoWaiverSwipe),
                        text="Error, please scan again",
                    )
                    id_error.pack(pady=40)
                    id_error_2 = tkinter.Label(
                        global_.app.get_frame(WaiverNoAccSwipe),
                        text="Error, please scan again",
                    )
                    id_error_2.pack(pady=40)
                    id_error.after(1500, lambda: self.destroySwipeError(id_error))
                    id_error_2.after(1500, lambda: self.destroySwipeError(id_error_2))
                return
            
            self.swipeCard(id_string)
            id_string = ""

    def swipeCard(self, id_string):
        user_card_number = id_string.strip()
        
        current_time = time.time()
        if (user_card_number == self.last_barcode and 
            current_time - self.last_scan_time < self.cooldown_period):
            logging.debug("Suppressing repeat barcode scan")
            return
        
        self.is_processing = True
        
        try:
            u_data = self.pullUser(user_card_number, "Student")
            if not u_data:
                logging.info("Student search returned False, returning...")
                return
            
            self.last_barcode = user_card_number
            self.last_scan_time = current_time
            
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
        finally:
            global_.app.after(500, self.reset_processing)
    
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

    def reset_processing(self):
        self.is_processing = False

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
