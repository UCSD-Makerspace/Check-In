from tkinter import * 
import tkinter
from ManualFill import *
from NoAccNoWaiverSwipe import *
from WaiverNoAccSwipe import *
from AccNoWaiverSwipe import *
from get_info_from_pid import *
from utils import *


class swipe():
    def __init__(self, app):
        self.app = app
    
    def keyboardPress(self, key):
        util = utils()
        global id_string, swipe_error_shown
        if (self.app.get_curr_frame() != NoAccNoWaiverSwipe) or (self.app.get_curr_frame() != WaiverNoAccSwipe):
            # If one of the swipe pages is not on top
            # Then don't do anything
            return

        check = util.IDVet(id_string)
        if check == "bad":
            id_string = ""
            #if not swipe_error_shown:
            #    swipe_error_shown = True
                #id_error = tkinter.Label(
                #    gui.get_frame(swipePage), text="Error, please swipe again"
                #)
                #id_error.pack(pady=40)
                #id_error.after(1500, lambda: self.destroySwipeError(id_error))
            return

        id_string = id_string + key.char
        print("The array is now: " + str(id_string))
        if (key.char == "?") and (len(id_string) == 37):
            self.swipeCard(id_string)
            
    def pullUser(self, ID, u_type):
        # This function takes in the User's ID and
        # if they are a Student or Staff
        # and runs David's query funciton accordingly
        # It returns a list containing:
        # [fname, lname, [emails]]
        print("ID Read is: " + ID)
        print("Trying to pull user...")
        type_label = tkinter.Label(
            self.app.get_frame(ManualFill), text=f"This user is a {u_type}"
        )
        correct = tkinter.Label(
            self.get_frame(ManualFill), text=f"Is this information correct?"
        )

        correct.pack(pady=40)
        correct.after(10000, lambda: correct.destroy())

        type_label.pack(pady=40)
        type_label.after(
            10000, lambda: type_label.destroy()
        )  # This line is a test and will not be in the final

        #return ["Logan", "Corrente", ["logan6656@gmail.com", "locorrente@ucsd.edu"]]

        contact = contact_client()
        try:
            if u_type == "Staff":
                u_info = contact.get_staff_info(ID)
            elif u_type == "Student":
                u_info = contact.get_student_info(ID)
        except:
            print("An exception has ocurred with pulling user information")
        print("Info pull succeeded:")
        print(u_info)
        return u_info
        
        
    def swipeCard(self, id_string):
        # Grabs the input from the global swipe entry
        # Deletes text from the entry box
        # Checks if any of the ID is a letter
        # If so return
        # Calls magswipe() on the entered string

        # TODO: entry boxes

        #global id_string, e1, e2, e3, e4
        #vetted_id = IDVet(id_string)
        u_info = self.magSwipe(id_string)

        u_type = u_info[0]
        u_id = u_info[1]

        # u_data is a list containing the user type and their ID
        u_data = self.pullUser(u_id, u_type)
        if u_type == "Student":
            u_id = "A" + u_id

        manfill = self.app.get_frame(ManualFill)
        manfill.clearEntries()
        manfill.updateEntries(u_data[0], u_data[1], u_data[2][0], u_id)

        self.app.show_frame(ManualFill)

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
    
    def destroySwipeError(id_error):
        #TODO: This may not be needed anymore
        global swipe_error_shown
        id_error.destroy()
        swipe_error_shown = False