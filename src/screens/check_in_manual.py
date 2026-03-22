from pathlib import Path
from tkinter import Button, END
from .base import Screen
from .components.canvas_entry import CanvasEntry

ASSETS_PATH = Path(__file__).parent.parent / "assets" / "check_in_manual"
SHARED_PATH = Path(__file__).parent.parent / "assets" / "shared"


class CheckInManual(Screen):
    def _build(self, controller):
        self.loading_text_id = None

        logo = self._photo(SHARED_PATH / "button_generic.png")
        self._image(88.0, 90.0, image=logo)

        home_img = self._photo(SHARED_PATH / "icon_home.png")
        home_btn = Button(
            self.canvas, image=home_img, bg="#153246",
            command=lambda: controller.back_to_main(),
            relief="flat", highlightthickness=0, bd=0,
        )
        self._window(53.0, 55.0, home_btn)

        field_img = self._photo(SHARED_PATH / "field.png")
        self._image(640.0, 424.0, image=field_img)

        self._text(
            640.0, 206.0, anchor="center",
            text="If you have already made an\naccount, scan your UCSD barcode\nor enter your PID manually",
            fill="#F5F0E6", font=("Montserrat", 48 * -1), justify="center",
        )
        self._text(
            640.0, 492.0, anchor="center",
            text="PID", fill="#F5F0E6", font=("Montserrat", 24 * -1),
        )

        btn_img = self._photo(ASSETS_PATH / "button_check_in.png")
        btn = Button(
            self.canvas, image=btn_img,
            borderwidth=0, highlightthickness=0,
            command=lambda: self._call_check_in(controller), relief="flat",
        )
        self._window(465.0, 598.0, btn, width=349, height=71)

        self.pid_entry = self._canvas_entry(
            640.0, 424.0, w=800, h=44, font=("Montserrat", 20),
        )

    def hide(self):
        CanvasEntry.blur_all()
        super().hide()

    def display_loading(self):
        if self.loading_text_id is None:
            self.loading_text_id = self.canvas.create_text(
                420.0, 545.0, anchor="nw",
                text="PLEASE WAIT: LOADING...",
                fill="#FF0000", font=("Montserrat", 36 * -1, "bold"), justify="center",
            )

    def clear_entries(self):
        self.pid_entry.delete(0, END)

    def update_entries(self, pid):
        self.pid_entry.insert(0, pid)

    def _call_check_in(self, controller):
        pid = self.pid_entry.get()
        if not pid:
            return

        self.display_loading()
        self.canvas.update_idletasks()
        self.clear_entries()

        self.controller.ctx.check_in.handle_by_pid(pid)

        if self.loading_text_id is not None:
            self.canvas.delete(self.loading_text_id)
            self.loading_text_id = None
