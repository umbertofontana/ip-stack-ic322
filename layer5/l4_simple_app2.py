# This is a simple networked application that can both send and
# receive data. Think of it as "telnet".

import logging
from tkinter import *
import user
import random
import led as led
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

            self.user = user.User("weapons")
            
            self.status = Label(win, text='Status')
            self.status.config(bg="green") 
            self.status.place(x=200, y=150)


    def receive(self, data, msgformat): # msgformat is just a variable that I pass to make the output nicer while keeping the raw data unchanged
        print(f"{msgformat}{data}")
        self.receiveMessage(data)

    def send(self, message, destport, srcport, destaddress):
        # Send a message to a receiver, passing the right port
        self.layer4.from_layer_5(message, destport, srcport, destaddress) # dest_address

    def launch(self):
        concat = "" + self.chat.get() + "\n" + "***LAUNCHING WEAPON, BEGIN COUNTDOWN***\nNOTIFYING OTHER DEPARTMENTS"
        self.chat.set(concat)
        self.chatbox.place(x=50, y=60, anchor='nw')
        self.send(self, "F", 1, self.user.port, 2)
        
    def receiveMessage(self, data):
        if data == "F":
            led.fire()
            self.status.config(bg="red") 
            #change status button to red
            #send back Fired ack
            self.send("F",0,1,1)
            
