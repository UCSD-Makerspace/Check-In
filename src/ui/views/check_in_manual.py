from __future__ import annotations

import re
from typing import TYPE_CHECKING, Literal

from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtCore import Qt

from misc.api_models import UCSD_EMAIL_DOMAIN
from misc.global_context import context
from ui.base import Screen
from ui.components.styled_button import StyledButton
from ui.components.styled_entry import field_row
from ui.components.label import styled_label

if TYPE_CHECKING:
    from controllers.navigation_controller import NavigationController


_PID_PATTERN = re.compile(r"[A-Za-z]?\d+")


def parse_identifier(value: str) -> tuple[Literal["pid", "email"], str]:
    if "@" in value:
        return "email", value
    if _PID_PATTERN.fullmatch(value):
        return "pid", value
    return "email", value + UCSD_EMAIL_DOMAIN


class CheckInManual(Screen):
    def _build(self, controller: NavigationController) -> None:
        self.add_home_row()

        self.content.addStretch(2)

        instruction = styled_label(
            "Enter your UCSD PID or email\n"
            "below to check in",
            font_size=36,
        )
        self.content.addWidget(instruction, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.content.addStretch(1)

        self.id_entry = field_row(self.content, "PID or Email", spacing=0)
        self.id_entry.returnPressed.connect(lambda: self._call_check_in())

        self.content.addStretch(2)

        btn_row = QHBoxLayout()
        self.check_in_btn = StyledButton("Check In")
        self.check_in_btn.setFixedWidth(349)
        self.check_in_btn.setEnabled(False)
        self.check_in_btn.clicked.connect(lambda: self._call_check_in())
        self.id_entry.textChanged.connect(self._update_btn_state)
        btn_row.addStretch()
        btn_row.addWidget(self.check_in_btn)
        btn_row.addStretch()
        self.content.addLayout(btn_row)

    def _update_btn_state(self) -> None:
        self.check_in_btn.setEnabled(bool(self.id_entry.text().strip()))

    def on_show(self) -> None:
        self.id_entry.setFocus()

    def on_hide(self) -> None:
        self.id_entry.clearFocus()
        self.clear_entries()

    def clear_entries(self) -> None:
        self.id_entry.clear()

    def update_entries(self, identifier: str) -> None:
        self.id_entry.setText(identifier)

    def _call_check_in(self) -> None:
        value = self.id_entry.text().strip()
        if not value:
            return
        self.clear_entries()
        method, identifier = parse_identifier(value)
        context().check_in_controller.check_in(method, identifier)
