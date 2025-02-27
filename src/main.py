from tkinter import *
from gui import *
from swipe import *
from sheets import *
from threading import Thread
from UserWelcome import *
from ManualFill import *
from CheckInNoId import *
from CheckInReason import *
import global_
import socket
import logging
import argparse
import serial.tools.list_ports as list_ports
import rfid

TRAFFIC_LIGHT_VID = 6790
READER_VID = 4292


def is_connected(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        return False


##############################################################
# This acts as the main loop of the program, ran in a thread #
##############################################################

no_wifi_shown = False


def myLoop(app):
    global no_wifi_shown, no_wifi
    logging.info("Now reading ID cards")
    last_tag = 0
    last_time = 0
    card_reader = rfid()

    while True:
        time.sleep(0.1)
        tag = 0

        if not is_connected():
            logging.info("ERROR wifi is not connected")
            if not no_wifi_shown:
                no_wifi_shown = True
                no_wifi = Label(
                    app.get_frame(MainPage),
                    text="ERROR! Connection cannot be established, please let staff know.",
                    font=("Arial", 25),
                )
                no_wifi.pack(pady=40)
                no_wifi.after(4000, lambda: destroyNoWifiError(no_wifi))
            continue

        app.get_frame(ManualFill).clearEntries()
        tag = card_reader.getRFID()

        if " " in tag:
            continue

        logging.debug("RFID Check Succeeded")

        global_.setRFID(tag)

        # Get a list of all users
        user_data = global_.sheets.get_user_db_data()
        curr_user = "None"

        for i in user_data:
            if i["Card UUID"] == tag:
                curr_user = i

        ############################
        # All scenarios for ID tap #
        ############################

        if curr_user == "None":
            logging.info("User was not found in the database")
            global_.traffic_light.set_red()
            app.show_frame(NoAccount)
            app.after(3000, lambda: app.show_frame(NoAccSwipe))
        else:
            new_row = [
                util.getDatetime(),
                int(time.time()),
                curr_user["Name"],
                str(tag),
                "User Checkin",
                curr_user["Email Address"],
                curr_user["Student ID"],
                "",
                curr_user["Affiliation"],
            ]

            check_in_reason = global_.app.get_frame(CheckInReason)
            check_in_reason.setCheckInUser(new_row)
            app.show_frame(CheckInReason)

        last_time = time.time()
        last_tag = tag


def destroyNoWifiError(no_wifi):
    global no_wifi_shown
    no_wifi.destroy()
    no_wifi_shown = False


def clearAndReturn():
    global_.traffic_light.set_off()
    global_.app.show_frame(MainPage)
    global_.app.get_frame(ManualFill).clearEntries()
    global_.app.get_frame(CheckInNoId).clearEntries()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Makerspace Check-in System",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Increase verbosity (print debug info)",
    )

    args = parser.parse_args()
    config = vars(args)

    if config["verbose"]:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    ports = list(list_ports.comports())
    traffic_usb_id = None

    for p in ports:
        if p.vid == TRAFFIC_LIGHT_VID:
            traffic_usb_id = p.device

    global_.init(traffic_usb_id)
    app = gui()
    global_.setApp(app)
    global_.traffic_light.set_off()
    sw = swipe()
    util = utils()
    thread = Thread(target=myLoop, args=(app))
    logging.info("Starting thread")
    thread.start()
    app.bind("<Key>", lambda i: sw.keyboardPress(i))
    app.bind("<Escape>", lambda i: clearAndReturn())
    logging.info("Made it to app start")
    app.start()
