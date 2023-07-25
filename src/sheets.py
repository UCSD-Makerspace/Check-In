import gspread
import os.path
from gspread_formatting import *
from oauth2client.service_account import ServiceAccountCredentials
import time
from swipe import *
from utils import *
from gui import *
from fabman import *


class sheets:
    def __init__(self):
        self.user_db = ""
        self.activity_log = ""
        self.waiver_db = ""
        try:
            self.connectSheet()
        except:
            print("gspread was unable to connect")
                    
    def connectSheet(self):
        #global user_db, w_db, a_log
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive",
        ]
        #TODO: This file path needs to be changed
        os.chdir("/home/makeradmin/checkin_logan/")
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            os.path.abspath("creds.json"), scope
        )
        client = gspread.authorize(creds)
        self.user_db = client.open("User Database").sheet1  # Open the spreadhseet
        print("User Database Loaded")
        self.activity_log = client.open_by_url(
            "https://docs.google.com/spreadsheets/d/1aLBb1J2ifoUG2UAxHHbwxNO3KrIIWoI0pnZ14c5rpOM/edit?usp=drive_web&ouid=104398832910104737872"
        ).sheet1
        print("Activity Log Loaded")
        self.waiver_db = client.open("Waiver Signatures").sheet1
        print("Waiver Database Loaded")

    def getUserDB(self):
        return self.user_db
    
    def getActivityLog(self):
        return self.activity_log
    
    def getWaiverDB(self):
        return self.waiver_db
    
    #TODO: Not sure if this is needed still
    #def backToMainFromDoc(self):
        #if gui.get_curr_frame() == docuPage:
        #    gui.show_frame(MainPage)
    
    def createAccount(self, fn, ln, e, p, rfid):
        #fn->first name
        #ln->last name
        #e->email
        #p->pid
        #rfid->id unique key
        validation_rule = DataValidationRule(
            BooleanCondition("BOOLEAN", ["TRUE", "FALSE"]),
        )

        idValid = utils.IDCheck(p)
        emailValid = utils.emailCheck(e)
        nameValid = utils.nameCheck(fn, ln)
        
        
        for validation in (idValid, emailValid, nameValid):
            if validation != "good":
                invalidID = tkinter.Label(
                    gui.get_frame(ManualFill), text=validation
                )
                invalidID.pack(pady=20)
                invalidID.after(3000, lambda: invalidID.destroy())
                return
        #TODO: This probably shouldn't happen
        inProgress = tkinter.Label(
            gui.get_frame(ManualFill), text="Account creation in progress!"
        )
        inProgress.pack(pady=20)
        gui.update()
        ManualFill.clearEntries()
        
        full_name = fn+" "+ln
        print(f"Creating user account for {full_name}")
        fabman.createFabmanAccount(fn, ln, e, rfid)
        new_row = [full_name, utils.getDatetime(), rfid, p, "", e, " ", " "]
        new_a = [utils.getDatetime(), int(time.time()),full_name, rfid, "New User", "", "", "",]
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
            if str(i["A_Number"])[1:] == p[1:]:
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