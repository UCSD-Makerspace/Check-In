from .screen import Screen


class UserThank(Screen):
    def _build(self, controller):
        self._text(
            99.33203125, 259.33203125, anchor="nw",
            text="Thank you for registering",
            fill="#F5F0E6", font=("Montserrat", 45 * -1),
        )
        self._text(
            429.0, 550.0, anchor="nw",
            text="UCSD Makerspace",
            fill="#F5F0E6", font=("Montserrat", 45 * -1),
        )

    def hide(self):
        super().hide()
        self.canvas.delete("thank")

    def display_name(self, name, nextPage):
        self.controller.show_frame(UserThank)
        self.controller.ctx.account.on_thank_start(nextPage)

        self.canvas.create_text(
            99.0, 323.0, anchor="nw",
            text=name,
            fill="#F5F0E6",
            font=("Montserrat", 73 * -1),
            tag="thank",
        )

        self.canvas.after(4500, lambda: self.canvas.delete("thank"))
        self.controller.after(4000, lambda: self._go_to_next(nextPage))

    def _go_to_next(self, nextPage):
        self.controller.ctx.account.on_thank_done(nextPage)
