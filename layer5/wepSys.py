from tkinter import *
from tkinter import ttk
import simple_app as SimpleApp


class wepSys(simpleApp):
    root = Tk()
    root.title("Fire Control")
    frm = ttk.Frame(root, padding=100)
    frm.grid()

    styleRED = ttk.Style()
    styleRED.configure("TButton", background ="#39FF14")
        #foreground = "Red", 
    ttk.Label(frm, text="Remote Operated First-Strike Laser-Guided\nMissile System", justify = "center").grid(column=0, row=0)

    statusWindow = ttk.Label(frm, text="Status",style="TButton")
    statusWindow.grid(column=0, row=1)
    root.mainloop()


def turnRed(statusWindow):
    print("Turning red")
    statusWindow.configure(background = "Red")
    


