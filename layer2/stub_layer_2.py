# This is a stub for Layer 2.

# Import Layers
import sys
sys.path.append('../')
import layer1.mocklayer1 as Layer1
import logging

class StubLayer2:
    def __init__(self, layer_3_cb):
        """Create a Layer 2 Object.

        `layer_3_cb` - Function. This layer will use `layer_3_cb` to pass data to Layer 3. `layer_3_cb`
                       must accept a single parameter `data`.
        """
        # Save parameter inputs as instance attributes so they can be referred to later
        self.layer_3_cb = layer_3_cb

        # Connect to Layer 1
        input_pin = int(sys.argv[1])
        output_pin = int(sys.argv[2])
        self.layer1 = Layer1.MockLayer1(input_pin, output_pin, self.from_layer_1)

    def from_layer_3(self, data):
        """Call this function to send data to this layer from layer 3"""
        logging.debug(f"Layer 2 received msg from Layer 3: {data}")

        # Pass the message down to Layer 1
        self.layer1.from_layer_2(data) 

    def from_layer_1(self, data):
        """Call this function to send data to this layer from layer 1"""
        logging.debug(f"Layer 2 received msg from Layer 1: {data}")

        # Let's just forward this up to layer 3.
        self.layer_3_cb(data)
