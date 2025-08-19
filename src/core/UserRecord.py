import global_
import json
import logging
from datetime import datetime as dt

LOCAL_DB_PATH = "assets/user_db.json"

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
                    cleaned = extract_user_data(row)
                    return cls(uuid, cleaned)
        return None
    
    def find_payment(self, util) -> bool:
        try:
            if self.data.get("Last Paid Term") == util.get_current_term():
                return True
            
            if util.check_user_payment(self.data):
                self.data["Last Paid Term"] = util.get_current_term()
                return True
            else:
                logging.info("Returning false in UserRecord find_payment")
                return False
        except Exception as e:
            logging.error(f"Error when using UserRecord find_payment: {e}")
    
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
                logging.info(f"User {self.data.get('Name', 'Unknown')} succeeded UserRecord check_waiver_match.")
                self.data["Waiver Signed"] = "true"
                return True
        except Exception as e:
            logging.error(f"Error checking waiver status for user {self.data.get('Name', 'Unknown')}: {e}")
            if waiver_signed == "true":
                return True   
        logging.info(f"User {self.data.get('Name', 'Unknown')} failed UserRecord has_waiver.")
        return False         

    def needs_refresh(self):
        last_checked_in = self.data.get("lastCheckIn")
        if last_checked_in is None:
            return True
        waiver_signed = self.data.get("Waiver Signed", "").strip().lower()

        if not (last_checked_in or
                not self.data.get("firstEnrTrm") or
                not self.data.get("lastEnrTrm")):
            return True
        
        try:
            diff_days = (dt.today().date() - dt.strptime(last_checked_in, "%Y-%m-%d").date()).days
            if diff_days >= 21:
                return True
        except ValueError as e:
            logging.warning(f"Invalid lastCheckIn date format: {last_checked_in}")
            return True

        if waiver_signed in ["false", " "]:
            logging.info(f"User {self.data.get('Name', 'Unknown')} has no local waiver signed, needs refresh")
            return True
        
        return False

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

def extract_user_data(user_acc) -> dict:
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
        "Last Paid Term": user_acc.get("Last Paid Term", "")
    }