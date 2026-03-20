from .screen import Screen


class NoAccCheckInOnly(Screen):
    def _build(self, controller):
        self._text(
            160.0, 180.0, anchor="nw",
            text="Looks like you don't have an\n account, please scan your ID\nat the main desk",
            fill="#F5F0E6", font=("Montserrat", 64 * -1),
        )
