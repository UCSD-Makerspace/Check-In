from datetime import datetime as dt
from tkinter import *
from gui import *
from checkin_queue import CheckInLogger
from reader import *
from swipe import swipe
from fabman import *
from sheets import *
from threading import Thread
from UserWelcome import *
from ManualFill import *
from CheckInNoId import *
from get_info_from_pid import contact_client
import global_
import json
import socket
import logging
import argparse
import serial.tools.list_ports as list_ports
from sys import stdout
from time import perf_counter

TRAFFIC_LIGHT_VID = 6790
READER_VID = 4292


def is_connected(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        return False


##############################################################
# This acts as the main loop of the program, ran in a thread #
##############################################################

no_wifi_shown = False


def myLoop(app, reader):
    global no_wifi_shown, no_wifi
    logging.info("Now reading ID cards")
    last_tag = 0
    last_time = 0
    # For looking up student info
    contact = contact_client()
    while True:
        time.sleep(0.1)
        in_waiting = reader.getSerInWaiting()
        tag = 0

        if in_waiting >= 14:
            if not is_connected():
                logging.info("ERROR wifi is not connected")
                if not no_wifi_shown:
                    no_wifi_shown = True
                    no_wifi = Label(
                        app.get_frame(MainPage),
                        text="ERROR! Connection cannot be established, please let staff know.",
                        font=("Arial", 25),
                    )
                    no_wifi.pack(pady=40)
                    no_wifi.after(4000, lambda: destroyNoWifiError(no_wifi))
                continue

            app.get_frame(ManualFill).clearEntries()
            tag_read_start = perf_counter()
            tag = reader.grabRFID()
            tag_read_end = perf_counter()

            if " " in tag:
                continue

            if tag == last_tag and not reader.canScanAgain(last_time):
                logging.debug("Suppressing repeat scan")
                continue

            s_reason = reader.checkRFID(tag)

            if s_reason != "good":
                logging.debug(s_reason)
                continue
            else:
                logging.debug("RFID Check Succeeded")

            global_.setRFID(tag)

            ##############################
            # Use local DB for user data #
            ##############################
            t0 = perf_counter()
            try:
                with open("assets/local_user_db.json", "r", encoding="utf-8") as f:
                    user_data = json.load(f)
            except FileNotFoundError:
                logging.error("Local user database not found. Please run export_user_db.py to create it.")
                continue 
            t1 = perf_counter()
            curr_user = user_data.get(tag, None)
            curr_user_w = "None"
            t2 = perf_counter()
            t3 = t4 = t5 = t6 = t7 = None

            ###################################
            # Case handling for user check-in #      
            ################################### 
            if curr_user:
                user_id = curr_user["Student ID"].strip().lower()
                waiver_signed = curr_user.get("Waiver Signed", "").strip().lower()
                firstEnrTrm = curr_user["firstEnrTrm"]
                lastEnrTrm = curr_user["lastEnrTrm"] 

                # Used to check if firstEnrTrm and lastEnrTrm are stale and need to be updated
                last_checked_in_str = curr_user.get("lastCheckIn")
                needs_refresh = False

                if last_checked_in_str:
                    last_checked_in_date = dt.strptime(last_checked_in_str, "%Y-%m-%d").date()
                    today = dt.today().date()
                    diff = (today - last_checked_in_date).days
                    if diff >= 21:
                        needs_refresh = True
                else:
                    # User has not checked in since local DB was created
                    needs_refresh = True

                if not curr_user.get("firstEnrTrm") or not curr_user.get("lastEnrTrm"):
                    needs_refresh = True

                waiver_updated = False

                if waiver_signed != "true":
                    logging.info("Waiver not found locally for " + curr_user["Name"]
                                + " with PID " + curr_user["Student ID"] + " at " + utils.getDatetime())
                    waiver_data = global_.sheets.get_waiver_db_data()
                    if utils.check_waiver_match(curr_user, waiver_data):
                        t4 = perf_counter()
                        logging.info("Waiver found online for " + curr_user["Name"])
                        curr_user["Waiver Signed"] = "true"
                        curr_user["Student ID"] = "A" + user_id.lstrip("a")
                        curr_user_w = "waiver_confirmed"
                        waiver_updated = True
                else:
                    logging.info("Account & waiver found locally for " + curr_user["Name"] + " at " + utils.getDatetime())
                    curr_user_w = "waiver_confirmed"

                if needs_refresh:
                    logging.info("Updating firstEnrTrm and lastEnrTrm for " + curr_user["Name"])
                    t5 = perf_counter()
                    student_info = contact.get_student_info_pid("A" + user_id.lstrip("a"))
                    t6 = perf_counter()
                    if student_info:
                        curr_user["firstEnrTrm"] = student_info[4]
                        curr_user["lastEnrTrm"] = student_info[5]
                    curr_user["lastCheckIn"] = dt.today().strftime("%Y-%m-%d")

                # Writing conditions: Either we update enrolled terms or local waiver status
                if waiver_updated or needs_refresh:
                    user_data[tag] = curr_user
                    with open("assets/local_user_db.json", "w", encoding="utf-8") as f:
                        json.dump(user_data, f, indent=2)

            # If user is not found locally, check the online user DB.
            # If found online, check waiver status and append both to local DB.
            # Else, redirect user to usual account creation page
            else:
                logging.info("User not found in local DB, checking with online database")
                user_data_online = global_.sheets.get_user_db_data()
                t3 = perf_counter()
                waiver_data = global_.sheets.get_waiver_db_data()
                for i in user_data_online:
                    if i["Card UUID"] == tag:
                        curr_user = i
                        user_id = curr_user["Student ID"].lower()
                        break
                if curr_user and utils.check_waiver_match(curr_user, waiver_data):
                    logging.info(f"User found online: {curr_user['Name']} but not locally at " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    
                    # Write user to local database if we find the user online but not locally
                    user_data[tag] = {
                        "Name": curr_user["Name"],
                        "Student ID": "A" + user_id.lstrip("a"),
                        "Email Address": curr_user["Email Address"],
                        "Waiver Signed": "true",
                    }

                    with open("assets/local_user_db.json", "w", encoding="utf-8") as f:
                        json.dump(user_data, f, indent=2)
                    curr_user_w = "waiver_confirmed"
                    logging.info(f"Updated local DB with user: {curr_user['Name']}")  

            if curr_user is None and curr_user_w == "None":
                logging.info("User was not found in online database")
                global_.traffic_light.set_red()
                app.show_frame(NoAccNoWaiver)
                app.after(3000, lambda: app.show_frame(NoAccNoWaiverSwipe))
            elif curr_user_w == "None":
                logging.info("User does not have waiver")
                global_.traffic_light.set_yellow()
                app.show_frame(AccNoWaiver)
                app.after(3000, lambda: app.show_frame(AccNoWaiverSwipe))
            elif curr_user is None:
                logging.info("User has a waiver but no account")
                app.show_frame(WaiverNoAcc)
                app.after(3000, lambda: app.show_frame(WaiverNoAccSwipe))
            else:
                new_row = [
                    util.getDatetime(),
                    int(time.time()),
                    curr_user["Name"],
                    str(tag),
                    "User Check-In",
                    "Main Check-In",
                    firstEnrTrm,
                    lastEnrTrm, 
                ]
                # Add to check-in queue
                t7 = perf_counter()
                global_.checkin_logger.enqueue_row(new_row, tag)
                global_.traffic_light.set_green()
                global_.app.get_frame(UserWelcome).displayName(curr_user["Name"])

                ###############
                # TIMING LOGS #
                ###############
                logging.info("[TIMING BREAKDOWN]")
                logging.info(f"RFID read time: {tag_read_end - tag_read_start:.4f}s")
                logging.info(f"Load local_user_db.json: {t1 - t0:.4f}s")
                logging.info(f"Local user lookup: {t2 - t1:.4f}s")
                if t3 is not None and t4 is not None:
                    logging.info(f"Online waiver check: {t4 - t3:.4f}s")
                if t5 is not None and t6 is not None:
                    logging.info(f"Student info API call: {t6 - t5:.4f}s")
                if t6 is not None and t7 is not None:
                    logging.info(f"Enqueue + display: {t7 - t6:.4f}s")
                elif t2 is not None and t7 is not None:
                    logging.info(f"Total check-in time (no API): {t7 - tag_read_start:.4f}s")
                logging.info(f"Total time from RFID scan to display: {t7 - tag_read_start:.4f}s")

            last_time = time.time()
            last_tag = tag

            reader.readSerial()


def destroyNoWifiError(no_wifi):
    global no_wifi_shown
    no_wifi.destroy()
    no_wifi_shown = False


def clearAndReturn():
    global_.traffic_light.set_off()
    global_.app.show_frame(MainPage)
    global_.app.get_frame(ManualFill).clearEntries()
    global_.app.get_frame(CheckInNoId).clearEntries()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Makerspace Check-in System",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Increase verbosity (print debug info)",
    )

    args = parser.parse_args()
    config = vars(args)

    if config["verbose"]:
        logging.basicConfig(level=logging.DEBUG, stream=stdout)
    else:
        logging.basicConfig(level=logging.INFO)

    ports = list(serial.tools.list_ports.comports())
    reader_usb_id = None
    traffic_usb_id = None

    for p in ports:
        if p.vid == READER_VID:
            reader_usb_id = p.device
        elif p.vid == TRAFFIC_LIGHT_VID:
            traffic_usb_id = p.device

    global_.init(traffic_usb_id)
    app = gui()
    global_.setApp(app)
    global_.traffic_light.set_off()
    global_.checkin_logger = CheckInLogger()
    sw = swipe()
    reader = Reader(reader_usb_id)
    util = utils()
    thread = Thread(target=myLoop, args=(app, reader))
    logging.info("Starting thread")
    thread.start()
    app.bind("<Key>", lambda i: sw.keyboardPress(i))
    app.bind("<Escape>", lambda i: clearAndReturn())
    logging.info("Made it to app start")
    app.start()