import uuid

from screens.main_page import MainPage
from screens.acc_no_waiver import AccNoWaiver
from screens.acc_no_waiver_swipe import AccNoWaiverSwipe
from screens.manual_fill import ManualFill
from screens.check_in_no_id import CheckInNoId
from screens.no_acc_check_in_only import NoAccCheckInOnly
from screens.no_acc_no_waiver import NoAccNoWaiver
from screens.no_acc_no_waiver_swipe import NoAccNoWaiverSwipe
from screens.qr_codes import QRCodes
from screens.user_thank import UserThank
from screens.user_welcome import UserWelcome
from screens.waiver_no_acc import WaiverNoAcc
from screens.waiver_no_acc_swipe import WaiverNoAccSwipe


class NavigationController:
    def __init__(self, window, ctx):
        self.ctx = ctx
        self._window = window
        self._frames = {}
        self._curr = None
        self._frame_uuid = uuid.uuid4().hex

        self._timeouts = {
            AccNoWaiverSwipe: 30000,
            QRCodes: 30000,
            NoAccNoWaiverSwipe: 30000,
        }

        for F in (
            MainPage,
            AccNoWaiver,
            AccNoWaiverSwipe,
            ManualFill,
            CheckInNoId,
            NoAccCheckInOnly,
            NoAccNoWaiver,
            NoAccNoWaiverSwipe,
            QRCodes,
            UserThank,
            UserWelcome,
            WaiverNoAcc,
            WaiverNoAccSwipe,
        ):
            self._frames[F] = F(window.canvas, self)

        self.show_frame(MainPage)

    def show_frame(self, screen_class):
        if self._curr is not None:
            self._frames[self._curr].hide()
        self._curr = screen_class
        self._frame_uuid = uuid.uuid4().hex
        self._frames[screen_class].show()

        if screen_class in self._timeouts:
            uid = self._frame_uuid
            self._window.after(
                self._timeouts[screen_class],
                lambda: self._on_timeout(uid),
            )

    def get_frame(self, screen_class):
        return self._frames[screen_class]

    def get_curr_frame(self):
        return self._curr

    def after(self, ms, fn):
        self._window.after(ms, fn)

    def back_to_main(self):
        self.ctx.traffic_light.request_off()
        self.show_frame(MainPage)

    def go_to_no_id(self):
        self.get_frame(CheckInNoId).clear_entries()
        self.show_frame(CheckInNoId)

    def go_to_manual_fill(self):
        self.get_frame(ManualFill).clear_entries()
        self.show_frame(ManualFill)

    def _on_timeout(self, uid):
        if uid == self._frame_uuid:
            self.back_to_main()
