from tkinter import Label
from gui import gui
from reader import *
from swipe import swipe
from sheets import *
from threading import Thread
from MainPage import MainPage
from ManualFill import ManualFill
from CheckInNoId import CheckInNoId
from utils import utils
from core.handle_check_in import handle_check_in
from core.render_ports import get_usb_ids
import global_
import socket
import logging
import argparse
from sys import stdout
from sheets import check_api_health

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
    scanner_error = False
    while True:
        time.sleep(0.1)

        if scanner_error:
            if reader.reconnect():
                logging.info("Card reader reconnected")
                scanner_error = False
            continue

        try:
            in_waiting = reader.getSerInWaiting()
        except OSError:
            if not scanner_error:
                logging.error("Card reader disconnected, disabling until reconnection")
                scanner_error = True
            continue

        if in_waiting >= 14:
            if not is_connected():
                logging.info("ERROR wifi is not connected")
                if not no_wifi_shown:
                    no_wifi_shown = True
                    no_wifi = Label(
                        app.canvas,
                        text="ERROR! Connection cannot be established, please let staff know.",
                        bg="#153246", fg="white", font=("Arial", 25),
                    )
                    no_wifi.place(relx=0.5, rely=0.1, anchor="center")
                    no_wifi.after(4000, lambda: destroyNoWifiError(no_wifi))
                continue

            app.get_frame(ManualFill).clearEntries()
            tag = reader.grabRFID()

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
            handle_check_in(tag)

            last_tag = tag
            last_time = time.time()

def trafficLightPoller():
    last_color = None
    while True:
        time.sleep(0.1)
        color = global_.sheets.get_traffic_light()
        if color != last_color:
            last_color = color
            if color == "red":
                global_.traffic_light.set_red()
            elif color == "green":
                global_.traffic_light.set_green()
            elif color == "yellow":
                global_.traffic_light.set_yellow()
            else:
                global_.traffic_light.set_off()


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
        logging.basicConfig(level=logging.DEBUG, stream=stdout)
    else:
        logging.basicConfig(level=logging.INFO)

    reader_usb_id, traffic_usb_id = get_usb_ids()
    check_api_health()
    global_.init(traffic_usb_id)
    app = gui()
    global_.setApp(app)
    global_.traffic_light.set_off()   

    sw = swipe()
    reader = Reader(reader_usb_id)
    util = utils()
    thread = Thread(target=myLoop, args=(app, reader))
    logging.info("Starting thread")
    thread.start()
    if global_.traffic_light.connected:
        poller = Thread(target=trafficLightPoller, daemon=True)
        poller.start()
    app.bind("<Key>", lambda i: sw.keyboardPress(i))
    app.bind("<Escape>", lambda i: clearAndReturn())
    logging.info("Made it to app start")
    app.start()