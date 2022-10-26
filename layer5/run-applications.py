# This program runs all the applications that will
# be running on our network stack.


from threading import Thread

import sys
sys.path.append('../')
import layer4.stub_layer_4 as Layer4
import my_simple_app as SimpleApp # Remember to change this when we merge
import logging

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
    client = SimpleApp.SimpleApp(layer4)
    while True:
        msg = input("Msg: ")
        # We haven't implemented an address scheme, so we will just
        # pass the receiver_addr = None.
        client.send(None, msg)

# Create a Server
t = Thread(target=start_server, args = ())
t.start()
# Create Client 1
t = Thread(target=start_client, args = ())
t.start()
# Create Client 2
t = Thread(target=start_client, args = ())
t.start()
# Create Client 3
t = Thread(target=start_client, args = ())
t.start()
