import logging
from tkinter import Label

from screens.user_welcome import UserWelcome


class CheckInController:
    def __init__(self, ctx):
        self.ctx = ctx

    def handle_by_uuid(self, tag):
        # Called from background thread — defer to main thread.
        self.ctx.window.after(
            0, lambda: self._run_check_in(tag, self.ctx.sheets.checkin_by_uuid)
        )

    def handle_by_pid(self, pid):
        self._run_check_in(pid, self.ctx.sheets.checkin_by_pid)

    def _run_check_in(self, identifier, check_fn, welcome_message="Welcome back"):
        result = check_fn(identifier)
        status = result.get("status")

        if status == "api_error":
            logging.error("API error during check-in")
            self.ctx.traffic_light.request_red()
            error_label = Label(
                self.ctx.window.canvas,
                text="System error, please let staff know.",
                bg="#153246", fg="white", font=("Arial", 25),
            )
            error_label.place(relx=0.5, rely=0.1, anchor="center")
            error_label.after(4000, error_label.destroy)
            return

        if status == "no_account":
            logging.info(f"No account found for {identifier}")
            self.ctx.traffic_light.request_red()
            self.ctx.nav.go_to_create_account(
                on_done=lambda: self._run_check_in(
                    identifier, check_fn, welcome_message="Thank you for registering"
                )
            )
            return

        if status == "no_waiver":
            logging.info(f"No waiver for {identifier}")
            self.ctx.traffic_light.request_yellow()
            self.ctx.nav.go_to_sign_waiver()
            return

        logging.info(f"Check-in successful: {result['name']}")
        self.ctx.traffic_light.request_green()
        self.ctx.nav.get_frame(UserWelcome).display_name(result["name"], welcome_message)
