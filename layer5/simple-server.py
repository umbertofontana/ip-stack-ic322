# This is a simple server that prints messages it receives.

import stub_layer_5 as Layer5
import logging

class SimpleServer:
    def __init__(self):
        """Create a server "process".
        """

        # Connect to our Layer 5 implementation
        self.layer5 = Layer5.StubLayer5(self.receive)

    def receive(self, data):
        """Receive and handle a message.
        """
        print(f"Server received message: {data}")

    def send(self, receiver_addr, data):
        """Sends a message to a receiver.
        """

        # Send the message to our layer 5 implementation
        self.layer5.from_application(data)


if __name__=="__main__":

    # Start server and wait.
    server = SimpleServer()
    print("Server online.")
    while True:
        pass

