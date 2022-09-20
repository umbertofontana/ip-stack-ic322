# This is a simple client that recieves user input and sends it to...?

import stub_layer_5 as Layer5
import logging

class SimpleClient:
    def __init__(self):
        """Create a client "process".
        """

        # Connect to our Layer 5 implementation
        self.layer5 = Layer5.StubLayer5(self.receive)

    def receive(self, data):
        """Receive and handle a message.
        """
        print(f"Client received message: {data}")

    def send(self, receiver_addr, data):
        """Sends a message to a receiver.
        """

        # Send the message to our layer 5 implementation
        self.layer5.from_application(data)


if __name__=="__main__":

    # Start client message loop.
    client = SimpleClient()
    while True:
        msg = input("Msg: ")
        # We haven't implemented an address scheme, so we will just pass
        # the receiver_addr = None.
        client.send(None, msg)

