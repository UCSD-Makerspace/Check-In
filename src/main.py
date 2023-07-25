from tkinter import *
from gui import *
from swipe import *


if __name__ == "__main__":
    app = gui()
    app.title("Check-In")
    app.geometry("1280x720")
    #TODO: Screen is gonna need to be set to 720p  
    #app.attributes("-fullscreen", True)
    
    app.bind("1", lambda i: app.show_frame(MainPage))
    app.bind("2", lambda i: app.show_frame(AccNoWaiver))
    app.bind("3", lambda i: app.show_frame(AccNoWaiverSwipe))
    app.bind("4", lambda i: app.show_frame(ManualFill))
    app.bind("5", lambda i: app.show_frame(NoAccNoWaiver))
    app.bind("6", lambda i: app.show_frame(NoAccNoWaiverSwipe))
    app.bind("7", lambda i: app.show_frame(QRCodes))
    app.bind("8", lambda i: app.show_frame(UserThank))
    app.bind("9", lambda i: app.show_frame(UserWelcome))
    app.bind("0", lambda i: app.show_frame(WaiverNoAcc))
    app.bind("-", lambda i: app.show_frame(WaiverNoAccSwipe))

    #readerThread = Reader()
    #readerThread.start()
    #monitor(app, readerThread)
    app.bind("<Key>", lambda i: swipe.keyboardPress(i))
    app.start()
