# This program runs all the applications that will
# be running on our network stack.


from threading import Thread

import sys
sys.path.append('../')
import layer4.layer4 as Layer4
import simple_app as SimpleApp
import logging
import simple_app1 as SimpleSys


# This line sets the logging level to "DEBUG".
# Here's more information about logging in Python:
# https://docs.python.org/3/howto/logging.html
logging.basicConfig(level=logging.DEBUG)

layer4 = Layer4.StubLayer4()

def start_server():
    server = SimpleApp.SimpleApp(layer4)
    print("Server online.")
    while True:
        pass

def start_client():
    # Start client message loop.
    client = SimpleSys.SimpleSys(layer4)
    while True:
        msg = input("Msg: ")
        # We haven't implemented an address scheme, so we will just
        # pass the receiver_addr = None.
        client.send(None, msg)

def start_GUI():
    #make the GUI
    GUI = SimpleSys.SimpleSys(layer4)
    GUI.runGUI()
    while True:
        pass 
        
t = Thread(target=start_server, args = ())
t.start()
t = Thread(target=start_client, args = ())
t.start()
t = Thread(target=start_GUI, args = ())
t.start()
