import tkinter
import tkinter as tk
from AccNoWaiver import AccNoWaiver
from MainPage import MainPage
from AccNoWaiverSwipe import AccNoWaiverSwipe
from ManualFill import ManualFill
from NoAccNoWaiver import NoAccNoWaiver
from NoAccNoWaiverSwipe import NoAccNoWaiverSwipe
from QRCodes import QRCodes
from UserThank import UserThank
from UserWelcome import UserWelcome
from WaiverNoAcc import WaiverNoAcc
from WaiverNoAccSwipe import WaiverNoAccSwipe



class gui(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.title("Check-In")
        self.geometry("1280x720")
         
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        self.curr_frame = None        
                
        for F in (MainPage, AccNoWaiver, AccNoWaiverSwipe, ManualFill, NoAccNoWaiver, NoAccNoWaiverSwipe, QRCodes, UserThank, UserWelcome, WaiverNoAcc, WaiverNoAccSwipe):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(MainPage)
             
    def show_frame(self, cont):
        frame = self.frames[cont]
        self.curr_frame = cont
        frame.tkraise()

    def get_frame(self, cont):
        return self.frames[cont]

    def get_curr_frame(self):
        return self.curr_frame
    
    def start(self):
        self.mainloop()