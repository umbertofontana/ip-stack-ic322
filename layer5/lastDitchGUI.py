import tkinter as tk
from tkinter import *
from tkinter import ttk
from threading import *
import user as User

class lastDitchGUI(tk.Tk):

    #Build window
    window = Tk() 
    window.title("M.E.N.T.O.S.")
    window.geometry('800x800')
    
    frm = ttk.Frame(window, padding= '0.3i',takefocus=True, height = '3i', width = '3i')
    self.input=Entry(width=30)
    self.enterbutton=Button(win, text='Send Message', command=self.updateChat)
    self.enterbutton.place(x=250, y=40)
    

    ttk.Label(frm, text="Username").grid(column=0,row=0)
    ttk.Label(frm, text="Password").grid(column=0,row=1)
    
    '''
    #Build log in frame
    def __init__(self):
        #Build window
        window = Tk() 
        window.title("M.E.N.T.O.S. Login")
        window.geometry('800x800')
        
        #Build login frame
        frm = ttk.Frame(window, padding= '0.3i',takefocus=True, height = '3i', width = '3i')
        ttk.Label(frm, text="Username").grid(column=0,row=0)
        ttk.Label(frm, text="Password").grid(column=0,row=1)
        
        #initialize variables to hold user input
        username = ""
        password = ""

        #take in user input via textbox
        name = ttk.Entry(frm, textvariable=username).grid(column=0,row=1)
        passwordInput = ttk.Entry(frm, textvariable=password,show ="*").grid(column=1,row=1)
        

        #on click event to check login
        
        loginButton = ttk.Button(frm, text="Login", command=self.loginAttempt().grid(column=2,row=1))
        window.mainloop() 
        
    def loginAttempt(self):
        #build user object based on user input for password
        loginTry = User.User(self.username)
        #check password given versus hash supplied via user.py
        success = loginTry.passCheck(self.password)
        
        if success:
            print("true")

if __name__ == "__main__":
    testObj = lastDitchGUI()
    testObj.mainloop()
'''




