import gspread
import tkinter
from tkinter import *
from AccountNoWaiver import AccountNoWaiver
from MainPage import MainPage



class gui(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
         
        container = Frame(self)

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        self.curr_frame = None        
        
        #TODO: This needs to have the figma frames
        
        """
        for F in (MainPage, AccountNoWaiver):
            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(MainPage)
        """   
        frame = StartPage(container, self)
        self.frames[StartPage] = frame
        self.show_frame(StartPage)
                
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
        
class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
         
        # label of frame Layout 2
        label = Label(self, text ="Startpage")
         
        # putting the grid in its place by using
        # grid
        label.grid(row = 0, column = 4, padx = 10, pady = 10)