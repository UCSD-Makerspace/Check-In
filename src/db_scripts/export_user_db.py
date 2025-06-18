import sys
import logging
import os
import json

script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, ".."))
os.chdir(project_root)

sys.path.append(os.path.join(project_root, "src"))

from sheets import SheetManager

EXPORT_PATH = os.path.join(
    project_root, "assets", "local_user_db.json"
)

########################################################
# Function to write user database to a local JSON file #
########################################################
def export_user_db():
    try:
        os.makedirs(os.path.dirname(EXPORT_PATH), exist_ok=True)

        sheet_manager = SheetManager()
        raw_data = sheet_manager.get_user_db_data(force_update=True)

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

        with open(EXPORT_PATH, "w", encoding="utf-8") as f:
            json.dump(user_data, f, indent=2)
        print("Exported user db locally")

    except Exception as e:
        print("Failed to export to local user db")
        logging.exception("Failed to export user DB")

if __name__ == "__main__":
    export_user_db()
