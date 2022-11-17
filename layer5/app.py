# This program runs all the applications that will
# be running on our network stack.

from guiouioui import MyWindow
from tkinter import *
from threading import Thread

import sys
sys.path.append('../')
import layer4.l4_layer_4 as Layer4
import simple_app as SimpleApp
import logging

# This line sets the logging level to "DEBUG".
# Here's more information about logging in Python:
# https://docs.python.org/3/howto/logging.html
logging.basicConfig(level=logging.DEBUG)

layer4 = Layer4.StubLayer4()

def start_server():
    server = SimpleApp.SimpleApp(layer4)
    data = server.message
    print("Server online.")
    while True:
        if (server.message != ""):
            print(server.message)
            mywin.receiveMessage(server.message)

def start_client():
    # Start client message loop.
    client = SimpleApp.SimpleApp(layer4)
    prev = True
    while True:
        if prev != mywin.buttonClicked:
            msg = mywin.input.get()
            # We haven't implemented an address scheme, so we will just
            # pass the receiver_addr = None.
            client.send(None, msg)
            prev = mywin.buttonClicked

#def runGUI():
    

window=Tk()
mywin=MyWindow(window)
window.title('WEAPON LAUNCH')
window.geometry("400x300+10+10")


t = Thread(target=start_server, args = ())
t.start()
t = Thread(target=start_client, args = ())
t.start()
#t = Thread(target=runGUI, args=())
#t.start()
window.mainloop()