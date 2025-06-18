import sys
import logging
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sheets import SheetManager

EXPORT_PATH = os.path.join(
    os.path.dirname(__file__), "assets", "local_user_db.json"
)

def export_user_db():
    try:
        sheet_manager = SheetManager()
    except Exception as e:
        print("Failed to export to local user db")
        logging.exception("Failed to export user DB")

if __name__ == "__main__":
    export_user_db()