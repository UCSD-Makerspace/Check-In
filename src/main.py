from tkinter import *
from gui import *
    
if __name__ == "__main__":
    app = gui()
    app.title("Check-In")
    app.geometry("1280x720")
    app.configure(bg = "#153246")

    #app.defaultFont = font.nametofont("TkDefaultFont")
    #app.defaultFont.configure(size=24)

    #app_style = ttk.Style(app)
    #app_style.theme_use("classic")
    #readerThread = Reader()
    #readerThread.start()
    #monitor(app, readerThread)
    #app.bind("<Key>", lambda i: keyboardPress(i))
    app.start()
    