import global_
import json
import logging
from datetime import datetime as dt
from time import perf_counter
from new_row_check_in import new_row_check_in
from gui import *
from reader import *
from render_ports import get_usb_ids

def handle_check_in(tag, contact, util):
    """
    Handles the check-in process for a user based on their tag.
    It checks the local user database first, then the online database if not found locally.
    Updates the waiver status and enrolled terms as necessary.
    """

    with open("assets/local_user_db.json", "r", encoding="utf-8") as f:
        user_data = json.load(f)

    curr_user = user_data.get(tag, None)
    curr_user_w = "None"

    ##################################################################
    # If user is not found locally, scan online and update user_data #
    ##################################################################
    if not curr_user:
        logging.info("User not found in local DB, checking with online database")
        user_data_online = global_.sheets.get_user_db_data()
        waiver_data = global_.sheets.get_waiver_db_data()
        for i in user_data_online:
            if i["Card UUID"] == tag:
                curr_user = i
                user_id = curr_user["Student ID"].lower()
                break

        if curr_user and util.check_waiver_match(curr_user, waiver_data):
            logging.info(f"User found online: {curr_user['Name']} but not locally at " + util.getDatetime())
            
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
    
    ##############################################
    # Main case: User is found in local database #
    ##############################################
    user_id = curr_user["Student ID"].strip().lower()
    waiver_signed = curr_user.get("Waiver Signed", "").strip().lower()
    firstEnrTrm = curr_user["firstEnrTrm"]
    lastEnrTrm = curr_user["lastEnrTrm"] 

    # Used to check if firstEnrTrm and lastEnrTrm are stale and need to be updated
    last_checked_in_str = curr_user.get("lastCheckIn")
    needs_refresh = False
    
    ##### Check if local user data needs to be refreshed #####
    if not last_checked_in_str:
        needs_refresh = True

    last_checked_in_date = dt.strptime(last_checked_in_str, "%Y-%m-%d").date()
    today = dt.today().date()
    diff = (today - last_checked_in_date).days
    if diff >= 21:
        needs_refresh = True

    if not curr_user.get("firstEnrTrm") or not curr_user.get("lastEnrTrm"):
        needs_refresh = True

    waiver_updated = False

    if waiver_signed != "true":
        logging.info("Waiver not found locally for " + curr_user["Name"]
                    + " with PID " + curr_user["Student ID"] + " at " + util.getDatetime())
        waiver_data = global_.sheets.get_waiver_db_data()
        if util.check_waiver_match(curr_user, waiver_data):
            t4 = perf_counter()
            logging.info("Waiver found online for " + curr_user["Name"])
            curr_user["Waiver Signed"] = "true"
            curr_user["Student ID"] = "A" + user_id.lstrip("a")
            curr_user_w = "waiver_confirmed"
            waiver_updated = True
    else:
        logging.info("Account & waiver found locally for " + curr_user["Name"] + " at " + util.getDatetime())
        curr_user_w = "waiver_confirmed"

    if needs_refresh:
        logging.info("Updating firstEnrTrm and lastEnrTrm for " + curr_user["Name"])
        student_info = contact.get_student_info_pid("A" + user_id.lstrip("aA"))
        if student_info:
            curr_user["firstEnrTrm"] = student_info[4]
            curr_user["lastEnrTrm"] = student_info[5]
        curr_user["lastCheckIn"] = dt.today().strftime("%Y-%m-%d")

    # Writing conditions: Either we update enrolled terms or local waiver status
    if waiver_updated or needs_refresh:
        user_data[tag] = curr_user
        with open("assets/local_user_db.json", "w", encoding="utf-8") as f:
            json.dump(user_data, f, indent=2)

    new_row_check_in(curr_user, curr_user_w, tag, util, firstEnrTrm, lastEnrTrm)

