import logging

from PyQt6.QtCore import QTimer

from screens.user_welcome import UserWelcome


class CheckInController:
    def __init__(self, ctx):
        self.ctx = ctx

    def handle_by_uuid(self, tag):
        # Called from background thread — dispatch to main thread via signal.
        self.ctx.dispatcher.call.emit(
            lambda: self._run_check_in(tag, self.ctx.sheets.checkin_by_uuid)
        )

    def handle_by_pid(self, pid):
        # Called on main thread (button click or barcode dispatcher).
        self._run_check_in(pid, self.ctx.sheets.checkin_by_pid)

    def _run_check_in(self, identifier, check_fn, welcome_message="Welcome back"):
        result = check_fn(identifier)
        status = result.get("status")

        if status == "api_error":
            logging.error("API error during check-in")
            self.ctx.traffic_light.request_red()
            self.ctx.nav.show_status("System error, please let staff know.")
            QTimer.singleShot(4000, self.ctx.nav.hide_status)
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
