import global_
import logging
from datetime import datetime as dt


class UserRecord():
    def __init__(self, uuid: str, data: dict):
        self.uuid = uuid
        self.data = data

    @classmethod
    def load(cls, uuid, sheets):
        row = sheets.get_user_by_card(uuid)
        if row is None:
            return None
        record = cls(uuid, extract_user_data(row))
        logging.info(f"User found: {record.data['Name']}")
        return record

    def has_waiver(self):
        try:
            return global_.sheets.check_waiver(self.data["Student ID"], self.data["Email Address"])
        except Exception as e:
            logging.error(f"Error checking waiver for {self.data.get('Name', 'Unknown')}: {e}")
            return False

    def update_terms(self, contact):
        refresh_user_terms(self.data, contact)


########### Helper Functions ###########
def refresh_user_terms(curr_user, contact):
    user_id = curr_user["Student ID"].strip().lower().lstrip("a")
    student_info = contact.get_student_info_pid("A" + user_id)
    if student_info:
        curr_user["firstEnrTrm"] = student_info[4]
        curr_user["lastEnrTrm"] = student_info[5]

def extract_user_data(row) -> dict:
    user_id = row["Student ID"].lower()
    return {
        "Name": row["Name"],
        "Timestamp": row["Timestamp"],
        "Student ID": "A" + user_id.strip().lstrip("a"),
        "Email Address": row["Email Address"],
        "firstEnrTrm": row.get("firstEnrTrm", ""),
        "lastEnrTrm": row.get("lastEnrTrm", ""),
    }
