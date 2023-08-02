from tkinter import *
from gui import *
from swipe import *
from reader import *
from fabman import *
from sheets import *
from threading import Thread
import global_

debug = 0

def myLoop(app, reader):
    print("Now reading ID Card")
    last_tag = 0
    last_time = 0
    while True:
        time.sleep(0.1)
        in_waiting = reader.getSerInWaiting()
        tag = 0
        if in_waiting >= 14:
            # TODO: Wifi check doesn't work

            tag = reader.grabRFID()
            
            if tag == last_tag and not reader.canScanAgain(last_time):
                # if not canScanAgain(self.lastTime): #This do not work
                print("Suppressing repeat scan")
                return

            s_reason = reader.checkRFID(tag)

            if s_reason != "good":
                print(s_reason)
                return
            else:
                print("RFID Check Succeeded")
                
            global_.setRFID(tag)

            user_db = global_.user_db
            user_data = user_db.get_all_records(numericise_ignore=["all"])

            # Get a list of all waiver signatures
            waiver_db = global_.waiver_db
            waiver_data = waiver_db.get_all_records(numericise_ignore=["all"])

            curr_user = "None"
            curr_user_w = "None"

            for i in user_data:
                if i["Card UUID"] == tag:
                    curr_user = i
            
            if curr_user != "None":
                for i in waiver_data:
                    if i["Name"] == curr_user["Name"]:
                        curr_user_w = i

            if curr_user == "None" and curr_user_w == "None":
                print("User was not found in the database")
                app.show_frame(NoAccNoWaiver)
                app.after(2000, lambda: app.show_frame(NoAccNoWaiverSwipe))
                #global need_tag
                #need_tag = str(self.tag)
            elif curr_user_w == "None":
                print("User does not have waiver")
                app.show_frame(AccNoWaiver)
                app.after(2000, lambda: app.show_frame(AccNoWaiverSwipe))
            elif curr_user == "None":
                print("User has a waiver but no account")
                app.show_frame(WaiverNoAcc)
                app.after(2000, lambda: app.show_frame(WaiverNoAccSwipe))
            else:
                new_row = [util.getDatetime(), int(time.time()), curr_user["Name"], str(tag), "User Checkin", "", "", ""]

                #infoLabel.destroy()
                activity_log = global_.activity_log
                activity_log.append_row(new_row)
                global_.app.get_frame(UserWelcome).displayName(curr_user["Name"])

            last_time = time.time()
            last_tag = tag

            reader.readSerial()
    

if __name__ == "__main__":
    global_.init()
    app = gui()
    global_.setApp(app)
    sw = swipe()
    reader = Reader()
    #sheet = sheets()
    util = utils()
    thread = Thread(target=myLoop, args=(app, reader))
    print("Starting thread")
    thread.start()

    #TODO: Screen is gonna need to be set to 720p
    #app.attributes("-fullscreen", True)

    #monitor(app, readerThread)

    app.bind("<Key>", lambda i: sw.keyboardPress(i))
    print("Made it to app start")
    app.start()