from tkinter import *
from gui import *
from swipe import *
from reader import *
from fabman import *
from sheets import *
from threading import Thread

def myLoop(app, reader):
    #time.sleep(0.1)
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

        user_db = sheet.getUserDB()
        user_data = user_db.get_all_records(numericise_ignore=["all"])

        # Get a list of all waiver signatures
        waiver_db = sheet.getWaiverDB()
        waiver_data = waiver_db.get_all_records(numericise_ignore=["all"])

        curr_user = "None"
        curr_user_w = "None"

        for i in user_data:
            if i["Card UUID"] == tag:
                curr_user = i
                        
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
            activity_log = sheet.getActivityLog()
            activity_log.append_row(new_row)
            welcome = app.get_frame(UserWelcome)
            welcome.displayName(curr_user["Name"])

        last_time = time.time()
        last_tag = tag

        reader.readSerial()
    

if __name__ == "__main__":
    fab = fabman()
    app = gui()
    sw = swipe(app)
    sheet = sheets()
    reader = Reader()
    util = utils(reader)
    thread = Thread(target=myLoop, args=(app, reader))
    thread.start()
    #app.title("Check-In")
    #app.geometry("1280x720")
    #TODO: Screen is gonna need to be set to 720p
    #app.attributes("-fullscreen", True)
    
    #TODO: Put logic here you goomba
    #This needs to have the scan logic, account creation and access
    #readerThread.run()
    #monitor(app, readerThread)

    app.bind("<Key>", lambda i: sw.keyboardPress(i))
    
    app.start()
    last_tag = 0
    last_time=0

    """
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
                    continue

                s_reason = reader.checkRFID(tag)

                if s_reason != "good":
                    print(s_reason)
                    continue
                else:
                    print("RFID Check Succeeded")

                user_db = sheet.getUserDB()
                user_data = user_db.get_all_records(numericise_ignore=["all"])

                # Get a list of all waiver signatures
                waiver_db = sheet.getWaiverDB()
                waiver_data = waiver_db.get_all_records(numericise_ignore=["all"])

                curr_user = "None"
                curr_user_w = "None"

                for i in user_data:
                    if i["Card UUID"] == tag:
                        curr_user = i
                        
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
                    activity_log = sheet.getActivityLog()
                    activity_log.append_row(new_row)
                    welcome = app.get_frame(UserWelcome)
                    welcome.displayName(curr_user["Name"])

                last_time = time.time()
                last_tag = tag

                reader.readSerial()
        """