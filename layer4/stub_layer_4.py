# Layer 4 Protocol

# Import Layers
# Why are we not importing Layer 5? 
import sys
sys.path.append('../')
import layer3.stub_layer_3 as Layer3
import logging
import base64

# Dictionary that correlates a port number to the object layer_5_cb
port_callback = {}

class StubLayer4:
    # Create a Layer 4 Object. The __init__ function is called automatically whenever a new object of a class is created. 
    # It's used to initialize the attributes of the class.
    def __init__(self):
        # Connect to Layer 3
        self.layer3 = Layer3.StubLayer3(self.from_layer_3)
    
    # -------------------------------------------------------------------------------------------------------------------------------------

    # Connect an application to a socket.
    def connect_to_socket(self, port_number, layer_5_cb):
       
        # For now, just send all messages to the latest open socket.
        # Everytime an application opens a connection, the object layer_5_cb is passed to us. We need to correlate that particular 
        # object to the particular process. I might use a dictionary for that.

        # layer_5_cb: function that is called when data comes in on the specified port.

        # You should keep track of which callback should be called for each socket. That is something you'll need to implement.
        # But how can I identify each callback? I can use the object! So dictionary with port:callback

        # For now, just send all messages to the latest open socket.
        self.layer_5_cb = layer_5_cb
        # New {port number:callback} entry for the dictionary. Is this the right way to keep track of the callbacks?
        port_callback[port_number] = self.layer_5_cb

    # -------------------------------------------------------------------------------------------------------------------------------------

    # Call this function to send data to this Layer from Layer 5.
    # This is the function called from Layer 5 when it wants to send us data. It's basically the function that sends a message.
    def from_layer_5(self, data, src_port, dest_port, dest_addr):
      
        logging.debug(f"Layer 4 received msg from Layer 5: {data}")
        logging.debug(f"{port_callback}")

        # This is the place to implement an header to attach to the data: it must contain the destination address, destination port 
        # and the source port. Port numbers are necessary to multiplex between applications.
        # This is also the place to implement a timer.  

        # - Header implementation -
        # Header = dest_addr + dest_port + src_port + data

        header = f"{base64.b64encode(dest_addr)}.{base64.b64encode(dest_port)}.{base64.b64encode(src_port)}"
        segment = f"{header}.{data}"

        # Pass the message down to Layer 3
        self.layer3.from_layer_4(segment) 
    
    # -------------------------------------------------------------------------------------------------------------------------------------

    # Call this function to send data to this Layer from Layer 3
    # This is the function called from Layer 3 when it wants to send us data. It's the function that receives a message.
    def from_layer_3(self, segment):

        dest_addr, dest_port, src_port, data = segment.split(".")
        
        dest_port = base64.b64decode(dest_port)
        data = base64.b64decode(data)

        logging.debug(f"Layer 4 received msg from Layer 3: {segment} -> {data} to port {dest_port}")

        # This is where I need to understand the header, remove it and implement multiplexing using the port numbers.
        # Here is also where I need to send an ACK back.

        # Pass the message up to Layer 5
        self.layer_5_cb(data)

        
