import uuid
import tkinter as tk
from pathlib import Path
from app_context import AppContext

ASSETS_PATH = Path(__file__).parent / "assets" / "shared"


#################################################
# Acts as the controller and the user interface #
#################################################
class Gui(tk.Tk):
    def __init__(self, ctx: AppContext, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.ctx = ctx

        self.title("Check-In")
        self.geometry("1280x720")
        self.bind("<Map>", self._on_map)

        # Single shared canvas — background is always painted here, never redrawn
        self.canvas = tk.Canvas(
            self,
            bg="#153246",
            height=720,
            width=1280,
            bd=0,
            highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True)

        # Load background images once and draw them permanently
        self._bg_photos = []
        bg1 = tk.PhotoImage(file=str(ASSETS_PATH / "image_1.png"))
        self._bg_photos.append(bg1)
        self.canvas.create_image(640.0, 360.0, image=bg1)

        bg2 = tk.PhotoImage(file=str(ASSETS_PATH / "image_2.png"))
        self._bg_photos.append(bg2)
        self.canvas.create_image(639.333984375, 359.333984375, image=bg2)

        self.frames = {}
        self.curr_frame = None
        self.frame_uuid = uuid.uuid4().hex

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
            self.frames[F] = F(self.canvas, self)

        self.show_frame(MainPage)

    def _on_map(self, event):
        self.unbind("<Map>")
        self.attributes("-fullscreen", True)

    def timeout_fn(self, curr_uuid):
        from screens.main_page import MainPage
        if curr_uuid == self.frame_uuid:
            self.show_frame(MainPage)
            self.ctx.traffic_light.set_off()

    def show_frame(self, cont):
        if self.curr_frame is not None:
            self.frames[self.curr_frame].hide()
        self.curr_frame = cont
        self.frame_uuid = uuid.uuid4().hex
        self.frames[cont].show()

        if cont in self._timeouts:
            curr_uuid = self.frame_uuid
            self.after(self._timeouts[cont], lambda: self.timeout_fn(curr_uuid))

    def get_frame(self, cont):
        return self.frames[cont]

    def get_curr_frame(self):
        return self.curr_frame

    def start(self):
        self.mainloop()
