from tkinter import PhotoImage


class Screen:
    def __init__(self, canvas, controller):
        self.canvas = canvas
        self.controller = controller
        self._items = []
        self._windows = []
        self._photos = []
        self._build(controller)
        self.hide()

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

    def _canvas_entry(self, x, y, w, h, font, fg="#F5F0E6"):
        from .components.canvas_entry import CanvasEntry
        entry = CanvasEntry(self.canvas, x, y, w, h, font, fg)
        self._items.extend(entry.item_ids)
        return entry

    def _window(self, x, y, widget, width=None, height=None):
        kw = dict(anchor="nw", window=widget)
        if width is not None:
            kw["width"] = width
        if height is not None:
            kw["height"] = height
        item = self.canvas.create_window(x, y, **kw)
        self._windows.append(item)
        return item

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
