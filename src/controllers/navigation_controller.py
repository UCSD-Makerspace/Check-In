import uuid

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import QLabel

from views.check_in_rfid import CheckInRFID
from views.transition_screen import TransitionScreen
from views.create_account_barcode import CreateAccountBarcode
from views.create_account_manual import CreateAccountManual
from views.create_account_no_pid import CreateAccountNoPid
from views.create_account_review import CreateAccountReview
from views.sign_waiver import SignWaiver
from views.check_in_manual import CheckInManual
from views.qr_codes import QRCodes
from views.user_welcome import UserWelcome


class NavigationController:
    def __init__(self, window, ctx, dev_mode=False):
        self.ctx = ctx
        self._window = window
        self._stacked = window.stacked
        self._frames = {}
        self._curr = None
        self._frame_uuid = uuid.uuid4().hex
        self._on_done_stack = []
        self._dev_overlay = None

        self._timeouts = {
            SignWaiver: 30000,
            QRCodes: 30000,
        }

        for F in (
                CheckInRFID,
                TransitionScreen,
                CreateAccountBarcode,
                CreateAccountManual,
                CreateAccountNoPid,
                CreateAccountReview,
                SignWaiver,
                CheckInManual,
                QRCodes,
                UserWelcome,
        ):
            frame = F(self)
            self._frames[F] = frame
            self._stacked.addWidget(frame)

        # Status overlay — floats over the stacked widget at the bottom
        self._status_label = QLabel("", window.central)
        self._status_label.setGeometry(40, 628, 1200, 56)
        self._status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._status_label.setStyleSheet(
            "color: #F5F0E6;"
            "font: bold 18pt Montserrat;"
            "background-color: rgba(0, 0, 0, 170);"
            "border-radius: 10px;"
            "border: none;"
        )
        self._status_label.hide()
        self._status_label.raise_()

        if dev_mode:
            from views.components.dev_overlay import DevOverlay
            self._dev_overlay = DevOverlay(window, self)

        self.show_frame(CheckInRFID)

    # ------------------------------------------------------------------
    # Core frame switching
    # ------------------------------------------------------------------

    def show_frame(self, screen_class):
        if self._curr is not None:
            self._frames[self._curr].on_hide()
        self._curr = screen_class
        self._frame_uuid = uuid.uuid4().hex
        self._stacked.setCurrentWidget(self._frames[screen_class])
        self._frames[screen_class].on_show()

        if self._dev_overlay is not None:
            self._dev_overlay.update(screen_class)

        if screen_class in self._timeouts:
            uid = self._frame_uuid
            QTimer.singleShot(
                self._timeouts[screen_class],
                lambda: self._on_timeout(uid),
            )

    def get_frame(self, screen_class):
        return self._frames[screen_class]

    def get_curr_frame(self):
        return self._curr

    # ------------------------------------------------------------------
    # Status overlay
    # ------------------------------------------------------------------

    def show_status(self, text):
        self._status_label.setText(text)
        self._status_label.show()
        self._status_label.raise_()

    def hide_status(self):
        self._status_label.hide()

    # ------------------------------------------------------------------
    # Stack-based flow
    # ------------------------------------------------------------------

    def push(self, screen_class, on_done=None):
        self._on_done_stack.append(on_done)
        self.show_frame(screen_class)

    def pop(self):
        cb = self._on_done_stack.pop() if self._on_done_stack else None
        if cb:
            cb()
        else:
            self.back_to_main()

    # ------------------------------------------------------------------
    # Named navigations
    # ------------------------------------------------------------------

    def back_to_main(self):
        self._on_done_stack.clear()
        self.ctx.rfid = ""
        self.ctx.traffic_light.request_off()
        self.show_frame(CheckInRFID)

    def go_to_no_id(self):
        self.get_frame(CheckInManual).clear_entries()
        self.show_frame(CheckInManual)

    def go_to_create_account_manual(self):
        self.get_frame(CreateAccountManual).clear_entries()
        self.show_frame(CreateAccountManual)

    def go_to_create_account_no_pid(self):
        self.get_frame(CreateAccountNoPid).clear_entries()
        self.show_frame(CreateAccountNoPid)

    def go_to_create_account_review(self, pid="", first_name="", last_name="", email=""):
        pid_locked = bool(pid)
        self.get_frame(CreateAccountReview).setup(
            first_name=first_name,
            last_name=last_name,
            email=email,
            pid=pid,
            pid_locked=pid_locked,
        )
        self.show_frame(CreateAccountReview)

    def go_to_create_account(self, on_done):
        self.get_frame(TransitionScreen).display(
            "Looks like you don't have an account,\nlet's set one up!"
        )
        QTimer.singleShot(3000, lambda: self.push(CreateAccountBarcode, on_done=on_done))

    def go_to_sign_waiver(self):
        self.get_frame(TransitionScreen).display(
            "Looks like you haven't signed\nthe waiver yet,\nlet's fix that!"
        )
        QTimer.singleShot(3000, lambda: self.show_frame(SignWaiver))

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _on_timeout(self, uid):
        if uid == self._frame_uuid:
            self.back_to_main()
