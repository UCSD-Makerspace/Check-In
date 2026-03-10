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


########### Helper Functions ###########
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
