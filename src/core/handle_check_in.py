import global_
import logging
from tkinter import Label
from core.write_checkin import write_checkin


def handle_check_in(tag):
    result = global_.sheets.checkin_by_uuid(tag)
    status = result.get("status")

    def update_ui():
        from screens.main_page import MainPage
        from screens.no_acc_no_waiver import NoAccNoWaiver
        from screens.no_acc_no_waiver_swipe import NoAccNoWaiverSwipe
        from screens.acc_no_waiver import AccNoWaiver
        from screens.acc_no_waiver_swipe import AccNoWaiverSwipe
        from screens.user_welcome import UserWelcome

        if status == "api_error":
            logging.error("API error during check-in")
            global_.traffic_light.set_red()
            error_label = Label(
                global_.app.canvas,
                text="System error, please let staff know.",
                bg="#153246", fg="white", font=("Arial", 25),
            )
            error_label.place(relx=0.5, rely=0.1, anchor="center")
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
