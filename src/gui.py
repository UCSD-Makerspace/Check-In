import uuid
import tkinter as tk
from pathlib import Path
import global_

ASSETS_PATH = Path(__file__).parent / "assets" / "main_page_assets"


#################################################
# Acts as the controller and the user interface #
#################################################
class gui(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Check-In")
        self.geometry("1280x720")
        self.after(10000, lambda: self.attributes("-fullscreen", True))

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

        # Import here to avoid circular imports at module level
        from MainPage import MainPage
        from AccNoWaiver import AccNoWaiver
        from AccNoWaiverSwipe import AccNoWaiverSwipe
        from ManualFill import ManualFill
        from CheckInNoId import CheckInNoId
        from NoAccCheckInOnly import NoAccCheckInOnly
        from NoAccNoWaiver import NoAccNoWaiver
        from NoAccNoWaiverSwipe import NoAccNoWaiverSwipe
        from QRCodes import QRCodes
        from UserThank import UserThank
        from UserWelcome import UserWelcome
        from WaiverNoAcc import WaiverNoAcc
        from WaiverNoAccSwipe import WaiverNoAccSwipe

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

    def timeout_fn(self, curr_uuid):
        if curr_uuid == self.frame_uuid:
            self.show_frame(MainPage)
            global_.traffic_light.set_off()

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
