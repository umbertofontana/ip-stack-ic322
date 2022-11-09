from tkinter import *
import random
import user
import os
import subprocess
from subprocess import Popen, PIPE, STDOUT
from threading import Thread

class MyWindow:
    
    def __init__(self, win):
        self.chat = StringVar()
        self.chat.set("LOGIN with STDIN")

        username = input("Username: ")
        self.user = user.User(username)
        
        self.ownlabel=Label(win, text=username.capitalize() + " Panel")
        self.ownlabel.place(x=380,y=42)
        if (username == 'ops'):
            self.fire = Button(win, text='FIRE',command=self.launch)
            self.fire.place(x=380, y=60)

        self.status = Button(win, text='Update status',command=self.status)
        self.status.place(x=380, y=80)


        self.chat.set("Welcome, " + username.upper() + "\n---------------------")
        #self.p = Popen(['nc','-l','-p','12345'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        self.chatbox=Label(win, textvariable=self.chat, justify=LEFT)
        self.chatdata = ""
        
        self.input=Entry(width=30)
        self.enterbutton=Button(win, text='Send Message', command=self.updateChat)
        self.enterbutton.place(x=250, y=40)
        self.buttonClicked = True
        

        self.chatbox.place(x=50, y=60, anchor='nw')
        self.input.place(x=50, y=40)

    def status(self):
        self.status = random.choice(["faulty", "good to go", "in need of repair","ready for firing"])
        concat = "" + self.chat.get() + "\n" + "Systems are " + self.status
        self.chat.set(concat)
        self.chatbox.place(x=50, y=60, anchor='nw')

    def launch(self):
        concat = "" + self.chat.get() + "\n" + "***LAUNCHING WEAPON, BEGIN COUNTDOWN***\nNOTIFYING OTHER DEPARTMENTS"
        self.chat.set(concat)
        self.chatbox.place(x=50, y=60, anchor='nw')
        
    def updateChat(self):
        self.buttonClicked = not self.buttonClicked 
        self.chatdata = self.chat.get()
        if (len(self.chatdata) == 0):
            return
        #stdout_data = self.p.communicate(input='data_to_write')[0]
        concat = "" + self.chat.get() + "\n" + self.input.get()
        self.chat.set(concat)
        self.chatbox.place(x=50, y=60, anchor='nw')

    def receiveMessage(self, data):
        self.chatdata = self.chat.get()
        #stdout_data = self.p.communicate(input='data_to_write')[0]
        concat = "" + self.chat.get() + "\n" + data
        self.chat.set(concat)
        self.chatbox.place(x=50, y=60, anchor='nw')
'''   
def monitorChat(num):
    window=Tk()
    mywin=MyWindow(window)
    username = input("Username: ")
    #user = user.User(username)
    window.title('Hello Python')
    window.geometry("400x300+10+10")
    mywin.chat.set("hello")
    window.mainloop()

    prev = ""
    
    while(True):
        if (len(window.p.stdout) > 0 ):
            print(window.p.stdout)
        if (window.chatdata != prev):
            concat = "" + window.chat.get() + "\n" + window.chatdata
            window.chat.set(concat)
            prev = window.chatdata
'''

'''window=Tk()
mywin=MyWindow(window)


window.title('WEAPON LAUNCH')
window.geometry("400x300+10+10")
#mywin.chat.set("hello")
window.mainloop()'''

#t = Thread(target=updateChat, args = (100,da))
#t.start()

