import tkinter
import logging


class AccountController:
    def __init__(self, ctx):
        self.ctx = ctx

    def create_account_from_barcode(self, barcode):
        self._create(barcode=barcode)

    def go_to_review_from_barcode(self, barcode):
        canvas = self.ctx.window.canvas
        loading = tkinter.Label(
            canvas,
            text="Looking up student...",
            bg="#153246", fg="white", font=("Arial", 25),
        )
        loading.place(relx=0.5, rely=0.87, anchor="center")
        self.ctx.window.update()

        student = self.ctx.sheets.lookup_by_barcode(barcode)
        loading.destroy()

        if student is None:
            error = tkinter.Label(
                canvas,
                text="Student not found. Please enter your details manually.",
                bg="#153246", fg="white", font=("Arial", 20),
            )
            error.place(relx=0.5, rely=0.87, anchor="center")
            error.after(3000, error.destroy)
            return

        self.ctx.nav.go_to_create_account_review(
            pid=student["pid"],
            first_name=student["first_name"],
            last_name=student["last_name"],
            email=student["email"],
        )

    def create_account_from_pid(self, pid):
        self._create(pid=pid)

    def go_to_review_from_pid(self, pid):
        canvas = self.ctx.window.canvas
        loading = tkinter.Label(
            canvas,
            text="Looking up student...",
            bg="#153246", fg="white", font=("Arial", 25),
        )
        loading.place(relx=0.5, rely=0.87, anchor="center")
        self.ctx.window.update()

        student = self.ctx.sheets.lookup_by_pid(pid)
        loading.destroy()

        if student is None:
            error = tkinter.Label(
                canvas,
                text="Student not found. Please check your PID.",
                bg="#153246", fg="white", font=("Arial", 20),
            )
            error.place(relx=0.5, rely=0.87, anchor="center")
            error.after(3000, error.destroy)
            return

        self.ctx.nav.go_to_create_account_review(
            pid=pid,
            first_name=student["first_name"],
            last_name=student["last_name"],
            email=student["email"],
        )

    def create_account_from_review(self, *, first_name, last_name, email, pid):
        if pid:
            self._create(pid=pid)
        else:
            self._create(first_name=first_name, last_name=last_name, email=email)

    def _create(self, *, barcode=None, pid=None, first_name=None, last_name=None, email=None):
        canvas = self.ctx.window.canvas
        inProgress = tkinter.Label(
            canvas,
            text="Account creation in progress!",
            bg="#153246", fg="white", font=("Arial", 25),
        )
        inProgress.place(relx=0.5, rely=0.87, anchor="center")
        self.ctx.window.update()

        result = self.ctx.sheets.create_account(
            self.ctx.rfid,
            barcode=barcode,
            pid=pid,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
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
