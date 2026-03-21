from tkinter import Label
from window import CheckInWindow
from controllers.navigation_controller import NavigationController
from reader import *
from controllers.swipe_controller import SwipeController
from threading import Thread
from screens.main_page import MainPage
from screens.manual_fill import ManualFill
from screens.check_in_no_id import CheckInNoId
from utils import Utils
from core.handle_check_in import handle_check_in
from core.render_ports import get_usb_ids
from app_context import AppContext
from sheets import check_api_health
import socket
import logging
import argparse
from sys import stdout


def is_connected(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False


no_wifi_shown = False


def myLoop(ctx: AppContext, reader):
    global no_wifi_shown, no_wifi
    logging.info("Now reading ID cards")
    last_tag = 0
    last_time = 0
    scanner_error = False
    while True:
        if scanner_error:
            time.sleep(0.1)
            if reader.reconnect():
                logging.info("Card reader reconnected")
                scanner_error = False
            continue

        try:
            in_waiting = reader.getSerInWaiting()
        except OSError as e:
            if not scanner_error:
                logging.error("Card reader disconnected, disabling until reconnection: %s", e)
                scanner_error = True
            continue

        if in_waiting >= 14:
            if not is_connected():
                logging.info("ERROR wifi is not connected")
                if not no_wifi_shown:
                    no_wifi_shown = True
                    no_wifi = Label(
                        ctx.window.canvas,
                        text="ERROR! Connection cannot be established, please let staff know.",
                        bg="#153246", fg="white", font=("Arial", 25),
                    )
                    no_wifi.place(relx=0.5, rely=0.1, anchor="center")
                    no_wifi.after(4000, lambda: destroyNoWifiError(no_wifi))
                continue

            ctx.nav.get_frame(ManualFill).clearEntries()
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

            ctx.rfid = tag
            handle_check_in(ctx, tag)

            last_tag = tag
            last_time = time.time()


def trafficLightPoller(ctx: AppContext):
    last_color = None
    light = ctx.traffic_light._light
    while True:
        time.sleep(0.1)
        color = ctx.sheets.get_traffic_light()
        if color != last_color:
            last_color = color
            if color == "red":
                light.set_red()
            elif color == "green":
                light.set_green()
            elif color == "yellow":
                light.set_yellow()
            else:
                light.set_off()


def destroyNoWifiError(no_wifi):
    global no_wifi_shown
    no_wifi.destroy()
    no_wifi_shown = False


def clearAndReturn(ctx: AppContext):
    ctx.traffic_light.set_off()
    ctx.nav.show_frame(MainPage)
    ctx.nav.get_frame(ManualFill).clearEntries()
    ctx.nav.get_frame(CheckInNoId).clearEntries()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Makerspace Check-in System",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase verbosity (print debug info)")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, stream=stdout)
    else:
        logging.basicConfig(level=logging.INFO)

    reader_usb_id, traffic_usb_id = get_usb_ids()
    check_api_health()
    ctx = AppContext.create(traffic_usb_id)
    window = CheckInWindow()
    nav = NavigationController(window, ctx)
    ctx.window = window
    ctx.nav = nav
    ctx.traffic_light.set_off()

    sw = SwipeController(ctx)
    reader = Reader(reader_usb_id)
    thread = Thread(target=myLoop, args=(ctx, reader))
    logging.info("Starting thread")
    thread.start()
    if ctx.traffic_light.connected:
        poller = Thread(target=trafficLightPoller, args=(ctx,), daemon=True)
        poller.start()
    window.bind("<Key>", lambda i: sw.keyboardPress(i))
    window.bind("<Escape>", lambda i: clearAndReturn(ctx))
    logging.info("Made it to app start")
    window.start()
