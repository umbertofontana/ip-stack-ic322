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

        self.portnum = port

        if sender:
            self.chat = StringVar()
            self.chat.set("LOGIN with STDIN")

            self.username = input("Username: ")
            self.user = user.User(username)
            
            self.ownlabel=Label(win, text=username.capitalize() + " Panel")
            self.ownlabel.place(x=380,y=42)
            if (username == 'ops'):
                self.fire = Button(win, text='FIRE',command=self.launch)
                self.fire.place(x=380, y=60)

            self.status = Button(win, text='Update status',command=self.status)
            self.status.place(x=380, y=80)
            self.status.config(bg='green')


            self.chat.set("Welcome, " + username.upper() + "\n---------------------")
            self.chatbox=Label(win, textvariable=self.chat, justify=LEFT)
            self.chatdata = ""
            
            self.input=Entry(width=30)
            self.enterbutton=Button(win, text='Send Message', command=self.updateChat)
            self.enterbutton.place(x=250, y=40)
            self.buttonClicked = True
            

            self.chatbox.place(x=50, y=60, anchor='nw')
            self.input.place(x=50, y=40)
            self.launchstatus = False

    def receive(self, data, msgformat): # msgformat is just a variable that I pass to make the output nicer while keeping the raw data unchanged
        print(f"{msgformat}{data}")
        self.receiveMessage(data)

    def send(self, message, destport, srcport, destaddress):
        # Send a message to a receiver, passing the right port
        self.layer4.from_layer_5(message + self.username[0], destport, srcport, destaddress) # dest_address

    def status(self):
        if self.launchstatus == False:
            concat = "" + self.chat.get() + "\n" + "Weapon is ready for launch. Ops needs to send the command"
        else:
            concat = "" + self.chat.get() + "\n" + "Weapon has been launched. Enemy = Destroyed"
        self.chat.set(concat)
        self.chatbox.place(x=50, y=60, anchor='nw')

    def launch(self):
        concat = "" + self.chat.get() + "\n" + "***LAUNCHING WEAPON***"
        self.chat.set(concat)
        self.chatbox.place(x=50, y=60, anchor='nw')
        self.send("F", 1, self.user.port, 2) # do we need to send self?
        
    def updateChat(self):
        self.buttonClicked = not self.buttonClicked 
        self.chatdata = self.chat.get()

        lookup = {0:"PRESIDENT",1:"OPS",2:"WEAPON"}

        if (len(self.chatdata) == 0):
            return
        words = self.input.get().split('~')
        if (len(words) < 3):
            concat = "" + self.chat.get() + "\n" + "Enter text in the format [MSG]~[dest addr]~[dest port]"
        else:
            concat = "" + self.chat.get() + "\n(ME) " + words[0] + "\t" + "Sent to " + lookup[self.portnum]
            self.send(words[0] + self.username[0],int(words[2]),self.portnum,int(words[1]))
        self.chat.set(concat)
        self.chatbox.place(x=50, y=60, anchor='nw')

    def receiveMessage(self, data):
        names = {'p':'(PRESIDENT) ','w':'(WEAPON) ', "o":'(OPS) '}

        if data == 'F':
            data = "Weapon Successfully Launched. LETS GOOOOOOOOOOOOOw"
            self.status.config(bg='red')

        self.chatdata = self.chat.get()
        concat = "" + self.chat.get() + "\n" + names[data[len(data) - 1]] + data[:-1]
        self.chat.set(concat)
        self.chatbox.place(x=50, y=60, anchor='nw')

