from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QResizeEvent

from .label import field_label
from ui.theme import ACCENT, CREAM, DARK, ERROR, READONLY_TEXT, app_font

_SUFFIX_INSET = 16


class StyledEntry(QLineEdit):

    def __init__(self, parent: QWidget | None = None, font_size: int = 20) -> None:
        super().__init__(parent)
        self.setMinimumHeight(54)
        self.setFont(app_font(font_size))
        self._readonly = False
        self._error = False
        self._apply_style()

        self._suffix_label = QLabel(self)
        self._suffix_label.setFont(self.font())
        self._suffix_label.setStyleSheet(f"color: {READONLY_TEXT}; background: transparent;")
        self._suffix_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self._suffix_label.hide()

    def set_suffix(self, suffix: str | None) -> None:
        if not suffix:
            self._suffix_label.hide()
            self.setTextMargins(0, 0, 0, 0)
            return
        self._suffix_label.setText(suffix)
        self._suffix_label.adjustSize()
        self._suffix_label.show()
        self.setTextMargins(0, 0, self._suffix_label.width(), 0)
        self._position_suffix()

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self._position_suffix()

    def _position_suffix(self) -> None:
        label = self._suffix_label
        label.move(
            self.width() - label.width() - _SUFFIX_INSET,
            (self.height() - label.height()) // 2,
        )

    def _apply_style(self) -> None:
        text_color = READONLY_TEXT if self._readonly else CREAM
        border_color = ERROR if self._error else CREAM
        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: rgba(0, 0, 0, 80);
                border: 2px solid {border_color};
                border-radius: 12px;
                color: {text_color};
                padding: 6px 14px;
                selection-background-color: {ACCENT};
                selection-color: {DARK};
            }}
        """)

    def set_readonly(self, readonly: bool) -> None:
        self.setReadOnly(readonly)
        self._readonly = readonly
        self._apply_style()

    def set_error(self, error: bool) -> None:
        if error != self._error:
            self._error = error
            self._apply_style()


def field_row(
    layout: QVBoxLayout,
    label_text: str,
    *,
    max_width: int = 800,
    spacing: int = 8,
) -> StyledEntry:
    layout.addWidget(field_label(label_text), alignment=Qt.AlignmentFlag.AlignHCenter)

    row = QHBoxLayout()
    entry = StyledEntry()
    entry.setMaximumWidth(max_width)
    row.addStretch()
    row.addWidget(entry)
    row.addStretch()
    layout.addLayout(row)

    if spacing:
        layout.addSpacing(spacing)

    return entry
