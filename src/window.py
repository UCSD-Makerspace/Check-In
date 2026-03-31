from pathlib import Path
from PyQt6.QtWidgets import QMainWindow, QWidget, QStackedWidget
from PyQt6.QtGui import QFontDatabase, QPainter, QPixmap, QColor
from PyQt6.QtCore import QTimer, Qt

ASSETS_PATH = Path(__file__).parent / "assets" / "shared"


class _RootWidget(QWidget):
    """Central widget that paints background_main.png centered on the dark base color."""

    def __init__(self, parent=None):
        super().__init__(parent)
        bg_path = ASSETS_PATH / "background_main.png"
        self._bg = QPixmap(str(bg_path)) if bg_path.exists() else QPixmap()

    def paintEvent(self, event):
        painter = QPainter(self)
        # Dark base fill
        painter.fillRect(self.rect(), QColor("#153246"))
        # Background image centered
        if not self._bg.isNull():
            x = (self.width() - self._bg.width()) // 2
            y = (self.height() - self._bg.height()) // 2
            painter.drawPixmap(x, y, self._bg)


class CheckInWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Check-In")
        self.setFixedSize(1280, 720)

        # Load Montserrat if bundled; falls back to system font
        fonts_dir = Path(__file__).parent.parent / "fonts"
        if fonts_dir.exists():
            for font_file in fonts_dir.glob("*.ttf"):
                QFontDatabase.addApplicationFont(str(font_file))

        self.central = _RootWidget()
        self.setCentralWidget(self.central)

        # Stacked widget fills the central widget; transparent so bg shows through
        self.stacked = QStackedWidget(self.central)
        self.stacked.setGeometry(0, 0, 1280, 720)
        self.stacked.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.stacked.setStyleSheet("background: transparent;")

        self._escape_handler = None

    def set_escape_handler(self, fn):
        self._escape_handler = fn

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape and self._escape_handler:
            self._escape_handler()
        else:
            super().keyPressEvent(event)

    def after(self, ms, fn):
        """Drop-in replacement for tkinter's window.after()."""
        QTimer.singleShot(ms, fn)

    def start(self):
        from PyQt6.QtWidgets import QApplication
        self.showFullScreen()
        QApplication.instance().exec()
