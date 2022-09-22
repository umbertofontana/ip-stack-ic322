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

        # Connect to Layer 1 on interface 1. Your actual implementation will
        # have multiple interfaces.
        self.layer1_interface_1 = Layer1.MockLayer1(interface_number=1, layer_2_cb=self.from_layer_1)

    def from_layer_3(self, data, interface):
        """Call this function to send data to this layer from layer 3"""
        logging.debug(f"Layer 2 received msg from Layer 3: {data}")

        # Layer 2 takes messages from Layer 3, converts the message to bits, and sends that
        # message down to Layer 1. Layer 1 will transmit the exact bitstream that it is sent.
        # So if your Layer 2 implementation will rely on any kind of "start pattern", length
        # field, or "end pattern", you'll need to add it here.

        # Layer 3 is making the decision about which interface to send the data. Layer 2
        # simply follows Layer 3's directions (and receives the interface number as an
        # argument.

        # Pass the message down to Layer 1. This 
        self.layer1_interface_1.from_layer_2(data) 

    def from_layer_1(self, data):
        """Call this function to send data to this layer from layer 1"""
        logging.debug(f"Layer 2 received msg from Layer 1: {data}")

        # The big goal of Layer 2 is to take incoming bits from Layer 1 and convert them into
        # Layer 3 messages. This is where you will put the logic for that. Think about:
        # 1. How will you know if the bits are actually part of a message, or just noise?
        # 2. How will you know when a message (a Layer 2 frame) begins?
        # 3. How will you know when a message ends?
        # 4. You will almost certainly *not* receive an entire frame at once. You will
        #    need to save incoming data in some kind of buffer (variable).
        # 5. How will you detect errors? What will you do if you detect an error?

        # Let's just forward this up to layer 3.
        self.layer_3_cb(data)


