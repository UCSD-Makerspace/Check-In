from threading import Thread
from os.path import exists
from datetime import datetime

from sheets import sheets
from utils import *
from MainPage import MainPage

import tkinter
import serial
import time
import traceback
import requests

expected_characters = 14
timeout = 1

class Reader(Thread):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.newFob = False
        self.tag = ""
        self.lastTag = ""
        self.counter = 0
        self.lastTime = 0
        self.tty = ""
        self.loadScanner()
        self.ser = serial.Serial(self.tty, 115200)
        print("reader __init__ finished")
        
        if self.checkWifi():
            self.sheet = sheets()
    
    def loadScanner(self):
        file_exists = exists("/dev/ttyUSB0")
        if file_exists:
            self.tty = "/dev/ttyUSB0"
        else:
            print("Scanner not connected")
            quit()

    def run(self):
        print("starting thread2")
        while True:
            time.sleep(0.1)
            if self.ser.in_waiting >= 14:
                # TODO: Wifi check doesn't work

                self.tag = self.grabRFID()

                if self.tag == self.lastTag and not self.canScanAgain(self.lastTime):
                    # if not canScanAgain(self.lastTime): #This do not work
                    print("Suppressing repeat scan")
                    continue

                s_reason = self.checkRFID(self.tag)

                if s_reason != "good":
                    print(s_reason)
                    continue
                else:
                    print("RFID Check Succeeded")

                
                infoLabel = tkinter.Label(
                    self.app.get_frame(MainPage),
                    text="Card read, please wait...",
                    font=("", 24),
                )
                infoLabel.pack(pady=20)

                # Get a list of all records
                user_db = sheets.getUserDB()
                user_data = user_db.get_all_records(numericise_ignore=["all"])

                # Get a list of all waiver signatures
                waiver_db = sheets.getWaiverDB
                waiver_data = waiver_db.get_all_records(numericise_ignore=["all"])

                curr_user = "None"

                for i in user_data:
                    if i["Card UUID"] == self.tag:
                        curr_user = i

                if curr_user == "None":
                    infoLabel.destroy()
                    print("User was not found in the database")
                    global need_tag
                    need_tag = str(self.tag)
                    #self.app.show_frame(swipePage)
                else:
                    new_row = [
                        utils.getDatetime(),
                        int(time.time()),
                        curr_user["Name"],
                        str(self.tag),
                        "User Checkin",
                        "",
                        "",
                        "",
                    ]

                    no_id = False
                    found = False

                    print(curr_user)

                    for i in waiver_data:
                        if str(i["A_Number"])[1:] == str(curr_user["Student ID"])[1:]:
                            found = True
                            print("User " + curr_user["Name"] + " was found")

                    if curr_user["Student ID"] == "":
                        print(f"Error: {curr_user['Name']}, does not have an ID")
                        no_id = True

                    if not found:
                        #TODO:
                        #I don't think this is needed anymore
                        infoLabel.destroy()
                        #displayQRCode(curr_user["Name"])
                    elif no_id:
                        infoLabel.destroy()
                        self.displayNoID(curr_user["Name"])
                    else:
                        infoLabel.destroy()
                        activity_log = sheets.getActivityLog()
                        activity_log.append_row(new_row)
                        self.displayThankYou(curr_user["Name"])

                self.newFob = True
                self.lastTime = time.time()
                self.lastTag = self.tag

                self.ser.read(self.ser.in_waiting)
    
    def grabRFID(self):
        print("RFID data incoming. Bytes in waiting: " + str(self.ser.in_waiting))
        tagBytes = self.ser.read(14)
        self.ser.read(self.ser.in_waiting)
        RFID = tagBytes.decode().replace("\r\n", "")
        print("Parsed tag: " + RFID)
        return str(RFID)
    
    def checkWifi():
        try:
            requests.head("http://www.google.com/", timeout=timeout)
            return 1
        except requests.ConnectionError:
            return 
        
    def checkRFID(self, tag):
        if self.ser.in_waiting >= expected_characters:
            second_tag = self.grabRFID()
            print(f"Comparing {tag} and {second_tag}")
            if tag != second_tag:
                reason = "The two scanned tags did not match"
        elif len(tag) != expected_characters:
            reason = "Tag was not the expected number of chars"
        else:
            reason = "good"

        return reason
    
    def canScanAgain(lastTime):
        return time.time() - lastTime > 3
    
    def displayThankYou(name):
        #TODO: Needs to switch frames
        #      display the name of the user 
        #      then switch back to main page
        
        #OLD CODE
        """
        thank_check = Label(
            app.get_frame(mainPage),
            text=name + ", thank you for checking in!",
            font=("", 36),
        )
        thank_check.pack()
        thank_check.after(3000, lambda: thank_check.destroy())
        """
    
    def displayNoID(name):
        #TODO
        #Not sure if this is still needed
        
        #OLD CODE
        """
        need_id = Label(
            app.get_frame(mainPage),
            text=name + ", Please let a staff know that your account has no PID!",
            font=("", 24),
        )
        need_id.pack()
        need_id.after(8000, lambda: need_id.destroy())
        """