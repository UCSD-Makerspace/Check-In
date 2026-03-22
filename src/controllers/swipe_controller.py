import tkinter
import logging
from screens.create_account_manual import CreateAccountManual
from screens.create_account_barcode import CreateAccountBarcode
from screens.check_in_manual import CheckInManual
from api.get_info_from_pid import ContactClient


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

    def keyboard_press(self, key):
        curr_frame = self.ctx.nav.get_curr_frame()

        if curr_frame not in (CreateAccountBarcode, CheckInManual):
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
                    id_error.after(1500, lambda: self._destroy_swipe_error(id_error))
                return

            self._swipe_card(self._id_string)
            self._id_string = ""

    def _pull_user(self, barcode, u_type):
        logging.info(f"Card barcode read is: {barcode}. Trying to pull user...")

        contact = ContactClient()
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

        logging.info(f"Info pull succeeded:\n {u_info.first_name}, {u_info.last_name}, {u_info.pid}")
        return u_info

    def _swipe_card(self, id_string):
        u_data = self._pull_user(id_string.strip(), "Student")
        if not u_data:
            logging.info("Student search returned False, returning...")
            return

        if self.ctx.nav.get_curr_frame() == CheckInManual:
            self.ctx.nav.get_frame(CheckInManual).clear_entries()
            self.ctx.nav.get_frame(CheckInManual).update_entries(u_data.pid)
            return

        email_to_use = "" if len(u_data.emails) == 0 else u_data.emails[0]
        for email in u_data.emails:
            if email.endswith("@ucsd.edu"):
                email_to_use = email

        manfill = self.ctx.nav.get_frame(CreateAccountManual)
        manfill.clear_entries()
        logging.info(f"Filling data with {u_data.first_name} {u_data.last_name} {email_to_use} {u_data.pid}")
        manfill.update_entries(u_data.first_name, u_data.last_name, email_to_use, u_data.pid)

        self.ctx.nav.show_frame(CreateAccountManual)

    def _destroy_swipe_error(self, id_error):
        id_error.destroy()
        self._swipe_error_shown = False
