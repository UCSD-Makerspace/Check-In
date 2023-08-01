from datetime import datetime
from gspread_formatting import *
import tkinter
import fabman
import time


class utils ():
    def __init__(self):
        self.rfid = 0
        
    def setRFID(self, rfid):
        self.rfid = rfid
        
    #TODO: 1 and 0 not good and bad
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
    
    def IDVet(id_check):
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
    
    def getDatetime():
        return datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    
    def createAccount(self, fname, lname, email, pid):        
        validation_rule = DataValidationRule(
            BooleanCondition("BOOLEAN", ["TRUE", "FALSE"]),
        )

        idValid = self.IDCheck(pid)
        emailValid = self.emailCheck(email)
        nameValid = self.nameCheck(fname, lname)
        
        
        for validation in (idValid, emailValid, nameValid):
            if validation != "good":
                #TODO: This needs to be done as a function
                #in the sheets class 
                #invalidID = tkinter.Label(
                #    self.app.get_frame(ManualFill), text=validation
                #)
                #invalidID.pack(pady=20)
                #invalidID.after(3000, lambda: invalidID.destroy())
                return
        #TODO: This probably shouldn't happen
        #inProgress = tkinter.Label(
        #    gui.get_frame(ManualFill), text="Account creation in progress!"
        #)
        #inProgress.pack(pady=20)
        #self.app.update()
        fab = fabman()
        full_name = fname+" "+lname
        print(f"Creating user account for {full_name}")
        fab.createFabmanAccount(fname, lname, email, self.rfid)
        new_row = [full_name, self.getDatetime(), self.rfid, pid, "", email, " ", " "]
        new_a = [self.getDatetime(), int(time.time()),full_name, self.rfid, "New User", "", "", "",]
        self.getUserDB().append_row(new_row)
        name_cell = self.getUserDB().find(full_name)
        s_name_cell = str(name_cell.address)
        s_name_cell = s_name_cell[1 : len(s_name_cell)]
        update_range = "I" + s_name_cell + ":AA" + s_name_cell
        set_data_validation_for_cell_range(self.getUserDB(), update_range, validation_rule)
        self.getActivityLog().append_row(new_a)    

        w_data = self.getWaiverDB().get_all_records(numericise_ignore=["all"])
        #toGoTo = docuPage
        for i in w_data:
            if str(i["A_Number"])[1:] == pid[1:]:
                print("User " + full_name + " made an account but had signed the waiver")
                #toGoTo = mainPage
        """
        inProgress.destroy()
        gui.show_frame(toGoTo)
        accountMadeLabel = tkinter.Label(
            gui.get_frame(toGoTo),
            text="Thank you, " + fn + ", your account has been created",
        )
        accountMadeLabel.pack(pady=20)
        accountMadeLabel.after(5000, lambda: accountMadeLabel.destroy())

        gui.after(20000, lambda: backToMainFromDoc(controller))
        """