import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials

#############################################################
# Declare all globals, and try to connect the google sheets #
# Also places the sheets in accessible global arrays        #
#############################################################
def init():
    global rfid, user_db, activity_log, waiver_db, app
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            os.path.abspath("creds.json"), scope
        )
        client = gspread.authorize(creds)
        user_db = client.open("User Database").sheet1  # Open the spreadhseet
        print("User Database Loaded")
        activity_log = client.open_by_url(
            "https://docs.google.com/spreadsheets/d/1aLBb1J2ifoUG2UAxHHbwxNO3KrIIWoI0pnZ14c5rpOM/edit?usp=drive_web&ouid=104398832910104737872"
        ).sheet1
        print("Activity Log Loaded")
        waiver_db = client.open("Waiver Signatures").sheet1
        print("Waiver Database Loaded")
    except:
        print("An ERROR has ocurred connecting to google sheets")

def setRFID(new_rfid):
    global rfid
    rfid = new_rfid
    
def setApp(new_app):
    global app
    app = new_app