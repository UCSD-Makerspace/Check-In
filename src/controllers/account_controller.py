import time
import tkinter
import logging
from screens.main_page import MainPage
from screens.acc_no_waiver_swipe import AccNoWaiverSwipe
from screens.user_thank import UserThank


class AccountController:
    def __init__(self, ctx):
        self.ctx = ctx

    def _email_check(self, email):
        if "@" not in email or "." not in email:
            return "Email is invalid"
        return "good"

    def _name_check(self, fname, lname):
        if len(fname) == 0 or len(lname) == 0:
            return "Name was not entered"
        return "good"

    def _id_check(self, user_id):
        if len(user_id) <= 2 or len(user_id) > 12:
            return "PID was not entered correctly"
        return "good"

    def create_account(self, fname, lname, email, pid):
        start = time.perf_counter()
        idValid = self._id_check(pid)
        emailValid = self._email_check(email)
        nameValid = self._name_check(fname, lname)

        canvas = self.ctx.window.canvas

        for validation in (idValid, emailValid, nameValid):
            if validation != "good":
                invalidID = tkinter.Label(
                    canvas, text=validation, bg="#153246", fg="white", font=("Arial", 20)
                )
                invalidID.place(relx=0.5, rely=0.83, anchor="center")
                invalidID.after(3000, lambda: invalidID.destroy())
                return

        end1 = time.perf_counter()
        logging.debug(f"Time to validate info: {end1 - start}")

        inProgress = tkinter.Label(
            canvas,
            text="Account creation in progress!",
            bg="#153246", fg="white", font=("Arial", 25),
        )
        inProgress.place(relx=0.5, rely=0.87, anchor="center")
        self.ctx.window.update()

        full_name = fname + " " + lname
        logging.info(f"Creating user account for {full_name}")

        no_wifi = tkinter.Label(
            canvas,
            text="ERROR! Connection cannot be established, please let staff know.",
            bg="#153246", fg="white", font=("Arial", 25),
        )

        end2 = time.perf_counter()
        logging.debug(f"Time to structure row entries: {end2 - end1}")

        retries = 1
        while retries < 6:
            try:
                result = self.ctx.sheets.create_account(fname, lname, email, pid, self.ctx.rfid)
                end3 = time.perf_counter()
                logging.debug(f"Time to create account: {end3 - end2}")

                if result is None:
                    raise Exception("Account creation returned no result")

                break
            except Exception as e:
                logging.warning("Exception occurred while in account creation")
                logging.exception("Exception occurred while in account creation")
                no_wifi.place(relx=0.5, rely=0.91, anchor="center")
                self.ctx.window.update()
                time.sleep(retries)
                retries += 1

        no_wifi.destroy()

        if retries == 6:
            self.ctx.nav.show_frame(MainPage)
            inProgress.destroy()
            return

        end4 = time.perf_counter()
        logging.debug(f"Total time to send data: {end4 - end2}")

        checkin_result = self.ctx.sheets.checkin_by_uuid(self.ctx.rfid)
        toGoTo = AccNoWaiverSwipe if checkin_result.get("status") == "no_waiver" else MainPage

        end5 = time.perf_counter()
        logging.debug(f"Time to check waiver via check-in: {end5 - end4}")

        self.ctx.nav.get_frame(UserThank).displayName(full_name, toGoTo)
        inProgress.destroy()

    def on_thank_start(self, next_page):
        from screens.main_page import MainPage
        if next_page == MainPage:
            self.ctx.traffic_light.set_green()
        else:
            self.ctx.traffic_light.set_yellow()

    def on_thank_done(self, next_page):
        from screens.main_page import MainPage
        self.ctx.nav.show_frame(next_page)
        if next_page == MainPage:
            self.ctx.traffic_light.set_off()
