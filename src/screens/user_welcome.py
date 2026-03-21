from .screen import Screen


class UserWelcome(Screen):
    def _build(self, controller):
        self.last_name = None
        self.offset = 0

        self._text(
            99.33203125, 259.33203125, anchor="nw",
            text="Welcome back",
            fill="#F5F0E6", font=("Montserrat", 45 * -1),
        )

    def hide(self):
        super().hide()
        # Clean up any dynamic name items when leaving this screen
        self.canvas.delete("welcome")
        self.last_name = None
        self.offset = 0

    def displayName(self, name):
        if name == self.last_name:
            return

        self.last_name = name

        from .main_page import MainPage
        self.controller.show_frame(UserWelcome)

        text_id = self.canvas.create_text(
            99.0,
            323.0 + self.offset,
            anchor="nw",
            text=name,
            fill="#F5F0E6",
            font=("Montserrat", 73 * -1),
            tag="welcome",
        )

        self.offset += 73
        self.canvas.after(3000, lambda: self._remove_name(text_id))

    def _remove_name(self, text_id):
        from .main_page import MainPage
        self.canvas.delete(text_id)
        self.offset -= 73

        for text in self.canvas.find_withtag("welcome"):
            coords = self.canvas.coords(text)
            if coords[1] > 323.0:
                self.canvas.move(text, 0, -73)

        if not self.canvas.find_withtag("welcome"):
            self.last_name = None
            self.controller.ctx.traffic_light.set_off()
            self.controller.show_frame(MainPage)
