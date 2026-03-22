import tkinter
import logging


class AccountController:
    def __init__(self, ctx):
        self.ctx = ctx

    def create_account_from_barcode(self, barcode):
        self._create(barcode=barcode)

    def create_account_from_pid(self, pid):
        self._create(pid=pid)

    def _create(self, *, barcode=None, pid=None):
        canvas = self.ctx.window.canvas
        inProgress = tkinter.Label(
            canvas,
            text="Account creation in progress!",
            bg="#153246", fg="white", font=("Arial", 25),
        )
        inProgress.place(relx=0.5, rely=0.87, anchor="center")
        self.ctx.window.update()

        result = self.ctx.sheets.create_account(self.ctx.rfid, barcode=barcode, pid=pid)
        inProgress.destroy()

        if result is None:
            error = tkinter.Label(
                canvas,
                text="ERROR! Could not create account, please try manually.",
                bg="#153246", fg="white", font=("Arial", 20),
            )
            error.place(relx=0.5, rely=0.87, anchor="center")
            error.after(3000, lambda: error.destroy())
            return

        logging.info("Account creation succeeded")
        self.ctx.nav.pop()
