# This is a simple networked application that can both send and
# receive data. Think of it as "telnet".

import logging
from tkinter import *
import user
import random

class SimpleApp:
    def __init__(self, port, layer4, win, sender):
        # Save the layer 4 object as a instance variable so we can reference it later
        self.layer4 = layer4
        # Open a new socket to listen on, passing the callback functions for receiving a message and the port
        self.layer4.connect_to_socket(self.receive, port)

        #######################################
        # GUI #
        if not sender:
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
            self.chatbox=Label(win, textvariable=self.chat, justify=LEFT)
            self.chatdata = ""
            
            self.input=Entry(width=30)
            self.enterbutton=Button(win, text='Send Message', command=self.updateChat)
            self.enterbutton.place(x=250, y=40)
            self.buttonClicked = True
            

            self.chatbox.place(x=50, y=60, anchor='nw')
            self.input.place(x=50, y=40)

    def receive(self, data, msgformat): # msgformat is just a variable that I pass to make the output nicer while keeping the raw data unchanged
        print(f"{msgformat}{data}")
        self.receiveMessage(data)

    def send(self, message, destport, srcport, destaddress):
        # Send a message to a receiver, passing the right port
        self.layer4.from_layer_5(message, destport, srcport, destaddress) # dest_address








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
        words = self.input.get().split('~')
        if (len(words) < 3):
            concat = "" + self.chat.get() + "\n" + "Enter text in the format [MSG]~[dest port]~[dest addr]"
        else:
            concat = "" + self.chat.get() + "\n" + words[0] + "\n\t" + "Sent to address " + words[1] + ", port " + words[2]
            self.send(words[0],int(words[2]),self.user.port,int(words[2]))
        self.chat.set(concat)
        self.chatbox.place(x=50, y=60, anchor='nw')

    def receiveMessage(self, data):
        self.chatdata = self.chat.get()
        concat = "" + self.chat.get() + "\n" + data
        self.chat.set(concat)
        self.chatbox.place(x=50, y=60, anchor='nw')

