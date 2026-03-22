import tkinter
import logging
from screens.create_account_barcode import CreateAccountBarcode
from screens.create_account_manual import CreateAccountManual


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

        if curr_frame not in (CreateAccountBarcode, CreateAccountManual):
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

            logging.info(f"Card barcode read: {self._id_string.strip()!r}")
            self.ctx.account.create_account_from_barcode(self._id_string.strip())
            self._id_string = ""

    def _destroy_swipe_error(self, id_error):
        id_error.destroy()
        self._swipe_error_shown = False
