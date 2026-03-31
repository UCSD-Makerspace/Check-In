from pathlib import Path
from tkinter import Button, END
from .base import Screen
from .components.canvas_entry import CanvasEntry
import logging

ASSETS_PATH = Path(__file__).parent.parent / "assets" / "create_account_manual"
SHARED_PATH = Path(__file__).parent.parent / "assets" / "shared"


class CreateAccountReview(Screen):
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
        self._image(640.0, 239.0, image=field_img)
        self._image(640.0, 339.0, image=field_img)
        self._image(640.0, 440.0, image=field_img)
        self._image(640.0, 542.0, image=field_img)

        self._text(
            250.0, 45.0, anchor="nw",
            text="Account Status:", fill="#F5F0E6", font=("Montserrat", 40 * -1),
        )
        self._text(
            670.0, 45.0, anchor="nw",
            text="Waiver Status:", fill="#F5F0E6", font=("Montserrat", 40 * -1),
        )
        self._text(
            640.0, 189.0, anchor="center",
            text="First Name", fill="#F5F0E6", font=("Montserrat", 24 * -1),
        )
        self._text(
            640.0, 290.0, anchor="center",
            text="Last Name", fill="#F5F0E6", font=("Montserrat", 24 * -1),
        )
        self._text(
            640.0, 391.0, anchor="center",
            text="Email", fill="#F5F0E6", font=("Montserrat", 24 * -1),
        )
        self._text(
            640.0, 492.0, anchor="center",
            text="PID", fill="#F5F0E6", font=("Montserrat", 24 * -1),
        )

        btn_img = self._photo(ASSETS_PATH / "register.png")
        btn = Button(
            self.canvas, image=btn_img,
            borderwidth=0, highlightthickness=0,
            command=self._submit, relief="flat",
        )
        self._window(465.0, 598.0, btn, width=349, height=71)

        self.first_name_entry = self._canvas_entry(640.0, 239.0, w=800, h=44, font=("Montserrat", 20))
        self.last_name_entry  = self._canvas_entry(640.0, 339.0, w=800, h=44, font=("Montserrat", 20))
        self.email_entry      = self._canvas_entry(640.0, 440.0, w=800, h=44, font=("Montserrat", 20))
        self.pid_entry        = self._canvas_entry(640.0, 542.0, w=800, h=44, font=("Montserrat", 20))

    def setup(self, first_name="", last_name="", email="", pid="", pid_locked=False):
        self.clear_entries()
        if first_name:
            self.first_name_entry.insert(0, first_name)
        if last_name:
            self.last_name_entry.insert(0, last_name)
        if email:
            self.email_entry.insert(0, email)
        if pid:
            self.pid_entry.insert(0, pid)
        self.pid_entry.set_readonly(pid_locked)

    def hide(self):
        CanvasEntry.blur_all()
        super().hide()

    def clear_entries(self):
        for entry in (self.first_name_entry, self.last_name_entry,
                      self.email_entry, self.pid_entry):
            entry.delete(0, END)
        self.pid_entry.set_readonly(False)

    def _submit(self):
        first = self.first_name_entry.get().strip()
        last  = self.last_name_entry.get().strip()
        email = self.email_entry.get().strip()
        pid   = self.pid_entry.get().strip()
        self.clear_entries()
        try:
            self.controller.ctx.account.create_account_from_review(
                first_name=first, last_name=last, email=email, pid=pid
            )
        except Exception:
            logging.warning("Error occurred trying to create a user account", exc_info=True)
