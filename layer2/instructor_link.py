# This is a stub for Layer 2.

# Import Layers
import sys
sys.path.append('../')
import layer1.EdgeCodesLayer1 as Layer1
import logging

#
# General Helpers
#
def flatten(l):
    """Flattens a list of lists."""
    return [item for sublist in l for item in sublist]

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

#
# Layer 2 Helpers
#
def bin_list_from_string(s):
    """Converts a string to a list of 1's and 0's."""
    # Convert string to a list of bytes
    bs = bytearray(s.encode()) # bytes
    # Convert to a list of binary strings ["010001","0010101"...]
    binary_strings = [format(x, '08b') for x  in bs]
    # Convert to a list of 1,0 ints [0,1,1,1,0...]
    binary_list = [int(x) for x in flatten(binary_strings)]
    logging.debug(f"{s} converted to {binary_list}, with {len(binary_list)} values in it.")
    return binary_list

def string_from_bin_list(bl):
    """Converts a list of 1s and 0s to a string!"""
    # convert the ints to strings
    binary_string_list = [str(x) for x in bl]
    # chunk into bytes
    binary_string_chunks = ["".join(x) for x in chunks(binary_string_list, 8)]
    # convert binary chunks into ints
    byte_list = [int(x,2) for x in binary_string_chunks]
    msg = bytes(byte_list).decode("utf-8")
    logging.debug(f"Converted back to {msg}")
    return msg



class StubLayer2:
    def __init__(self, layer_3_cb):
        """Create a Layer 2 Object.

        `layer_3_cb` - Function. This layer will use `layer_3_cb` to pass data to Layer 3. `layer_3_cb`
                       must accept a single parameter `data`.
        """
        # Save parameter inputs as instance attributes so they can be referred to later
        self.layer_3_cb = layer_3_cb

        # Connect to Layer 1 on interface 1. Your actual implementation will
        # have multiple interfaces.
        self.interfaces= [
            Layer1.EdgeCodesLayer1(interface_number=1, layer_2_cb=self.from_layer_1, enforce_binary=True),
                ]

    def from_layer_3(self, data, interface):
        """Call this function to send data to this layer from layer 3"""
        logging.debug(f"Layer 2 received msg from Layer 3: {data}")

        # Convert layer 3 message to binary
        binary_message = bin_list_from_string(data)

        # self.layer1_interface_1.from_layer_2(binary_message) 
        self.interfaces[interface-1].from_layer_2(binary_message) 


    def from_layer_1(self, data):
        """Call this function to send data to this layer from layer 1"""
        logging.debug(f"Layer 2 received msg from Layer 1: {data}")

        # Convert binary list back to string


        try:
            msg = string_from_bin_list(data)
            self.layer_3_cb(msg)
        except UnicodeDecodeError as e:
            logging.error("Layer 2 error understanding message from layer 1. Probably a corrupted message. Tossing out.")


