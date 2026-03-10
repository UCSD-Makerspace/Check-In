from pathlib import Path
from tkinter import Button
from screen import Screen
import global_

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/acc_no_waiver_swipe_assets")


class AccNoWaiverSwipe(Screen):
    def _build(self, controller):
        img2 = self._photo(ASSETS_PATH / "image_2.png")
        self._image(1042.0, 359.0, image=img2)

        img3 = self._photo(ASSETS_PATH / "image_3.png")
        self._image(408.0, 76.0, image=img3)

        img4 = self._photo(ASSETS_PATH / "image_4.png")
        self._image(408.0, 429.0, image=img4)

        img5 = self._photo(ASSETS_PATH / "image_5.png")
        self._image(395.0, 70.0, image=img5)

        img6 = self._photo(ASSETS_PATH / "image_6.png")
        self._image(750.0, 70.0, image=img6)

        img7 = self._photo(ASSETS_PATH / "image_7.png")
        self._image(1042.0, 328.0, image=img7)

        self._text(
            37.0, 45.0, anchor="nw",
            text="Account Status:", fill="#F5F0E6", font=("Montserrat", 40 * -1),
        )
        self._text(
            430.0, 45.0, anchor="nw",
            text="Waiver Status:", fill="#F5F0E6", font=("Montserrat", 40 * -1),
        )
        self._text(
            45.0, 270.0, anchor="nw",
            text="Please scan the QR code\non the right and sign our \n     waiver",
            fill="#F5F0E6", font=("Montserrat", 48 * -1),
        )

        btn_img = self._photo(ASSETS_PATH / "button_1.png")
        btn = Button(
            self.canvas, image=btn_img,
            borderwidth=0, highlightthickness=0,
            command=self._back_to_main, relief="flat",
        )
        self._window(875.0, 581.0, btn, width=344, height=71)

    def _back_to_main(self):
        from MainPage import MainPage
        global_.traffic_light.set_off()
        global_.app.show_frame(MainPage)
