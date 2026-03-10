import global_
import logging
from tkinter import Label
from core.write_checkin import write_checkin
from gui import *


def handle_check_in(tag):
    result = global_.sheets.checkin_by_uuid(tag)
    status = result.get("status")

    def update_ui():
        if status == "api_error":
            logging.error("API error during check-in")
            global_.traffic_light.set_red()
            error_label = Label(
                global_.app.get_frame(MainPage),
                text="System error, please let staff know.",
                font=("Arial", 25),
            )
            error_label.pack(pady=40)
            error_label.after(4000, error_label.destroy)
            return

        if status == "no_account":
            logging.info(f"User {tag} not found.")
            global_.traffic_light.set_red()
            global_.app.show_frame(NoAccNoWaiver)
            global_.app.after(3000, lambda: global_.app.show_frame(NoAccNoWaiverSwipe))
            return

        if status == "no_waiver":
            logging.info(f"User {tag} does not have waiver.")
            global_.traffic_light.set_yellow()
            global_.app.show_frame(AccNoWaiver)
            global_.app.after(3000, lambda: global_.app.show_frame(AccNoWaiverSwipe))
            return

        logging.info(f"User found: {result['name']}")
        global_.traffic_light.set_green()
        global_.app.get_frame(UserWelcome).displayName(result["name"])
        write_checkin({
            "Name": result["name"],
            "Student ID": result["student_id"],
        }, tag)

    global_.app.after(0, update_ui)
