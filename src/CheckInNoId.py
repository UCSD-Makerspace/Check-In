from pathlib import Path
from tkinter import Button, Entry, StringVar, END
from screen import Screen
import global_
import logging

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/check_in_no_id_assets")


########################################################
# This is the frame where users will manually check in #
########################################################

class CheckInNoId(Screen):
    def _build(self, controller):
        from NoAccCheckInOnly import NoAccCheckInOnly
        from NoAccNoWaiverSwipe import NoAccNoWaiverSwipe
        from UserWelcome import UserWelcome
        from AccNoWaiver import AccNoWaiver

        self.loading_text_id = None
        self.pid = StringVar()

        img2 = self._photo(ASSETS_PATH / "image_2.png")
        self._image(640.0, 360.0, image=img2)

        img3 = self._photo(ASSETS_PATH / "image_3.png")
        self._image(640.0, 424.0, image=img3)

        self._text(
            212.0, 120.0, anchor="nw",
            text="If you have already made an\naccount, scan your UCSD barcode\nor enter your PID manually",
            fill="#F5F0E6", font=("Montserrat", 48 * -1), justify="center",
        )
        self._text(
            605.0, 480.0, anchor="nw",
            text="PID", fill="#F5F0E6", font=("Montserrat", 24 * -1),
        )

        btn_img = self._photo(ASSETS_PATH / "button_1.png")
        btn = Button(
            self.canvas, image=btn_img,
            borderwidth=0, highlightthickness=0,
            command=lambda: self._call_check_in(controller), relief="flat",
        )
        self._window(465.0, 598.0, btn, width=349, height=71)

        self.pid_entry = Entry(self.canvas, textvariable=self.pid, width=40, font=52)
        self._window(420.0, 412.0, self.pid_entry)

    def displayLoading(self):
        if self.loading_text_id is None:
            self.loading_text_id = self.canvas.create_text(
                420.0, 545.0, anchor="nw",
                text="PLEASE WAIT: LOADING...",
                fill="#FF0000", font=("Montserrat", 36 * -1, "bold"), justify="center",
            )

    def clearEntries(self):
        self.pid_entry.delete(0, END)

    def updateEntries(self, pid):
        self.pid_entry.insert(0, pid)

    def _call_check_in(self, controller):
        from NoAccCheckInOnly import NoAccCheckInOnly
        from NoAccNoWaiverSwipe import NoAccNoWaiverSwipe
        from UserWelcome import UserWelcome
        from AccNoWaiver import AccNoWaiver
        from MainPage import MainPage

        pid = self.pid_entry.get()
        if not pid:
            return

        self.displayLoading()
        self.canvas.update_idletasks()
        self.clearEntries()

        result = global_.sheets.checkin_by_pid(pid)
        status = result.get("status")

        if self.loading_text_id is not None:
            self.canvas.delete(self.loading_text_id)
            self.loading_text_id = None

        if status == "no_account":
            logging.info("Manual check-in: user account not found")
            controller.show_frame(NoAccCheckInOnly)
            controller.after(5000, lambda: controller.show_frame(MainPage))
            return

        if status == "no_waiver":
            logging.info(f"Manual check-in: no waiver for {result.get('name', pid)}")
            controller.show_frame(AccNoWaiver)
            controller.after(3000, lambda: controller.show_frame(NoAccNoWaiverSwipe))
            return

        logging.info(f"Manual check-in for {result['name']}")
        global_.traffic_light.set_green()
        global_.app.get_frame(UserWelcome).displayName(result["name"])
