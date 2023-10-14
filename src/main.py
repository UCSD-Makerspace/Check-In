from tkinter import *
from gui import *
from swipe import *
from reader import *
from fabman import *
from sheets import *
from threading import Thread
from UserWelcome import *
from ManualFill import *
import global_
import socket
import tkinter

debug = 0

def is_connected():
    try:
        # Attempt to resolve a common hostname
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

##############################################################
# This acts as the main loop of the program, ran in a thread #
##############################################################

no_wifi_shown = False

def myLoop(app, reader):
    global no_wifi_shown, no_wifi
    print("Now reading ID Card")
    last_tag = 0
    last_time = 0
    while True:
        time.sleep(0.1)
        in_waiting = reader.getSerInWaiting()
        tag = 0
        if in_waiting >= 14:
            if not is_connected():
                print("ERROR wifi is not connected")
                no_wifi_shown=True
                no_wifi = Label(app.get_frame(MainPage), text="ERROR, connection cannot be established, please let staff know.")
                no_wifi.pack(pady=40)
                no_wifi.after(4000, lambda: destroyNoWifiError(no_wifi))
            app.get_frame(ManualFill).clearEntries()
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
            user_data = global_.sheets.get_user_db_data()
            
            # Get a list of all waiver signatures
            waiver_data = global_.sheets.get_waiver_db_data()

            curr_user = "None"
            curr_user_w = "None"

            for i in user_data:
                if i["Card UUID"] == tag:
                    curr_user = i
            
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
                activity_log = global_.sheets.get_activity_db()
                activity_log.append_row(new_row)
                global_.app.get_frame(UserWelcome).displayName(curr_user["Name"])

            last_time = time.time()
            last_tag = tag

            reader.readSerial()
    
    
def destroyNoWifiError(no_wifi):
    global no_wifi_shown
    no_wifi.destroy()
    no_wifi_shown = False

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