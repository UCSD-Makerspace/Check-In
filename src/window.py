import tkinter as tk
from pathlib import Path

ASSETS_PATH = Path(__file__).parent / "assets" / "shared"


class CheckInWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Check-In")
        self.geometry("1280x720")
        self.bind("<Map>", self._on_map)

        self.canvas = tk.Canvas(
            self,
            bg="#153246",
            height=720,
            width=1280,
            bd=0,
            highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True)

        self._bg_photos = []
        bg1 = tk.PhotoImage(file=str(ASSETS_PATH / "image_1.png"))
        self._bg_photos.append(bg1)
        self.canvas.create_image(640.0, 360.0, image=bg1)

        bg2 = tk.PhotoImage(file=str(ASSETS_PATH / "image_2.png"))
        self._bg_photos.append(bg2)
        self.canvas.create_image(639.333984375, 359.333984375, image=bg2)

    def _on_map(self, event):
        self.unbind("<Map>")
        self.attributes("-fullscreen", True)

    def start(self):
        self.mainloop()
