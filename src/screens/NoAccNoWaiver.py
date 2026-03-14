from .screen import Screen


class NoAccNoWaiver(Screen):
    def _build(self, controller):
        self._text(
            80.0, 180.0, anchor="nw",
            text="Looks like your card isn't registered, \n     let's set up your account.",
            fill="#F5F0E6", font=("Montserrat", 64 * -1),
        )
