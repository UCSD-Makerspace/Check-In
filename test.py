from tkinter import Tk, Label

root=Tk()

def key_pressed(event):
    print(event.char)
    return

root.bind("<Key>",key_pressed)

root.mainloop()