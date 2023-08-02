import gspread
import os.path
from oauth2client.service_account import ServiceAccountCredentials
import time

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
        #os.chdir("/home/makeradmin/checkin_logan/")
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
    
    def appendActivityLog(self, new_a):
        try:
            self.user_db.append_row(new_a)
        except:
            print("Unable to append row, ACTIVITY")
    
    def appendUserDB(self, new_row):
        try:
            self.user_db.append_row(new_row)
        except:
            print("Unable to append row, USERDB")
        
    #TODO: Not sure if this is needed still
    #def backToMainFromDoc(self):
        #if gui.get_curr_frame() == docuPage:
        #    gui.show_frame(MainPage)