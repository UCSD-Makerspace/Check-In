import global_
import logging
from core.write_checkin import write_checkin
from core.new_row_check_in import new_row_check_in
from core.UserRecord import UserRecord
from gui import *
from reader import *

def handle_check_in(tag, util):
    curr_user = UserRecord.load(tag, global_.sheets)

    if not curr_user:
        logging.info(f"User {tag} not found.")
        new_row_check_in(None, "None", tag, util, None, None)
        return

    waiver_status = "waiver_confirmed" if curr_user.has_waiver() else "None"

    new_row_check_in(curr_user.data, waiver_status, tag, util, curr_user.data.get("firstEnrTrm"), curr_user.data.get("lastEnrTrm"))
    write_checkin(curr_user.data, tag)
