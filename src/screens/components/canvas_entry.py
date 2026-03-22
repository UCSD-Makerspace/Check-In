import tkinter as tk

_focused = None


class CanvasEntry:
    def __init__(self, canvas, x, y, w, h, font, fg="#F5F0E6"):
        self.canvas = canvas
        self._x = x
        self._y = y

        canvas.configure(insertbackground=fg, insertontime=600, insertofftime=400)

        self._hit_id = canvas.create_rectangle(
            x - w / 2, y - h / 2, x + w / 2, y + h / 2,
            fill="", outline="", state="hidden",
        )
        self._text_id = canvas.create_text(
            x, y, text="", fill=fg, font=font,
            anchor="center", state="hidden",
        )

        canvas.tag_bind(self._hit_id, "<Button-1>", self._on_click)
        canvas.tag_bind(self._text_id, "<Button-1>", self._on_click)

    @property
    def item_ids(self):
        return [self._hit_id, self._text_id]

    def _on_click(self, event=None):
        global _focused
        if _focused and _focused is not self:
            _focused._blur()
        _focused = self
        self.canvas.focus_set()
        self.canvas.focus(self._text_id)
        self.canvas.bind("<Key>", _dispatch_key)
        if event:
            idx = self.canvas.index(self._text_id, f"@{event.x},{event.y}")
            self.canvas.icursor(self._text_id, idx)
        else:
            self.canvas.icursor(self._text_id, tk.END)

    def _blur(self):
        global _focused
        if _focused is self:
            _focused = None
        self.canvas.focus("")

    @classmethod
    def blur_all(cls):
        global _focused
        if _focused:
            _focused._blur()

    def get(self):
        return self.canvas.itemcget(self._text_id, "text")

    def delete(self, start, end=None):
        self.canvas.dchars(self._text_id, 0, tk.END)

    def insert(self, index, text):
        self.canvas.insert(self._text_id, index, text)


def _dispatch_key(event):
    if _focused:
        if event.keysym == "BackSpace":
            idx = _focused.canvas.index(_focused._text_id, tk.INSERT)
            if idx > 0:
                _focused.canvas.dchars(_focused._text_id, idx - 1, idx - 1)
        elif event.char and event.char.isprintable():
            _focused.canvas.insert(_focused._text_id, tk.INSERT, event.char)
