from screen import Screen


class WaiverNoAcc(Screen):
    def _build(self, controller):
        self._text(
            191.0, 258.0, anchor="nw",
            text="Looks like you don't have an\n    account, let's solve that",
            fill="#F5F0E6", font=("Montserrat", 64 * -1),
        )
