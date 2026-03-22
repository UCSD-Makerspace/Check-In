from pathlib import Path
from tkinter import Button, END
from .base import Screen
from .components.canvas_entry import CanvasEntry
import logging

ASSETS_PATH = Path(__file__).parent.parent / "assets" / "create_account_manual"
SHARED_PATH = Path(__file__).parent.parent / "assets" / "shared"


class CreateAccountManual(Screen):
    def _build(self, controller):
        logo = self._photo(SHARED_PATH / "button_generic.png")
        self._image(88.0, 90.0, image=logo)

        home_img = self._photo(SHARED_PATH / "icon_home.png")
        home_btn = Button(
            self.canvas, image=home_img, bg="#153246",
            command=lambda: controller.back_to_main(),
            relief="flat", highlightthickness=0, bd=0,
        )
        self._window(53.0, 55.0, home_btn)

        outline1_img = self._photo(ASSETS_PATH / "outline_1.png")
        self._image(640.0, 76.0, image=outline1_img)

        outline2_img = self._photo(ASSETS_PATH / "outline_2.png")
        self._image(640.0, 430.0, image=outline2_img)

        icon_unchecked = self._photo(SHARED_PATH / "icon_unchecked_box.png")
        self._image(605.0, 77.0, image=icon_unchecked)
        self._image(1010.0, 77.0, image=icon_unchecked)

        field_img = self._photo(SHARED_PATH / "field.png")
        self._image(640.0, 390.0, image=field_img)

        self._text(
            250.0, 45.0, anchor="nw",
            text="Account Status:", fill="#F5F0E6", font=("Montserrat", 40 * -1),
        )
        self._text(
            670.0, 45.0, anchor="nw",
            text="Waiver Status:", fill="#F5F0E6", font=("Montserrat", 40 * -1),
        )
        self._text(
            640.0, 340.0, anchor="center",
            text="PID", fill="#F5F0E6", font=("Montserrat", 24 * -1),
        )

        btn_img = self._photo(ASSETS_PATH / "register.png")
        btn = Button(
            self.canvas, image=btn_img,
            borderwidth=0, highlightthickness=0,
            command=self._call_account_creation, relief="flat",
        )
        self._window(465.0, 490.0, btn, width=349, height=71)

        self.pid_entry = self._canvas_entry(640.0, 390.0, w=800, h=44, font=("Montserrat", 20))

    def hide(self):
        CanvasEntry.blur_all()
        super().hide()

    def clear_entries(self):
        self.pid_entry.delete(0, END)

    def _call_account_creation(self):
        pid = self.pid_entry.get()
        self.clear_entries()
        try:
            self.controller.ctx.account.create_account_from_pid(pid)
        except Exception:
            logging.warning("Error occurred trying to create a user account", exc_info=True)
