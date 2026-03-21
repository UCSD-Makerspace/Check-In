import logging
from tkinter import Label
from core.write_checkin import write_checkin


def handle_check_in(ctx, tag):
    result = ctx.sheets.checkin_by_uuid(tag)
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
            ctx.traffic_light.set_red()
            error_label = Label(
                ctx.window.canvas,
                text="System error, please let staff know.",
                bg="#153246", fg="white", font=("Arial", 25),
            )
            error_label.place(relx=0.5, rely=0.1, anchor="center")
            error_label.after(4000, error_label.destroy)
            return

        if status == "no_account":
            logging.info(f"User {tag} not found.")
            ctx.traffic_light.set_red()
            ctx.nav.show_frame(NoAccNoWaiver)
            ctx.window.after(3000, lambda: ctx.nav.show_frame(NoAccNoWaiverSwipe))
            return

        if status == "no_waiver":
            logging.info(f"User {tag} does not have waiver.")
            ctx.traffic_light.set_yellow()
            ctx.nav.show_frame(AccNoWaiver)
            ctx.window.after(3000, lambda: ctx.nav.show_frame(AccNoWaiverSwipe))
            return

        logging.info(f"User found: {result['name']}")
        ctx.traffic_light.set_green()
        ctx.nav.get_frame(UserWelcome).displayName(result["name"])
        write_checkin({
            "Name": result["name"],
            "Student ID": result["student_id"],
        }, tag)

    ctx.window.after(0, update_ui)
