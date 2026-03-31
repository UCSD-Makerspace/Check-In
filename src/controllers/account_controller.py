import logging

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication


class AccountController:
    def __init__(self, ctx):
        self.ctx = ctx

    def go_to_review_from_barcode(self, barcode):
        self.ctx.nav.show_status("Looking up student...")
        QApplication.processEvents()

        student = self.ctx.sheets.lookup_by_barcode(barcode)
        self.ctx.nav.hide_status()

        if student is None:
            self.ctx.nav.show_status("Student not found. Please enter your details manually.")
            QTimer.singleShot(3000, self.ctx.nav.hide_status)
            return

        self.ctx.nav.go_to_create_account_review(
            pid=student["pid"],
            first_name=student["first_name"],
            last_name=student["last_name"],
            email=student["email"],
        )

    def go_to_review_from_pid(self, pid):
        self.ctx.nav.show_status("Looking up student...")
        QApplication.processEvents()

        student = self.ctx.sheets.lookup_by_pid(pid)
        self.ctx.nav.hide_status()

        if student is None:
            self.ctx.nav.show_status("Student not found. Please check your PID.")
            QTimer.singleShot(3000, self.ctx.nav.hide_status)
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
        self.ctx.nav.show_status("Account creation in progress!")
        QApplication.processEvents()

        result = self.ctx.sheets.create_account(
            self.ctx.rfid,
            barcode=barcode,
            pid=pid,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        self.ctx.nav.hide_status()

        if result is None:
            self.ctx.nav.show_status("ERROR! Could not create account, please try manually.")
            QTimer.singleShot(3000, self.ctx.nav.hide_status)
            return

        logging.info("Account creation succeeded")
        self.ctx.nav.pop()
