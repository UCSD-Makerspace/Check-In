from .screen import Screen


class AccNoWaiver(Screen):
    def _build(self, controller):
        self._text(
            169.0, 258.0, anchor="nw",
            text="Looks like you haven't signed\n  the waiver, let's solve that",
            fill="#F5F0E6", font=("Montserrat", 64 * -1),
        )
