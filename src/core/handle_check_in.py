import global_
import json
import logging
from datetime import datetime as dt
from core.write_checkin import write_checkin
from core.new_row_check_in import new_row_check_in
from core.UserRecord import *
from gui import *
from reader import *

LOCAL_DB_PATH = "assets/local_user_db.json"

def handle_check_in(tag, contact, util):
    """ Handles the check-in process for a user based on their tag.
    It checks the local user database first, then the online database if not found locally.
    Updates the local waiver status and enrolled terms as necessary. """

    with open(LOCAL_DB_PATH, "r", encoding="utf-8") as f:
        user_data = json.load(f)

    curr_user = UserRecord.load_from_local(tag, user_data)
    waiver_status = "None"

    if not curr_user:
        logging.info(f"User with tag {tag} not found locally. Checking online...")
        curr_user = UserRecord.load_from_online(tag, global_.sheets, util)
        if curr_user:
            waiver_status = "waiver_confirmed"
            curr_user.save(user_data)
            dump_json(user_data)
            logging.info(f"User added from online to local database: {curr_user.data['Name']}")
        if not curr_user:
            logging.info(f"User {tag} not found locally or online.")
            new_row_check_in(None, "None", tag, util, None, None)
            return

    if curr_user.has_waiver(util):
        waiver_status = "waiver_confirmed"

    if curr_user.needs_refresh():
        logging.info(f"Refreshing terms and last check-in for user {curr_user.data['Name']}")
        curr_user.update_terms(contact)
        curr_user.save(user_data)
        dump_json(user_data)

    new_row_check_in(curr_user.data, waiver_status, tag, util, curr_user.data.get("firstEnrTrm"), curr_user.data.get("lastEnrTrm"))
    write_checkin(curr_user.data, tag)

# Helper function
def dump_json(user_data):
    with open(LOCAL_DB_PATH, "w", encoding="utf-8") as f:
        json.dump(user_data, f, indent=2)