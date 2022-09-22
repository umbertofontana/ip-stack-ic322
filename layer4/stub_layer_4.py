# This is a stub for Layer 4.

# Import Layers
import sys
sys.path.append('../')
import layer3.stub_layer_3 as Layer3
import logging

class StubLayer4:
    def __init__(self):
        """Create a Layer 4 Object.

            This initializer doesn't ask for a callback since there
            will likely be multiple callbacks connected to sockets.
            Use the `connect_to_socket` method to register a
            layer_5_cb.

        """

        # Connect to Layer 3
        self.layer3 = Layer3.StubLayer3(self.from_layer_3)

    def connect_to_socket(self, port_number, layer_5_cb):
        """Connect an application to a socket.

        `port_number` - Integer.

        `layer_5_cb` - Function. This function will be called when data comes in on the specified port.
        """

        # You should keep track of which callback should be called
        # for each socket. That is something you'll need
        # to implement.

        # For now, just send all messages to the latest open socket.
        self.layer_5_cb = layer_5_cb


    def from_layer_5(self, data, src_port, dest_port, dest_addr):
        """Call this function to send data to this layer from layer 5

        `src_port` - Integer. This is the port number on this machine
        `dest_port` - Integer. This is the port number on the
                      receiver's machine.
        """
        logging.debug(f"Layer 4 received msg from Layer 5: {data}")

        # Right now I'm not doing anything with the port numbers.
        # You should use them to multiplex between applications.

        # Pass the message down to Layer 3
        self.layer3.from_layer_4(data) 

    def from_layer_3(self, data):
        """Call this function to send data to this layer from layer
        3
        """
        logging.debug(f"Layer 4 received msg from Layer 3: {data}")

        # You need to take Layer 3 data and forward it to Layer 5.
        # However, there might be multiple Layer 5 applications you could
        # send the data to. How are you going to multiplex these?

        # Let's just forward this up to layer 5.
        self.layer_5_cb(data)
