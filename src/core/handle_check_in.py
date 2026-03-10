import global_
import logging
import time
from core.write_checkin import write_checkin
from core.UserRecord import UserRecord
from gui import *


def handle_check_in(tag, util):
    curr_user = UserRecord.load(tag, global_.sheets)

    if not curr_user:
        logging.info(f"User {tag} not found.")
        global_.traffic_light.set_red()
        global_.app.show_frame(NoAccNoWaiver)
        global_.app.after(3000, lambda: global_.app.show_frame(NoAccNoWaiverSwipe))
        return

    if not curr_user.has_waiver():
        logging.info(f"User {curr_user.data['Name']} does not have waiver")
        global_.traffic_light.set_yellow()
        global_.app.show_frame(AccNoWaiver)
        global_.app.after(3000, lambda: global_.app.show_frame(AccNoWaiverSwipe))
        return

    new_row = [
        util.getDatetime(),
        int(time.time()),
        curr_user.data["Name"],
        str(tag),
        "User Check-In",
        "",
        curr_user.data.get("firstEnrTrm", ""),
        curr_user.data.get("lastEnrTrm", ""),
    ]

    global_.checkin_logger.enqueue_row(new_row, tag)
    global_.traffic_light.set_green()
    global_.app.get_frame(UserWelcome).displayName(curr_user.data["Name"])
    write_checkin(curr_user.data, tag)
