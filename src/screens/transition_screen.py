from .base import Screen


class TransitionScreen(Screen):
    def _build(self, controller):
        self._msg_id = self._text(
            640, 340, anchor="center",
            text="",
            fill="#F5F0E6", font=("Montserrat", 64 * -1),
            justify="center",
        )

    def display(self, message):
        self.canvas.itemconfigure(self._msg_id, text=message)
        self.controller.show_frame(TransitionScreen)
