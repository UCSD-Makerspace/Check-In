from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from misc.asset import Asset
from misc.global_context import context
from ui.base import Screen
from ui.components.styled_button import StyledButton
from ui.components.label import styled_label

if TYPE_CHECKING:
    from controllers.navigation_controller import NavigationController


class SignWaiver(Screen):
    def _build(self, controller: NavigationController) -> None:
        content = QHBoxLayout()
        content.setContentsMargins(50, 0, 50, 0)
        content.setSpacing(50)

        left = QVBoxLayout()
        left.setSpacing(0)

        left.addStretch(5)

        heading = styled_label("Please Wait!", font_size=48, bold=True, align=Qt.AlignmentFlag.AlignRight, width=500)
        left.addWidget(heading, alignment=Qt.AlignmentFlag.AlignHCenter)

        left.addSpacing(8)

        instruction = styled_label(
            "You haven't signed the waiver yet. Please sign it using the QR code on the right",
            font_size=36,
            align=Qt.AlignmentFlag.AlignRight,
            width=500
        )
        left.addWidget(instruction, alignment=Qt.AlignmentFlag.AlignHCenter)

        left.addSpacing(24)

        email_caption = styled_label("Sign using this email:", font_size=18, align=Qt.AlignmentFlag.AlignRight, width=500)
        left.addWidget(email_caption, alignment=Qt.AlignmentFlag.AlignHCenter)

        self._email_label = styled_label("", font_size=18, bold=True, align=Qt.AlignmentFlag.AlignRight, width=500)
        left.addWidget(self._email_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        left.addStretch(7)

        right = QVBoxLayout()
        right.setSpacing(0)
        right.addStretch()

        qr_px = QPixmap(Asset.QR_WAIVER.get_path())
        qr_px = qr_px.scaled(320, 320, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        qr_label = QLabel()
        qr_label.setPixmap(qr_px)
        qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        qr_label.setStyleSheet("background: transparent; border: none;")
        right.addWidget(qr_label)

        right.addSpacing(24)

        done_btn = StyledButton("Done Scanning")
        done_btn.setFixedWidth(280)
        done_btn.clicked.connect(lambda: controller.reset_check_in_session())
        right.addWidget(done_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

        right.addStretch()

        content.addStretch()
        content.addLayout(left)
        content.addLayout(right)
        content.addStretch()

        self.content.addLayout(content)

    def on_show(self) -> None:
        self._email_label.setText(context().session.email)

    def on_hide(self) -> None:
        self._email_label.setText("")
