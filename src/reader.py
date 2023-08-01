from threading import Thread
from os.path import exists
from datetime import datetime

#from sheets import sheets
#from utils import *
#from MainPage import MainPage
#from NoAccNoWaiver import *
#from UserThank import *
#from AccNoWaiver import *

import tkinter
import serial
import time
import traceback
import requests

expected_characters = 14
timeout = 1

class Reader(Thread):
    def __init__(self):
        super().__init__()
        #self.newFob = False
        #self.tag = ""
        #self.lastTag = ""
        #self.lastTime = 0
        self.tty = ""
        self.loadScanner()
        self.ser = serial.Serial(self.tty, 115200)
        print("reader __init__ finished")
    
    def loadScanner(self):
        file_exists = exists("/dev/ttyUSB0")
        if file_exists:
            self.tty = "/dev/ttyUSB0"
        else:
            print("Scanner not connected")
            quit()


    def getSerInWaiting(self):
        return self.ser.in_waiting
    
    def readSerial(self):
        self.ser.read(self.ser.in_waiting)
    
    """
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

                user_db = self.sheet.getUserDB()
                user_data = user_db.get_all_records(numericise_ignore=["all"])

                # Get a list of all waiver signatures
                waiver_db = self.sheet.getWaiverDB()
                waiver_data = waiver_db.get_all_records(numericise_ignore=["all"])

                curr_user = "None"
                curr_user_w = "None"

                for i in user_data:
                    if i["Card UUID"] == self.tag:
                        curr_user = i
                        
                for i in waiver_data:
                    if i["Name"] == curr_user["Name"]:
                        curr_user_w = i

                if curr_user == "None" and curr_user_w == "None":
                    print("User was not found in the database")
                    self.app.show_frame(NoAccNoWaiver)
                    self.app.after(2000, lambda: self.app.show_frame(NoAccNoWaiverSwipe))
                    #global need_tag
                    #need_tag = str(self.tag)
                elif curr_user_w == "None":
                    print("User does not have waiver")
                    self.app.show_frame(AccNoWaiver)
                    self.app.after(2000, lambda: self.app.show_frame(AccNoWaiverSwipe))
                elif curr_user == "None":
                    print("User has a waiver but no account")
                    self.app.show_frame(WaiverNoAcc)
                    self.app.after(2000, lambda: self.app.show_frame(WaiverNoAccSwipe))
                else:
                    new_row = [utils.getDatetime(), int(time.time()), curr_user["Name"], str(self.tag), "User Checkin", "", "", ""]

                    #infoLabel.destroy()
                    activity_log = self.sheet.getActivityLog()
                    activity_log.append_row(new_row)
                    UserWelcome.displayName(curr_user["Name"])

                self.newFob = True
                self.lastTime = time.time()
                self.lastTag = self.tag

                self.ser.read(self.ser.in_waiting)
            """
    
    def grabRFID(self):
        print("RFID data incoming. Bytes in waiting: " + str(self.ser.in_waiting))
        tagBytes = self.ser.read(14)
        self.ser.read(self.ser.in_waiting)
        RFID = tagBytes.decode().replace("\r\n", "")
        print("Parsed tag: " + RFID)
        return str(RFID)
    
    def checkWifi(self):
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
    
    def canScanAgain(self, lastTime):
        return time.time() - lastTime > 3
    
    def getRFID(self):
        return self.tag
