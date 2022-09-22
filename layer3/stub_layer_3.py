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

        # Do you want to send a message without waiting for Layer 4 to call? You
        # can do that any time by calling:
        #   self.layer2.from_layer_3(data, interface=1) 

    def from_layer_4(self, data):
        """Call this function to send data to this layer from layer 4"""
        logging.debug(f"Layer 3 received msg from Layer 4: {data}")

        # The major job of Layer 3 is to decide which interface to send messages on.
        # You want to "map out" the network (probably using your own Layer 3 messages)
        # and then use some kind of routing algorithm to decide which interface to use.

        # Pass the message down to Layer 2; use interface 1.
        self.layer2.from_layer_3(data, interface=1) 

    def from_layer_2(self, data):
        """Call this function to send data to this layer from layer 2"""
        logging.debug(f"Layer 3 received msg from Layer 2: {data}")

        # Is this data addressed to this host? If so, pass it up to the next layer.
        # If not, pass it back down to the correct interface on Layer 2.

        # If you're using some kind of "Layer 3 message" to communicate between different
        # hosts' layer 3's (perhaps to do some kind or routing or discoverability), you'll also
        # need to decide whether this data is destined to go to an application (in
        # which case you pass it up to Layer 4) or if it's supposed to be used here in Layer 3.
        # Hopefully you added your own header to it!

        # For now let's just forward this up to layer 4.
        self.layer_4_cb(data)
