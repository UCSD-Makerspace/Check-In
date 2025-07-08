from datetime import datetime as dt
from core.checkin_queue import CheckInLogger
from core.handle_check_in import handle_check_in
from core.render_ports import get_usb_ids
from gui import *
from reader import *
from fabman import *
import json
from sheets import *
from threading import Thread
from UserWelcome import *
from ManualFill import *
from CheckInNoId import *
from get_info_from_pid import contact_client
from swipe import *
from tkinter import *
import global_
import socket
import logging
import argparse


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


def myLoop(app, reader):
    global no_wifi_shown, no_wifi
    logging.info("Now reading ID cards")
    last_tag = 0
    last_time = 0
    contact = contact_client()

    while True:
        time.sleep(0.1)
        in_waiting = reader.getSerInWaiting()
        tag = 0

        if in_waiting >= 14:
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

            tag_read_start = perf_counter()
            tag = reader.grabRFID()
            tag_read_end = perf_counter()

            if " " in tag:
                continue

            if tag == last_tag and not reader.canScanAgain(last_time):
                logging.debug("Suppressing repeat scan")
                continue

            s_reason = reader.checkRFID(tag)

            if s_reason != "good":
                logging.debug(s_reason)
                continue
            else:
                logging.debug("RFID Check Succeeded")

            global_.setRFID(tag)
            handle_check_in(tag, contact, util)

            last_tag = tag
            last_time = time.time()

            reader.readSerial()

def destroyNoWifiError(no_wifi):
    global no_wifi_shown
    no_wifi.destroy()
    no_wifi_shown = False


def clearAndReturn():
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

    reader_usb_id, traffic_usb_id = get_usb_ids()
    global_.init(traffic_usb_id) 
    app = gui()
    global_.setApp(app)
    global_.checkin_logger = CheckInLogger()
    reader = Reader()
    util = utils()
    thread = Thread(target=myLoop, args=(app, reader))
    logging.info("Starting thread")
    thread.start()
    app.bind("<Escape>", lambda i: clearAndReturn())
    logging.info("Made it to app start")
    app.start()
