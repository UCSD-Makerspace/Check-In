import tkinter
import logging
from screens.manual_fill import ManualFill
from screens.no_acc_no_waiver_swipe import NoAccNoWaiverSwipe
from screens.waiver_no_acc_swipe import WaiverNoAccSwipe
from screens.check_in_no_id import CheckInNoId
from api.get_info_from_pid import contact_client


class SwipeController:
    def __init__(self, ctx):
        self.ctx = ctx
        self._id_string = ""
        self._swipe_error_shown = False

    def _id_vet(self, id_check):
        if any(i.isalpha() for i in id_check):
            return "bad"
        if len(id_check) >= 16:
            return "bad"
        return "good"

    def keyboardPress(self, key):
        curr_frame = self.ctx.nav.get_curr_frame()

        if curr_frame not in (NoAccNoWaiverSwipe, WaiverNoAccSwipe, CheckInNoId):
            return

        self._id_string += key.char
        logging.debug("The array is now: " + repr(str(self._id_string)))

        if self._id_string.endswith("\r"):
            if self._id_vet(self._id_string) == "bad":
                self._id_string = ""
                if not self._swipe_error_shown:
                    self._swipe_error_shown = True
                    id_error = tkinter.Label(
                        self.ctx.window.canvas, text="Error, please scan again",
                        bg="#153246", fg="white", font=("Arial", 20),
                    )
                    id_error.place(relx=0.5, rely=0.85, anchor="center")
                    id_error.after(1500, lambda: self._destroySwipeError(id_error))
                return

            self._swipeCard(self._id_string)
            self._id_string = ""

    def _pullUser(self, barcode, u_type):
        logging.info(f"Card barcode read is: {barcode}. Trying to pull user...")

        contact = contact_client()
        try:
            if u_type == "Staff":
                u_info = contact.get_staff_info(barcode)
            elif u_type == "Student":
                u_info = contact.get_student_info(barcode)
        except Exception:
            logging.warning("An exception has ocurred with pulling user information", exc_info=True)
            return None

        if not u_info:
            logging.info("Student search returned False, returning...")
            return None

        logging.info(f"Info pull succeeded:\n {u_info[0]}, {u_info[1]}, {u_info[3]}")
        return u_info

    def _swipeCard(self, id_string):
        u_data = self._pullUser(id_string.strip(), "Student")
        if not u_data:
            logging.info("Student search returned False, returning...")
            return

        if self.ctx.nav.get_curr_frame() == CheckInNoId:
            self.ctx.nav.get_frame(CheckInNoId).clearEntries()
            self.ctx.nav.get_frame(CheckInNoId).updateEntries(u_data[3])
            return

        email_to_use = "" if len(u_data[2]) == 0 else u_data[2][0]
        for email in u_data[2]:
            if email.endswith("@ucsd.edu"):
                email_to_use = email

        manfill = self.ctx.nav.get_frame(ManualFill)
        manfill.clearEntries()
        logging.info(f"Filling data with {u_data[0]} {u_data[1]} {email_to_use} {u_data[3]}")
        manfill.updateEntries(u_data[0], u_data[1], email_to_use, u_data[3])

        self.ctx.nav.show_frame(ManualFill)

    def _destroySwipeError(self, id_error):
        id_error.destroy()
        self._swipe_error_shown = False
