import global_
import json
import logging
from datetime import datetime as dt
from core.write_checkin import write_checkin
from core.new_row_check_in import new_row_check_in
from gui import *
from reader import *

LOCAL_DB_PATH = "assets/local_user_db.json"

def handle_check_in(tag, contact, util):
    """ Handles the check-in process for a user based on their tag.
    It checks the local user database first, then the online database if not found locally.
    Updates the local waiver status and enrolled terms as necessary. """

    with open(LOCAL_DB_PATH, "r", encoding="utf-8") as f:
        user_data = json.load(f)

    curr_user = user_data.get(tag, None)
    curr_user_w = "None"

    ##### If user is not found locally, scan online and update user_data #####
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
            
            user_data[tag] = extract_user_data(curr_user, tag)
            logging.info(f"Extracted user data: {user_data[tag]}")
            dump_json(user_data)
            curr_user_w = "waiver_confirmed"
            logging.info(f"Updated local DB with user: {curr_user['Name']}")  
        else:
            logging.info("User not found in local or online database")
            new_row_check_in(None, "None", tag, util, "", "")
            return
    
    ##### Main case: User is found in local database #####
    user_id = curr_user["Student ID"].strip().lower()
    firstEnrTrm = curr_user.get("firstEnrTrm")
    lastEnrTrm = curr_user.get("lastEnrTrm")
    needs_refresh = False

    # Determine if local data needs to be refreshed #
    last_checked_in_str = curr_user.get("lastCheckIn")

    if not last_checked_in_str or not firstEnrTrm or not lastEnrTrm:
        needs_refresh = True
    elif (dt.today().date() - dt.strptime(last_checked_in_str, "%Y-%m-%d").date()).days >= 21:
        needs_refresh = True

    has_waiver, waiver_updated = check_waiver_status(curr_user, util)
    if has_waiver:
        curr_user_w = "waiver_confirmed"
    if waiver_updated:
        needs_refresh = True

    if needs_refresh:
        logging.info("Updating local info for " + curr_user["Name"])
        refresh_user_terms(curr_user, contact)

        cleaned = extract_user_data(curr_user, tag)
        cleaned["firstEnrTrm"] = curr_user.get("firstEnrTrm", "")
        cleaned["lastEnrTrm"] = curr_user.get("lastEnrTrm", "")
        cleaned["lastCheckIn"] = curr_user.get("lastCheckIn", None)

        user_data[tag] = cleaned
        dump_json(user_data)
        curr_user = cleaned

    new_row_check_in(curr_user, curr_user_w, tag, util, firstEnrTrm, lastEnrTrm)
    write_checkin(curr_user, tag)

########### Helper Functions ###########
def dump_json(user_data):
    with open(LOCAL_DB_PATH, "w", encoding="utf-8") as f:
        json.dump(user_data, f, indent=2)

def refresh_user_terms(curr_user, contact):
    user_id = curr_user["Student ID"].strip().lower().lstrip("aA")
    student_info = contact.get_student_info_pid("A" + user_id)
    if student_info:
        curr_user["firstEnrTrm"] = student_info[4]
        curr_user["lastEnrTrm"] = student_info[5]
    curr_user["lastCheckIn"] = dt.today().strftime("%Y-%m-%d")

def extract_user_data(online_user, tag):
    user_id = online_user["Student ID"].lower()
    return {
        "Name": online_user["Name"],
        "Timestamp": online_user["Timestamp"],
        "Student ID": "A" + user_id.strip().lstrip("aA"),
        "Email Address": online_user["Email Address"],
        "Waiver Signed": "true",
        "firstEnrTrm": "",
        "lastEnrTrm": "",
        "lastCheckIn": None,
    }

def check_waiver_status(curr_user, util) -> tuple[bool,bool]:
    """ 
    Checks if curr_user has a waiver.
    Returns (has_waiver, waiver_updated), where:
    - has_waiver: True if waiver is found locally or online
    - waiver_updated: True only if we just updated the waiver from online
    """
    waiver_status = curr_user.get("Waiver Signed", "").strip().lower()
    if waiver_status != "true":
        logging.info("Waiver not found locally for " + curr_user["Name"] + " " + curr_user["Student ID"] + " at " + util.getDatetime())
        waiver_data = global_.sheets.get_waiver_db_data()
        if util.check_waiver_match(curr_user, waiver_data):
            logging.info("Waiver found online for " + curr_user["Name"])
            curr_user["Waiver Signed"] = "true" 
            return True, True
        return False, False
    else:
        logging.info("Account & waiver found locally for " + curr_user["Name"] + " at " + util.getDatetime())
        return True, False