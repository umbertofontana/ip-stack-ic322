# This is a stub for Layer 5.

# Import Layers
import sys
sys.path.append('../')
import layer4.stub_layer_4 as Layer4
import logging

class StubLayer5:
    def __init__(self, application_cb):
        """Create a Layer 5 Object.

        `application_cb` - Function. This layer will use `application_cb` to pass data to Layer 6. `application_cb`
                       must accept a single parameter `data`.
        """
        # Save parameter inputs as instance attributes so they can be referred to later
        self.application_cb = application_cb

        # Connect to Layer 4
        self.layer4 = Layer4.StubLayer4(self.from_layer_4)

    def from_application(self, data):
        """Call this function to send data to this layer from application"""
        logging.debug(f"Layer 5 received msg from application: {data}")

        # Pass the message down to Layer 4
        self.layer4.from_layer_5(data) 

    def from_layer_4(self, data):
        """Call this function to send data to this layer from layer 4"""
        logging.debug(f"Layer 5 received msg from Layer 4: {data}")

        # Let's just forward this up to the application
        self.application_cb(data)
