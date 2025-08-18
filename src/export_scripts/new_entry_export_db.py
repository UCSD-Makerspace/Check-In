import json
import logging
import os

from sheets import SheetManager

IMPORT_PATH = os.path.join(os.path.dirname(__file__), "assets", "local_user_db.json")
EXPORT_PATH = os.path.join(os.path.dirname(__file__), "assets", "user_db.json")

def export_user_db():
    try:
        with open(IMPORT_PATH, "r", eocoding="utf-8") as f:
            data = json.load(f)

        for user_data in data.values():
            user_data["Last Paid Term"] = None

        with open(EXPORT_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    except Exception:
        print("Failed to export to local user db")
        logging.exception("Failed to export user DB")

if __name__ == "__main__":
    export_user_db()
