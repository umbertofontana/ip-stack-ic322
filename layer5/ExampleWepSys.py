
import tkinter as tk
from tkinter import ttk
from threading import *

class wepSys(tk.Tk):
    styleRED = ""
    myLabel = ""

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Fire Control")

        frm = ttk.Frame(self, padding=100)
        frm.grid()
        

        self.styleRED = ttk.Style()
        self.styleRED.configure("TButton", background ="#39FF14")

        self.myLabel = ttk.Label(frm, text="Remote Operated First-Strike Laser-Guided\nMissile System", justify = "center")
        self.myLabel.grid(column=0, row=0)
        statusWindow = ttk.Button(frm, text="Status",style="TButton",command =self.threading)
        statusWindow.grid(column=0, row=1)

        #root.mainloop()

    def turnRed(self):
        #styleRED = ttk.Style()
        self.styleRED.configure("TButton", background ="Red")
        #self.myLabel.configure

    def threading(self):
        t1=Thread(target=self.turnRed())
        t1.start()
   

if __name__ == "__main__":
     
    testObj = wepSys()
    testObj.mainloop()
    print("test")


