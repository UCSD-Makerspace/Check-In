from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QPainter, QPainterPath, QColor, QPen, QFont
from PyQt6.QtCore import Qt, QRectF, QRect
import qtawesome as qta

from .theme import OUTER_MARGIN, INNER_MARGIN, NAV_BTN_SIZE, NAV_ICON_SIZE

__all__ = ["StyledButton", "home_button", "OUTER_MARGIN", "INNER_MARGIN", "NAV_BTN_SIZE", "NAV_ICON_SIZE"]


class StyledButton(QPushButton):

    def __init__(self, text="", parent=None, font_size=30, ghost=False, radius=20):
        super().__init__(text, parent)
        self._font_size = font_size
        self._ghost = ghost
        self._radius = radius
        self._hovered = False
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(65)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent; border: none;")

    def enterEvent(self, event):
        self._hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovered = False
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self._ghost:
            half_pen = 2
            rect = QRectF(self.rect()).adjusted(half_pen, half_pen, -half_pen, -half_pen)
            path = QPainterPath()
            path.addRoundedRect(rect, self._radius, self._radius)

            painter.fillPath(path, QColor(255, 255, 255, 30) if self._hovered else QColor(0, 0, 0, 0))

            pen = QPen(QColor(240, 240, 240, 200))
            pen.setWidth(4)
            pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPath(path)

            ico = self.icon()
            if not ico.isNull():
                sz = self.iconSize()
                ico.paint(painter, QRect(
                    (self.width() - sz.width()) // 2,
                    (self.height() - sz.height()) // 2,
                    sz.width(), sz.height(),
                ))
            else:
                painter.setFont(QFont("Montserrat", self._font_size))
                painter.setPen(QColor("#F5F0E6"))
                painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())
        else:
            rect = QRectF(self.rect()).adjusted(1, 1, -1, -1)
            path = QPainterPath()
            path.addRoundedRect(rect, self._radius, self._radius)
            painter.fillPath(path, QColor("#E8E4DA") if self._hovered else QColor("#F5F0E6"))

            painter.setFont(QFont("Montserrat", self._font_size))
            painter.setPen(QColor("#4EBEEE"))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())


def home_button(on_click):
    btn = StyledButton(ghost=True)
    btn.setIcon(qta.icon('fa5s.home', color='#F5F0E6'))
    btn.setIconSize(NAV_ICON_SIZE)
    btn.setFixedSize(NAV_BTN_SIZE, NAV_BTN_SIZE)
    btn.clicked.connect(on_click)
    return btn
