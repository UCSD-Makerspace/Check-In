import gspread
import tkinter
import tkinter as tk
from pathlib import Path
from tkinter import ttk
from AccNoWaiver import AccNoWaiver
from MainPage import MainPage



class gui(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
         
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        self.curr_frame = None        
                
        for F in (MainPage, AccNoWaiver):
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