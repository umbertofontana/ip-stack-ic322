# Layer 4 Protocol

# Import Layers
# Why are we not importing Layer 5? 
import sys
sys.path.append('../')
import layer3.stub_layer_3 as Layer3
import logging

class StubLayer4:
    # Create a Layer 4 Object. The __init__ function is called automatically whenever a new object of a class is created. 
    # It's used to initialize the attributes of the class.
    def __init__(self):
        # Connect to Layer 3
        self.layer3 = Layer3.StubLayer3(self.from_layer_3)
    
    # -------------------------------------------------------------------------------------------------------------------------------------

    # Connect an application to a socket.
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
        logging.debug(f"{self.layer_5_cb}")

    # -------------------------------------------------------------------------------------------------------------------------------------

    # Call this function to send data to this Layer from Layer 5.
    # This is the function called from Layer 5 when it wants to send us data. It's basically the function that sends a message.
    def from_layer_5(self, data, src_port, dest_port, dest_addr):
      
        logging.debug(f"Layer 4 received msg from Layer 5: {data}")

        # This is the place to implement an header to attach to the data: it must contain the destination address, destination port 
        # and the source port. Port numbers are necessary to multiplex between applications.
        # This is also the place to implement a timer.

        # Pass the message down to Layer 3
        self.layer3.from_layer_4(data) 
    
    # -------------------------------------------------------------------------------------------------------------------------------------

    # Call this function to send data to this Layer from Layer 3
    # This is the function called from Layer 3 when it wants to send us data. It's the function that receives a message.
    def from_layer_3(self, data):
       
        logging.debug(f"Layer 4 received msg from Layer 3: {data}")

        # This is where I need to understand the header, remove it and implement multiplexing using the port numbers.
        # Here is also where I need to send an ACK back.

        # Pass the message up to Layer 5
        self.layer_5_cb(data)
