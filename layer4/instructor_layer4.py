# This is a stub for Layer 4. This is a change.

# Import Layers
import sys
sys.path.append('../')
import layer3.instructor_layer3 as Layer3
import logging


#
# Layer 4 Helpers
#
def add_header(msg, port_number):
    """Adds header to string. Returns string."""
    port_field = str(port_number).zfill(5)
    return port_field + msg

def parse_header(msg):
    """Reads header and returns values (including message without
    header)"""
    header = msg[0:5]
    port_number = int(header)
    message= msg[5:]
    return {
        "message": message,
        "port_number": port_number
            }

class StubLayer4:
    def __init__(self):
        """Create a Layer 4 Object.

            This initializer doesn't ask for a callback since there
            will likely be multiple callbacks connected to sockets.
            Use the `connect_to_socket` method to register a
            layer_5_cb.

        """
        # Create a port-callback lookup
        self.port_to_cb = {}

        # Connect to Layer 3
        self.layer3 = Layer3.StubLayer3(self.from_layer_3)

    def connect_to_socket(self, port_number, layer_5_cb):
        """Connect an application to a socket.

        `port_number` - Integer.

        `layer_5_cb` - Function. This function will be called when data comes in on the specified port.
        """

        # Record which port number goes to which cb function
        self.port_to_cb[port_number] = layer_5_cb
        logging.debug(f"Connected to port {port_number}")


    def from_layer_5(self, data, src_port, dest_port, dest_addr):
        """Call this function to send data to this layer from layer 5

        `src_port` - Integer. This is the port number on this machine
        `dest_port` - Integer. This is the port number on the
                      receiver's machine.
        """
        logging.debug(f"Layer 4 received msg from Layer 5: {data}")

        # Add header
        message_with_header = add_header(data, dest_port)
        # send message with headers
        self.layer3.from_layer_4(message_with_header, dest_addr=dest_addr) 

        # add message to sent message list

    def from_layer_3(self, data):
        """Call this function to send data to this layer from layer
        3
        """
        logging.debug(f"Layer 4 received msg from Layer 3: {data}")

        # parse header
        parsed_message = parse_header(data)

        # figure out which port number this goes to
        port = parsed_message["port_number"]
        logging.debug(f"Layer 4 determines port {port}")

        # look up the correct callback function
        cb = self.port_to_cb[port]

        # send the message to the correct application
        msg = parsed_message["message"]
        cb(msg)
