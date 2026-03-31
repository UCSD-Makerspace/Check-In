import tkinter as tk

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


def _sim_fill_and_go(nav):
    frm = nav.get_frame(CreateAccountManual)
    frm.clear_entries()
    frm.pid_entry.insert(0, _DEV_PID)
    nav.go_to_create_account_manual()


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
        ("sim barcode swipe",                 _sim_fill_and_go),
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


class DevOverlay:
    def __init__(self, canvas, nav):
        self._canvas = canvas
        self._nav = nav
        self._buttons = []

        self._frame = tk.Frame(canvas, bg="#1a1a2e", relief="solid", bd=1)
        tk.Label(
            self._frame,
            text="DEV NAV",
            bg="#1a1a2e", fg="#aaaaaa",
            font=("Courier", 9, "bold"),
        ).pack(pady=(4, 2), padx=6)

        self._canvas_window = canvas.create_window(
            1270, 715, anchor="se", window=self._frame,
        )

    def update(self, screen_class):
        for btn in self._buttons:
            btn.destroy()
        self._buttons.clear()

        for label, action in TRANSITIONS.get(screen_class, []):
            btn = tk.Label(
                self._frame,
                text=label,
                bg="#2a2a4e", fg="white",
                font=("Courier", 9),
                padx=6, pady=3,
                cursor="hand2",
            )
            btn.pack(fill="x", padx=4, pady=1)
            btn.bind("<Button-1>", lambda e, a=action: a(self._nav))
            btn.bind("<Enter>", lambda e, w=btn: w.configure(bg="#4a4a8e"))
            btn.bind("<Leave>", lambda e, w=btn: w.configure(bg="#2a2a4e"))
            self._buttons.append(btn)

        self._canvas.tag_raise(self._canvas_window)
