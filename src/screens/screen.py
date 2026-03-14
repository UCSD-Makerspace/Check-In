from tkinter import PhotoImage


class Screen:
    """Base class for all check-in screens drawn on the shared canvas."""

    def __init__(self, canvas, controller):
        self.canvas = canvas
        self.controller = controller
        self._items = []    # canvas item IDs (text, image)
        self._windows = []  # canvas window IDs (Button, Entry)
        self._photos = []   # PhotoImage refs — prevent garbage collection
        self._build(controller)
        self.hide()

    # ------------------------------------------------------------------
    # Helpers for subclasses
    # ------------------------------------------------------------------

    def _photo(self, path):
        img = PhotoImage(file=str(path))
        self._photos.append(img)
        return img

    def _image(self, x, y, **kwargs):
        item = self.canvas.create_image(x, y, **kwargs)
        self._items.append(item)
        return item

    def _text(self, x, y, **kwargs):
        item = self.canvas.create_text(x, y, **kwargs)
        self._items.append(item)
        return item

    def _window(self, x, y, widget, width=None, height=None):
        """Embed a tk widget into the canvas.  x, y = top-left corner."""
        kw = dict(anchor="nw", window=widget)
        if width is not None:
            kw["width"] = width
        if height is not None:
            kw["height"] = height
        item = self.canvas.create_window(x, y, **kw)
        self._windows.append(item)
        return item

    # ------------------------------------------------------------------
    # Visibility
    # ------------------------------------------------------------------

    def show(self):
        for item in self._items:
            self.canvas.itemconfigure(item, state="normal")
        for win in self._windows:
            self.canvas.itemconfigure(win, state="normal")

    def hide(self):
        for item in self._items:
            self.canvas.itemconfigure(item, state="hidden")
        for win in self._windows:
            self.canvas.itemconfigure(win, state="hidden")

    # Subclasses implement this instead of __init__
    def _build(self, controller):
        pass
