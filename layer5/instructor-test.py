# This is a simple networked application that can both send and
# receive data. Think of it as "telnet".

from threading import Thread

import sys
sys.path.append('../')
import layer4.instructor_layer4 as Layer4
import logging
logging.basicConfig(level=logging.DEBUG)

class SimpleApp:
    def __init__(self, layer4, port, name="Unnamed"):
        """Create a client "process".

        We pass a layer 5 object so that we don't instantiate
        more than one "network stack."
        """

        # Save the layer 4 object as a instance variable
        # so we can reference it later
        self.layer4 = layer4

        # more instance variables
        self.name = name

        # Open a new socket to listen on. Here we're choosing
        # port 80 (just as an example.)
        logging.debug(f"{name} connecting on port {port}")
        self.layer4.connect_to_socket(port, self.receive)

    def receive(self, data):
        """Receive and handle a message.
        """
        print(f"{self.name} received message: {data}")

    def send(self, dest_addr, data):
        """Sends a message to a receiver.
        """

        # Send the message to layer 4. We haven't implemented
        # proper addresses yet so we're setting the port numbers
        # and addr to None.
        self.layer4.from_layer_5(data=data, src_port=None,
                dest_port=90, dest_addr=dest_addr)


############
#   Main   #
############

layer4 = Layer4.StubLayer4()

def start_server():
    server = SimpleApp(layer4, 90, "Server")
    print("Server online.")
    while True:
        pass

def start_client():
    # Start client message loop.
    client = SimpleApp(layer4, 91, "Client")
    while True:
        address = input("Dest Address: ")
        msg = input("Msg: ")
        # We haven't implemented an address scheme, so we will just
        # pass the receiver_addr = None.
        client.send(address, msg)


t = Thread(target=start_server, args = ())
t.start()
t = Thread(target=start_client, args = ())
t.start()
