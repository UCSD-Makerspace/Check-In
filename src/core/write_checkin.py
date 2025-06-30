import os
import json
from datetime import datetime as dt

LOG_BASE_PATH = "assets/logs"

def write_checkin(curr_user, tag):
    now = dt.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    timestamp = now.isoformat(timespec="seconds")

    log_dir = os.path.join(LOG_BASE_PATH, year, month)
    os.makedirs(log_dir, exist_ok=True)

    log_path = os.path.join(log_dir, f"{day}.log")
    log_entry = {
        "tag": tag,
        "name": curr_user.get("Name", ""),
        "pid": curr_user.get("Student ID", ""),
        "timestamp": timestamp,
    }

    with open(log_path, "a", encoding="utf-8") as f:
        json.dump(log_entry, f)
        f.write("\n")