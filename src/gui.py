import uuid
import tkinter as tk
from pathlib import Path
import global_

ASSETS_PATH = Path(__file__).parent / "assets" / "shared"


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

        from screens.MainPage import MainPage
        from screens.AccNoWaiver import AccNoWaiver
        from screens.AccNoWaiverSwipe import AccNoWaiverSwipe
        from screens.ManualFill import ManualFill
        from screens.CheckInNoId import CheckInNoId
        from screens.NoAccCheckInOnly import NoAccCheckInOnly
        from screens.NoAccNoWaiver import NoAccNoWaiver
        from screens.NoAccNoWaiverSwipe import NoAccNoWaiverSwipe
        from screens.QRCodes import QRCodes
        from screens.UserThank import UserThank
        from screens.UserWelcome import UserWelcome
        from screens.WaiverNoAcc import WaiverNoAcc
        from screens.WaiverNoAccSwipe import WaiverNoAccSwipe

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
        from screens.MainPage import MainPage
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
