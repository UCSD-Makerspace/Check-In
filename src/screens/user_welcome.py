from PyQt6.QtWidgets import QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer
from .base import Screen
from .components.outline_frame import OutlineFrame
from .components.theme import INNER_MARGIN, OUTER_MARGIN


class UserWelcome(Screen):
    def _build(self, controller):
        self._last_name = None
        self._active_labels: set = set()

        outer = QVBoxLayout(self)
        outer.setContentsMargins(OUTER_MARGIN, OUTER_MARGIN, OUTER_MARGIN, OUTER_MARGIN)
        outer.setSpacing(0)

        outline = OutlineFrame()
        outer.addWidget(outline)

        inner = QVBoxLayout(outline)
        inner.setContentsMargins(INNER_MARGIN, INNER_MARGIN, INNER_MARGIN, INNER_MARGIN)
        inner.setSpacing(0)

        inner.addStretch()

        self._msg_label = QLabel("Welcome back")
        self._msg_label.setStyleSheet(
            "color: #F5F0E6; font: 38pt Montserrat;"
            "background: transparent; border: none;"
        )
        self._msg_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        inner.addWidget(self._msg_label)

        inner.addSpacing(8)

        self._names_layout = QVBoxLayout()
        self._names_layout.setContentsMargins(0, 0, 0, 0)
        self._names_layout.setSpacing(0)
        inner.addLayout(self._names_layout)

        inner.addStretch()

    def on_hide(self):
        self._active_labels.clear()
        while self._names_layout.count():
            item = self._names_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._msg_label.setText("Welcome back")
        self._last_name = None

    def display_name(self, name, message="Welcome back"):
        if name == self._last_name:
            return

        self._last_name = name
        self._msg_label.setText(message)
        self.controller.show_frame(UserWelcome)

        label = QLabel(name)
        label.setStyleSheet(
            "color: #F5F0E6; font: bold 70pt Montserrat;"
            "background: transparent; border: none;"
        )
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self._names_layout.addWidget(label)
        self._active_labels.add(label)

        QTimer.singleShot(3000, lambda: self._remove_name(label))

    def _remove_name(self, label):
        if label not in self._active_labels:
            return
        self._active_labels.discard(label)
        self._names_layout.removeWidget(label)
        label.deleteLater()

        if not self._active_labels:
            self._last_name = None
            self.controller.back_to_main()
