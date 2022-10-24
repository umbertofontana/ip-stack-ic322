# This is a simple networked application that can both send and
# receive data. Think of it as "telnet".

import logging

assignedport = {}

class SimpleApp:
    def __init__(self, layer4):
        # Create a client process

        # Save the layer 4 object as a instance variablevso we can reference it later
        self.layer4 = layer4

        # Open a new socket to listen on (standard port is port 80), passing the callback functions for receiving a message and the port
        self.layer4.connect_to_socket(80, self.receive, self.porthandler)


    def receive(self, data):
        print(f"Client received message: {data}")

    # Receive the port assigned from Layer 4
    def porthandler(self, port):
        # Store the port number into a dictionary
        assignedport["source_port"] = port

    def send(self, receiver_addr, data):
        # Send a message to a receiver

        # I assume for now that all messages need to be directed to the Server, which is on port 15000
        self.layer4.from_layer_5(data=data, src_port=assignedport["source_port"], dest_port=15000, dest_addr=None)
