# This is a stub for Layer 4.

# Import Layers
import sys
sys.path.append('../')
import layer3.stub_layer_3 as Layer3
import logging

class StubLayer4:
    def __init__(self, layer_5_cb):
        """Create a Layer 4 Object.

        `layer_5_cb` - Function. This layer will use `layer_5_cb` to pass data to Layer 5. `layer_5_cb`
                       must accept a single parameter `data`.
        """
        # Save parameter inputs as instance attributes so they can be referred to later
        self.layer_5_cb = layer_5_cb

        # Connect to Layer 3
        self.layer3 = Layer3.StubLayer3(self.from_layer_3)

    def from_layer_5(self, data):
        """Call this function to send data to this layer from layer 5"""
        logging.debug(f"Layer 4 received msg from Layer 5: {data}")

        # Pass the message down to Layer 3
        self.layer3.from_layer_4(data) 

    def from_layer_3(self, data):
        """Call this function to send data to this layer from layer 3"""
        logging.debug(f"Layer 4 received msg from Layer 3: {data}")

        # Let's just forward this up to layer 5.
        self.layer_5_cb(data)
