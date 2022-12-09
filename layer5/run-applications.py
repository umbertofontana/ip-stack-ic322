# This program runs all the applications that will
# be running on our network stack.

from threading import Thread

import sys
sys.path.append('../')
import layer4.layer4 as Layer4
import l4_simple_app as SimpleApp # Remember to change this when we merge
import logging
from tkinter import *

# Chat: port 0
# Weapon: port 1

# This line sets the logging level to "DEBUG".
# Here's more information about logging in Python:
# https://docs.python.org/3/howto/logging.html
logging.basicConfig(level=logging.DEBUG)

layer4 = Layer4.StubLayer4()

def start_chat(mywin, sender):
    chatport = 0 # The port where the chat client communicates is hardcoded as 0
    chat = SimpleApp.SimpleApp(chatport, layer4, mywin, sender)
    print("Server online.")
    while True:
        pass
        '''
        message = input("Msg: ")
        destport = int(input("Chat or weapon? <0: chat, 1: weapon control>"))
        destaddress = int(input("To which address? <0 through 4>"))
        # We haven't implemented an address scheme, so we will just pass the receiver_addr = None.
        chat.send(message, destport, chatport, destaddress)
        '''
        
def start_weapon(mywin, sender):
    # The weapon only listens to feedback at the moment
    weaponport = 1 # The port where the weapon control communicates is hardcoded as 1
    weapon = SimpleApp.SimpleApp(weaponport, layer4, mywin, sender)
    while True:
        pass

window=Tk()
window.title('WEAPON LAUNCH')
window.geometry("400x300+10+10")

t = Thread(target=start_chat, args = (window,True))
t.start()
t = Thread(target=start_weapon, args = (window,False))
t.start()

window.mainloop()

