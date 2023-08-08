from tkinter import *
from gui import *
from swipe import *
from reader import *
from fabman import *
from sheets import *
from threading import Thread
from UserWelcome import *
import global_

debug = 0

##############################################################
# This acts as the main loop of the program, ran in a thread #
##############################################################
def myLoop(app, reader):
    print("Now reading ID Card")
    last_tag = 0
    last_time = 0
    while True:
        time.sleep(0.1)
        in_waiting = reader.getSerInWaiting()
        tag = 0
        if in_waiting >= 14:
            tag = reader.grabRFID()
            if tag == last_tag and not reader.canScanAgain(last_time):
                print("Suppressing repeat scan")
                continue

            s_reason = reader.checkRFID(tag)

            if s_reason != "good":
                print(s_reason)
                continue
            else:
                print("RFID Check Succeeded")
                
            global_.setRFID(tag)

            # Get a list of all users
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

            #TODO
            #print("TESTING: " + curr_user)
            
            if curr_user != "None" :
                for i in waiver_data:
                    user_id = i["A_Number"]
                    waiver_id = curr_user["Student ID"]
                    
                    #TODO
                    print(waiver_id + "=" + user_id)
                        
                    if (user_id[0] == "A") or (user_id[0] == "a"):
                        user_id = user_id[1:]
                        
                    if (waiver_id[0] == "A") or (waiver_id[0] == "a"):
                        waiver_id = waiver_id[1:]  
                            
                    if user_id == waiver_id:
                        curr_user_w = i
                        
            ############################     
            # All scenarios for ID tap #
            ############################
            if curr_user == "None" and curr_user_w == "None":
                print("User was not found in the database")
                app.show_frame(NoAccNoWaiver)
                app.after(4000, lambda: app.show_frame(NoAccNoWaiverSwipe))
            elif curr_user_w == "None":
                print("User does not have waiver")
                app.show_frame(AccNoWaiver)
                app.after(4000, lambda: app.show_frame(AccNoWaiverSwipe))
            elif curr_user == "None":
                print("User has a waiver but no account")
                app.show_frame(WaiverNoAcc)
                app.after(4000, lambda: app.show_frame(WaiverNoAccSwipe))
            else:
                new_row = [util.getDatetime(), int(time.time()), curr_user["Name"], str(tag), "User Checkin", "", "", ""]
                activity_log = global_.activity_log
                activity_log.append_row(new_row)
                global_.app.get_frame(UserWelcome).displayName(curr_user["Name"])

            last_time = time.time()
            last_tag = tag

            reader.readSerial()
    
    
def clearAndReturn():
    global_.app.show_frame(MainPage)
    global_.app.get_frame(ManualFill).clearEntries()
    
if __name__ == "__main__":
    global_.init()
    app = gui()
    global_.setApp(app)
    sw = swipe()
    reader = Reader()
    util = utils()
    thread = Thread(target=myLoop, args=(app, reader))
    print("Starting thread")
    thread.start()
    app.bind("<Key>", lambda i: sw.keyboardPress(i))
    app.bind("<Escape>", lambda i: clearAndReturn())
    print("Made it to app start")
    app.start()