import logging
from tkinter import Label

from screens.main_page import MainPage
from screens.no_acc_no_waiver import NoAccNoWaiver
from screens.no_acc_no_waiver_swipe import NoAccNoWaiverSwipe
from screens.no_acc_check_in_only import NoAccCheckInOnly
from screens.acc_no_waiver import AccNoWaiver
from screens.acc_no_waiver_swipe import AccNoWaiverSwipe
from screens.user_welcome import UserWelcome


class CheckInController:
    def __init__(self, ctx):
        self.ctx = ctx

    def handle_by_uuid(self, tag):
        result = self.ctx.sheets.checkin_by_uuid(tag)
        status = result.get("status")

        def update_ui():
            if status == "api_error":
                logging.error("API error during check-in")
                self.ctx.traffic_light.set_red()
                error_label = Label(
                    self.ctx.window.canvas,
                    text="System error, please let staff know.",
                    bg="#153246", fg="white", font=("Arial", 25),
                )
                error_label.place(relx=0.5, rely=0.1, anchor="center")
                error_label.after(4000, error_label.destroy)
                return

            if status == "no_account":
                logging.info(f"User {tag} not found.")
                self.ctx.traffic_light.set_red()
                self.ctx.nav.show_frame(NoAccNoWaiver)
                self.ctx.window.after(3000, lambda: self.ctx.nav.show_frame(NoAccNoWaiverSwipe))
                return

            if status == "no_waiver":
                logging.info(f"User {tag} does not have waiver.")
                self.ctx.traffic_light.set_yellow()
                self.ctx.nav.show_frame(AccNoWaiver)
                self.ctx.window.after(3000, lambda: self.ctx.nav.show_frame(AccNoWaiverSwipe))
                return

            logging.info(f"User found: {result['name']}")
            self.ctx.traffic_light.set_green()
            self.ctx.nav.get_frame(UserWelcome).displayName(result["name"])

        self.ctx.window.after(0, update_ui)

    def handle_by_pid(self, pid):
        result = self.ctx.sheets.checkin_by_pid(pid)
        status = result.get("status")

        if status == "no_account":
            logging.info("Manual check-in: user account not found")
            self.ctx.nav.show_frame(NoAccCheckInOnly)
            self.ctx.nav.after(5000, lambda: self.ctx.nav.show_frame(MainPage))
            return

        if status == "no_waiver":
            logging.info(f"Manual check-in: no waiver for {result.get('name', pid)}")
            self.ctx.nav.show_frame(AccNoWaiver)
            self.ctx.nav.after(3000, lambda: self.ctx.nav.show_frame(NoAccNoWaiverSwipe))
            return

        logging.info(f"Manual check-in for {result['name']}")
        self.ctx.traffic_light.set_green()
        self.ctx.nav.get_frame(UserWelcome).displayName(result["name"])
