# This is a stub for Layer 3.

# Import Layers
import sys
sys.path.append('../')
import layer2.instructor_link as Layer2
import logging
from threading import Timer # Timer used for discovery messages



###############
# Helpers
###############

def interfaces():
    """Returns a list with all the interfaces"""
    return [1]

def cmd_line_args():
    """Returns a hash, with arg:value of every command line argument."""

    cmd_line_key_values = {}
    for full_arg in sys.argv[1:]: # the first argv value is the process name.
        # strip leading hyphens and split on equal signs
        try:
            k, v = full_arg.strip("-").split("=")
        except ValueError as e:
            raise("Your command line argument {full_arg} is wrong. Make sure you follow the format --key=value and you don't use spaces.")
        cmd_line_key_values[k] = v
    return cmd_line_key_values

def parse_header(msg_with_header):
    """ Header format:
    Bits 0-1: Message Type (int, zero-padded)
                01 - Application Message
                02 - Discovery Message
         2-3: Source address (int, zero-padded)
         4-5: Destination address (int, zero-padded)
         6-till: message
    """

    return {
        "message": msg_with_header[6:],
        "message_type": msg_with_header[:2],
        "source_address": msg_with_header[2:4],
        "destination_address": msg_with_header[4:6],
            }

def add_header(message, message_type, source_address, destination_address):
    return f"{message_type.zfill(2)}{source_address.zfill(2)}{destination_address.zfill(2)}{message}"

###############
# Main Class
###############

class StubLayer3:
    def __init__(self, layer_4_cb):
        """Create a Layer 3 Object.

        `layer_4_cb` - Function. This layer will use `layer_4_cb` to pass data to Layer 4. `layer_4_cb`
                       must accept a single parameter `data`.
        """
        # Save parameter inputs as instance attributes so they can be referred to later
        self.layer_4_cb = layer_4_cb

        # Connect to Layer 2
        self.layer2 = Layer2.StubLayer2(self.from_layer_2)

        # Get my address
        self.address = cmd_line_args()["address"].zfill(2)
        logging.debug(f"Layer 3 Address: {self.address}")

        # Send discovery messages every once in a while
        # t = Timer(3.0, self.send_discovery_message)
        # t.start()


    def from_layer_4(self, data, dest_addr):
        """Call this function to send data to this layer from layer 4"""
        logging.debug(f"Layer 3 received msg from Layer 4: {data}")

        # Add header
        msg = add_header(message_type="01", source_address=self.address, destination_address = dest_addr, message=data)
        logging.debug(f"Address {self.address} sending {msg}")
        self.layer2.from_layer_3(msg, interface=1) 

    def from_layer_2(self, data):
        """Call this function to send data to this layer from layer 2"""
        logging.debug(f"Layer 3 received msg from Layer 2: {data}")

        # parse headers
        parsed_message = parse_header(data)
        logging.debug(f"Address {self.address} received {parsed_message}.")

        # not for me... forward on
        if parsed_message["destination_address"] != self.address and parsed_message["destination_address"] != "99":
            logging.debug(f"Dest:{parsed_message['destination_address']}, data:{data}")
            for i in interfaces():
                self.layer2.from_layer_3(data, interface = i)

        # for one of my applications
        elif parsed_message["message_type"] == "01":
            self.layer_4_cb(parsed_message["message"])
        
        # a discover message
        elif parsed_message["message_type"] == "02":
            logging.info(f"Address {self.address} received Discover message from {parsed_message['source_address']}")

    def send_discovery_message(self):
        data = "Hello!"
        msg = add_header(message_type="02", source_address=self.address, destination_address = "99", message=data)

        for i in interfaces():
            self.layer2.from_layer_3(msg, interface = i)
