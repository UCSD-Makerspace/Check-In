from PyQt6.QtWidgets import QWidget


class Screen(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._build(controller)

    def _build(self, controller):
        """Subclasses build their UI here instead of in __init__."""
        pass

    def on_show(self):
        """Called by NavigationController when this screen becomes visible."""
        pass

    def on_hide(self):
        """Called by NavigationController just before this screen is hidden."""
        pass
