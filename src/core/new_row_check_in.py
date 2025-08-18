import logging
import global_
import time
from gui import *

def new_row_check_in(curr_user, curr_user_w, tag, util, firstEnrTrm, lastEnrTrm, last_payment):
    if curr_user and last_payment == "unpaid":
        logging.info(f"Payment not found for user {curr_user}")
        global_.traffic_light.set_red()
        global_.app.show_frame(AccNoWaiver)
        global_.app.after(3000, lambda: global_.app.show_frame(AccNoWaiverSwipe))
    elif curr_user is None and curr_user_w == "None":
        logging.info("User was not found in databases")
        global_.traffic_light.set_red()
        global_.app.show_frame(NoAccNoWaiver)
        global_.app.after(3000, lambda: global_.app.show_frame(NoAccNoWaiverSwipe))
    elif curr_user_w == "None":
        logging.info("User does not have waiver")
        global_.traffic_light.set_yellow()
        global_.app.show_frame(AccNoWaiver)
        global_.app.after(3000, lambda: global_.app.show_frame(AccNoWaiverSwipe))
    elif curr_user is None:
        logging.info("User has a waiver but no account")
        global_.app.show_frame(WaiverNoAcc)
        global_.app.after(3000, lambda: global_.app.show_frame(WaiverNoAccSwipe))
    else:
        new_row = [
            util.getDatetime(),
            int(time.time()),
            curr_user["Name"],
            str(tag),
            "User Check-In",
            "",
            firstEnrTrm,
            lastEnrTrm, 
        ]

        global_.checkin_logger.enqueue_row(new_row, tag)
        global_.traffic_light.set_green()
        global_.app.get_frame(UserWelcome).displayName(curr_user["Name"])