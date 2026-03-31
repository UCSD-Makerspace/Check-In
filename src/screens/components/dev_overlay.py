from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QTimer

from screens.check_in_rfid import CheckInRFID
from screens.create_account_barcode import CreateAccountBarcode
from screens.create_account_manual import CreateAccountManual
from screens.create_account_no_pid import CreateAccountNoPid
from screens.create_account_review import CreateAccountReview
from screens.sign_waiver import SignWaiver
from screens.check_in_manual import CheckInManual
from screens.qr_codes import QRCodes
from screens.user_welcome import UserWelcome

_DEV_NAME  = "Dev User"
_DEV_EMAIL = "devuser@ucsd.edu"
_DEV_PID   = "A12345678"
_DEV_RFID  = "1a2b3c4d5e6f7g"
_THANK_MSG = "Thank you for registering"


def _sim_no_account_success(nav):
    nav.ctx.rfid = _DEV_RFID
    def on_done():
        nav.ctx.traffic_light.request_green()
        nav.get_frame(UserWelcome).display_name(_DEV_NAME, _THANK_MSG)
    nav.go_to_create_account(on_done=on_done)


def _sim_no_account_needs_waiver(nav):
    nav.ctx.rfid = _DEV_RFID
    nav.go_to_create_account(on_done=nav.go_to_sign_waiver)


def _sim_barcode_swipe(nav):
    nav.go_to_create_account_review(
        pid=_DEV_PID,
        first_name=_DEV_NAME.split()[0],
        last_name=_DEV_NAME.split()[1],
        email=_DEV_EMAIL,
    )


TRANSITIONS = {
    CheckInRFID: [
        ("QR Codes",                          lambda nav: nav.show_frame(QRCodes)),
        ("No ID",                             lambda nav: nav.go_to_no_id()),
        ("card: success",                     lambda nav: nav.get_frame(UserWelcome).display_name(_DEV_NAME)),
        ("card: no account [→ success]",      _sim_no_account_success),
        ("card: no account [→ waiver]",       _sim_no_account_needs_waiver),
        ("card: no waiver",                   lambda nav: nav.go_to_sign_waiver()),
    ],
    QRCodes: [
        ("← Main",                            lambda nav: nav.back_to_main()),
    ],
    CheckInManual: [
        ("← Main",                            lambda nav: nav.back_to_main()),
        ("PID: success",                      lambda nav: nav.get_frame(UserWelcome).display_name(_DEV_NAME)),
        ("PID: no account [→ success]",       _sim_no_account_success),
        ("PID: no account [→ waiver]",        _sim_no_account_needs_waiver),
        ("PID: no waiver",                    lambda nav: nav.go_to_sign_waiver()),
    ],
    CreateAccountBarcode: [
        ("sim barcode swipe",                 _sim_barcode_swipe),
        ("manual fill",                       lambda nav: nav.go_to_create_account_manual()),
        ("← Main",                            lambda nav: nav.back_to_main()),
    ],
    CreateAccountManual: [
        ("→ review (pid lookup)",             lambda nav: nav.ctx.account.go_to_review_from_pid(_DEV_PID)),
        ("→ no-pid screen",                   lambda nav: nav.go_to_create_account_no_pid()),
        ("← Main",                            lambda nav: nav.back_to_main()),
    ],
    CreateAccountNoPid: [
        ("submit",                            lambda nav: nav.pop()),
        ("← Main",                            lambda nav: nav.back_to_main()),
    ],
    CreateAccountReview: [
        ("submit",                            lambda nav: nav.pop()),
        ("← Main",                            lambda nav: nav.back_to_main()),
    ],
    SignWaiver: [
        ("← Main",                            lambda nav: nav.back_to_main()),
    ],
}


class DevOverlay(QWidget):

    def __init__(self, window, nav):
        super().__init__(window.central)
        self._nav = nav
        self._stacked = window.stacked
        self._buttons: list[QPushButton] = []

        self.setStyleSheet("QWidget { background-color: #1a1a2e; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(2)

        header = QLabel("DEV NAV")
        header.setStyleSheet(
            "color: #aaaaaa; font: bold 9pt Courier;"
            "background: transparent; border: none;"
        )
        header.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(header)

        self._layout = layout

    def update(self, screen_class):
        while self._layout.count() > 1:
            item = self._layout.takeAt(1)
            w = item.widget()
            if w:
                w.setParent(None)
        self._buttons.clear()

        for label, action in TRANSITIONS.get(screen_class, []):
            btn = QPushButton(label)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2a2a4e;
                    color: white;
                    font: 9pt Courier;
                    padding: 3px 6px;
                    border: none;
                    text-align: left;
                }
                QPushButton:hover { background-color: #4a4a8e; }
            """)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, a=action: a(self._nav))
            self._layout.addWidget(btn)
            self._buttons.append(btn)

        QTimer.singleShot(0, self._refresh)

    def _refresh(self):
        self.adjustSize()
        self._reposition()
        self.raise_()
        self.show()

    def _reposition(self):
        s = self._stacked
        self.move(
            s.x() + s.width()  - self.width()  - 10,
            s.y() + s.height() - self.height() - 10,
        )
