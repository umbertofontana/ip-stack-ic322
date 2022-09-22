# This is a simple server that prints messages it receives.

import logging


class SimpleServer:
    def __init__(self, layer4):
        """Create a server "process".
        """

        # Save the layer 4 object as a instance variable
        # so we can reference it later
        self.layer4 = layer4

        # Open a new socket to listen on. Here we're choosing
        # port 80 (just as an example.)
        self.layer4.connect_to_socket(80, self.receive)

    def receive(self, data):
        """Receive and handle a message.
        """
        print(f"Server received message: {data}")

    def send(self, data):
        """Sends a message to a receiver.
        """

        # Send the message to layer 4. We haven't implemented
        # proper addresses yet so we're setting the port numbers
        # and addr to None.
        self.layer4.from_layer_5(data=data, src_port=None,
                dest_port=None, dest_addr=None)



