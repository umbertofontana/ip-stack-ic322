# This program runs all the applications that will
# be running on our network stack.


from threading import Thread

import sys
sys.path.append('../')
import layer4.l4_layer_4 as Layer4
import l4_simple_app as SimpleApp # Remember to change this when we merge
import logging

# Chat: port 0
# Weapon: port 1

# This line sets the logging level to "DEBUG".
# Here's more information about logging in Python:
# https://docs.python.org/3/howto/logging.html
logging.basicConfig(level=logging.DEBUG)

layer4 = Layer4.StubLayer4()

def start_chat():
    chatport = 0 # The port where the chat client communicates is hardcoded as 0
    chat = SimpleApp.SimpleApp(chatport, layer4)
    print("Server online.")
    while True:
        msg = input("Msg: ")
        recv_port = int(input("Destination? <0: chat, 1: weapon control>"))
        # We haven't implemented an address scheme, so we will just pass the receiver_addr = None.
        chat.send(None, chatport, recv_port, msg)
        
def start_weapon():
    # The weapon only listens to feedback at the moment
    weaponport = 1 # The port where the weapon control communicates is hardcoded as 1
    weapon = SimpleApp.SimpleApp(weaponport, layer4)
    while True:
        pass

# Start the chat thread
t = Thread(target=start_chat, args = ())
t.start()
# Start the weapon thread
t = Thread(target=start_weapon, args = ())
t.start()