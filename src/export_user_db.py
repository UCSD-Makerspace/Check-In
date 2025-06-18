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

        user_data = []
        for row in raw_data:
            user_data.append({
                "Name": row.get("Name", ""),
                "Timestamp": row.get("Timestamp", ""),
                "Card UUID": row.get("Card UUID", ""),
                "Student ID": row.get("Student ID", ""),
                "Email Address": row.get("Email Address", ""),
                "Waiver Signed": row.get("Waiver Signed?", ""),
            })
        print(f"Length of user data: {len(user_data)}")

        print(f"Writing to: {os.path.abspath(EXPORT_PATH)}")
        with open(EXPORT_PATH, "w", encoding="utf-8") as f:
            json.dump(user_data, f, indent=2)

        print("Exported user db locally")

    except Exception:
        print("Failed to export to local user db")
        logging.exception("Failed to export user DB")

if __name__ == "__main__":
    export_user_db()
