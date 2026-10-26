import qtawesome as qta
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFocusEvent, QResizeEvent

from .label import field_label
from ui.theme import ACCENT, CREAM, DARK, ERROR, READONLY_TEXT, app_font

_BORDER = 2
_PADDING_X = 14
_TEXT_INSET = _BORDER + _PADDING_X

_TAP_HINT_TEXT = "Tap to select"
_TAP_ICON_SIZE = 24
_TAP_ICON_GAP = 8


class StyledEntry(QLineEdit):
    focus_changed = pyqtSignal()

    def __init__(self, parent: QWidget | None = None, font_size: int = 20) -> None:
        super().__init__(parent)
        self.setMinimumHeight(54)
        self.setFont(app_font(font_size))
        self._readonly = False
        self._error = False
        self._tap_hint_enabled = True
        self._apply_style()

        self._suffix_label = QLabel(self)
        self._suffix_label.setFont(self.font())
        self._suffix_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self._suffix_label.setStyleSheet(f"color: {READONLY_TEXT}; background: transparent;")
        self._suffix_label.hide()

        self._tap_icon = QLabel(self)
        self._tap_icon.setPixmap(qta.icon("mdi.gesture-tap", color=READONLY_TEXT).pixmap(_TAP_ICON_SIZE, _TAP_ICON_SIZE))
        self._tap_icon.adjustSize()
        self._tap_icon.setStyleSheet("background: transparent;")
        self._tap_icon.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self._tap_icon.hide()

        self.textChanged.connect(self._update_overlays)
        self.cursorPositionChanged.connect(self._position_overlays)
        self._update_overlays()

    def set_suffix(self, suffix: str | None) -> None:
        self._suffix_label.setText(suffix or "")
        self._suffix_label.adjustSize()
        self._update_overlays()

    def set_tap_hint_enabled(self, enabled: bool) -> None:
        self._tap_hint_enabled = enabled
        self._update_overlays()

    def resizeEvent(self, event: QResizeEvent | None) -> None:
        super().resizeEvent(event)
        self._position_overlays()

    def focusInEvent(self, event: QFocusEvent | None) -> None:
        super().focusInEvent(event)
        self._update_overlays()
        self.focus_changed.emit()

    def focusOutEvent(self, event: QFocusEvent | None) -> None:
        super().focusOutEvent(event)
        self._update_overlays()
        self.focus_changed.emit()

    def _update_overlays(self) -> None:
        show_tap_hint = self._tap_hint_enabled and not self.text() and not self.hasFocus() and not self._readonly
        has_suffix = bool(self._suffix_label.text())

        self._tap_icon.setVisible(show_tap_hint)
        self.setPlaceholderText(_TAP_HINT_TEXT if show_tap_hint else "")
        self._suffix_label.setVisible(has_suffix and (bool(self.text()) or self.hasFocus()))

        self.setTextMargins(
            _TAP_ICON_SIZE + _TAP_ICON_GAP if show_tap_hint else 0,
            0,
            self._suffix_label.width() if has_suffix else 0,
            0,
        )
        self._position_overlays()

    def _position_overlays(self) -> None:
        icon = self._tap_icon
        icon.move(_TEXT_INSET, (self.height() - icon.height()) // 2)

        label = self._suffix_label
        text_end = self.cursorRect().center().x() + self.fontMetrics().horizontalAdvance(self.text()[self.cursorPosition():])
        label.move(
            min(text_end, self.width() - label.width() - _TEXT_INSET),
            (self.height() - label.height()) // 2,
        )

    def _apply_style(self) -> None:
        text_color = READONLY_TEXT if self._readonly else CREAM
        border_color = ERROR if self._error else CREAM
        focus_border_color = border_color if self._error or self._readonly else ACCENT
        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: rgba(0, 0, 0, 80);
                border: {_BORDER}px solid {border_color};
                border-radius: 12px;
                color: {text_color};
                padding: 6px {_PADDING_X}px;
                selection-background-color: {ACCENT};
                selection-color: {DARK};
            }}
            QLineEdit:focus {{
                border-color: {focus_border_color};
            }}
        """)

    def set_readonly(self, readonly: bool) -> None:
        self.setReadOnly(readonly)
        self._readonly = readonly
        self._apply_style()
        self._update_overlays()

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
