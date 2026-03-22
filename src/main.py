from window import CheckInWindow
from controllers.navigation_controller import NavigationController
from controllers.swipe_controller import SwipeController
from controllers.check_in_controller import CheckInController
from controllers.account_controller import AccountController
from controllers.rfid_reader_controller import RfidReaderController
from hardware.rfid_reader import Reader
from screens.create_account_manual import CreateAccountManual
from screens.check_in_manual import CheckInManual
from hardware.usb_ports import get_usb_ids
from app_context import AppContext
from api.sheets import check_api_health
import logging
import argparse
from sys import stdout


def clear_and_return(ctx: AppContext):
    ctx.nav.back_to_main()
    ctx.nav.get_frame(CreateAccountManual).clear_entries()
    ctx.nav.get_frame(CheckInManual).clear_entries()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Makerspace Check-in System",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase verbosity (print debug info)")
    parser.add_argument("-d", "--dev", action="store_true", help="Enable dev mode with on-screen navigation overlay")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, stream=stdout)
    else:
        logging.basicConfig(level=logging.INFO)

    import os
    dev_mode = args.dev or os.environ.get("DEV_MODE") == "1"

    usb = get_usb_ids()
    check_api_health()
    ctx = AppContext.create(usb.traffic_light)
    window = CheckInWindow()
    nav = NavigationController(window, ctx, dev_mode=dev_mode)
    ctx.window = window
    ctx.nav = nav
    ctx.check_in = CheckInController(ctx)
    ctx.account = AccountController(ctx)
    ctx.traffic_light.request_off()

    sw = SwipeController(ctx)
    reader = Reader(usb.reader)
    card_reader = RfidReaderController(ctx)
    card_reader.start(reader)

    window.bind("<Key>", lambda i: sw.keyboard_press(i))
    window.bind("<Escape>", lambda i: clear_and_return(ctx))
    logging.info("Made it to app start")
    window.start()
