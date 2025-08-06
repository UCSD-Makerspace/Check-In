import global_
import json
import logging
from datetime import datetime as dt

LOCAL_DB_PATH = "assets/local_user_db.json"

class UserRecord():
    def __init__(self, uuid: str, data: dict):
        self.uuid = uuid
        self.data = data

    @classmethod
    def load_from_local(cls, uuid, user_db):
        user_data = user_db.get(uuid, None)
        return cls(uuid, user_data) if user_data else None
    
    @classmethod
    def load_from_online(cls, uuid, sheets, util):
        for row in sheets.get_user_db_data():
            if row["Card UUID"] == uuid:
                if util.check_waiver_match(row, sheets.get_waiver_db_data()):
                    logging.info(f"User found online: {row['Name']} but not locally at " + util.getDatetime())
                    cleaned = extract_user_data(row, uuid)
                    return cls(uuid, cleaned)
        return None
    
    def has_waiver(self, util):
        waiver_signed = self.data.get("Waiver Signed", "").strip().lower()
        if waiver_signed == "true":
            return True
        
        try:    
            waiver_data = global_.sheets.get_waiver_db_data()
            if not waiver_data:
                logging.warning("Waiver data is empty or None, cannot check waiver status in UserRecord.py")
                if waiver_signed in ["false", ""]:
                    return False
                logging.warning(f"Unknown local waiver status: {waiver_signed}")
                return False
            if util.check_waiver_match(self.data, waiver_data):
                self.data["Waiver Signed"] = "true"
                return True
        except Exception as e:
            logging.error(f"Error checking waiver status for user {self.data.get('Name', 'Unknown')}: {e}")
            if waiver_signed == "true":
                return True            

    def needs_refresh(self):
        last_checked_in = self.data.get("lastCheckIn")
        if not last_checked_in or not self.data.get("firstEnrTrm") or not self.data.get("lastEnrTrm") or self.data.get("Waiver Signed") == "false" or self.data.get("Waiver Signed") == " ":
            return True
        diff_days = (dt.today().date() - dt.strptime(last_checked_in, "%Y-%m-%d").date()).days
        return diff_days >= 21

    def update_terms(self, contact):
        refresh_user_terms(self.data, contact)

    def save(self, user_db):
        user_db[self.uuid] = self.data
                
########### Helper Functions ###########
def refresh_user_terms(curr_user, contact):
    user_id = curr_user["Student ID"].strip().lower().lstrip("aA")
    student_info = contact.get_student_info_pid("A" + user_id)
    if student_info:
        curr_user["firstEnrTrm"] = student_info[4]
        curr_user["lastEnrTrm"] = student_info[5]
    curr_user["lastCheckIn"] = dt.today().strftime("%Y-%m-%d")

def extract_user_data(user_acc, tag) -> dict:
    user_id = user_acc["Student ID"].lower()
    return {
        "Name": user_acc["Name"],
        "Timestamp": user_acc["Timestamp"],
        "Student ID": "A" + user_id.strip().lstrip("aA"),
        "Email Address": user_acc["Email Address"],
        "Waiver Signed": "true",
        "firstEnrTrm": user_acc.get("firstEnrTrm", ""),
        "lastEnrTrm": user_acc.get("lastEnrTrm", ""),
        "lastCheckIn": None,
    }