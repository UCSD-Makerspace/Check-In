import json
import logging
import os

from sheets import SheetManager

EXPORT_PATH = os.path.join(os.path.dirname(__file__), "assets", "local_user_db.json")

def export_user_db():
    try:
        os.makedirs(os.path.dirname(EXPORT_PATH), exist_ok=True)

        sheet_manager = SheetManager()
        raw_data = sheet_manager.get_user_db_data(force_update=True)
        print(f"Length of raw data: {len(raw_data)}")

        user_data  = {}
        for row in raw_data:
            card_uuid = row.get("Card UUID", "")
            if not card_uuid:
                continue  # Skip entries with no UUID
            user_data[card_uuid] = {
                "Name": row.get("Name", ""),
                "Timestamp": row.get("Timestamp", ""),
                "Student ID": row.get("Student ID", ""),
                "Email Address": row.get("Email Address", ""),
                "Waiver Signed": row.get("Waiver Signed?", ""),
            }
        print(f"Length of user data: {len(user_data)}")

        print(f"Writing to: {os.path.abspath(EXPORT_PATH)}")
        with open(EXPORT_PATH, "w", encoding="utf-8") as f:
            json.dump(user_data, f, indent=2)

        print("Exported user db locally")

    except Exception:
        print("Failed to export to local user db")
        logging.exception("Failed to export user DB")

def update_local_user_db():
    """
    Update the local user database by exporting it from Google Sheets.
    This function is intended to be run periodically to keep the local database up-to-date.
    """
    try:
        export_user_db()
        print("Local user database updated successfully.")
    except Exception as e:
        print(f"Error updating local user database: {e}")
        logging.exception("Error updating local user database")

if __name__ == "__main__":
    export_user_db()
