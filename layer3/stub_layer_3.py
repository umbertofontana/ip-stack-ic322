# This is a stub for Layer 3.

# Import Layers
import sys
sys.path.append('../')
import layer2.stub_layer_2 as Layer2
import logging

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

    def from_layer_4(self, data):
        """Call this function to send data to this layer from layer 4"""
        logging.debug(f"Layer 3 received msg from Layer 4: {data}")

        # Pass the message down to Layer 2
        self.layer2.from_layer_3(data) 

    def from_layer_2(self, data):
        """Call this function to send data to this layer from layer 2"""
        logging.debug(f"Layer 3 received msg from Layer 2: {data}")

        # Let's just forward this up to layer 4.
        self.layer_4_cb(data)
