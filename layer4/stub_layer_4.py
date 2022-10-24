# Layer 4 Protocol

# Import Layers 
import sys
sys.path.append('../')
import layer3.stub_layer_3 as Layer3
import logging
import base64

# Dictionary that correlates a port number to the object layer_5_cb
connections = {}

# Dictionary that increments the port number for each connection
portincrement = {"p":15000}

class StubLayer4:


    # Create a Layer 4 object and initialize the attributes of the class
    def __init__(self):
        # Connect to Layer 3
        self.layer3 = Layer3.StubLayer3(self.from_layer_3)


    # Connect an application to a socket.
    def connect_to_socket(self, port_number, layer_5_cb, portassigner):

        # First connection is the server. All subsequent connections are clients.
        # This function always gets called with port number 80. We need to assign it a new port number..
        self.layer_5_cb = layer_5_cb
        self.portassigner = portassigner
        
        logging.debug(f"Socket connected")

        # Server is assigned port 15000. All other clients will have an incremental port starting at 15001
        socketport = portincrement["p"]
        connections[socketport] = self.layer_5_cb

        # Send back the port number to the process in order for him to know his own port number
        self.portassigner(socketport)

        # Increment the port number for future connections
        socketport = socketport + 1
        portincrement["p"] = socketport

        logging.debug(f"{connections}")


    # Call this function to send data to this Layer from Layer 5.
    def from_layer_5(self, data, src_port, dest_port, dest_addr):
       
        logging.debug(f"Layer 4 received msg from Layer 5: {data}")

        # Header implementation
        # For now, the destination address is not included. I first need to see how Layer 3 will implement addresses
        data = base64.b64encode(data.encode("utf-8"))
        data = str(data, "utf-8")

        header = f"{dest_port}.{src_port}"
        segment = f"{header}.{data}"

        # Pass the message down to Layer 3
        self.layer3.from_layer_4(segment) 

        # Here is where a timeout system will be implemented
    

    # Call this function to send data to this Layer from Layer 3
    def from_layer_3(self, segment):

        # Server port is 15000
        # Clients are currently on the range 15001-15003

        # Decode the header information and the data
        dest_port, src_port, data = segment.split(".")
        dest_port = int(dest_port)
        data = base64.b64decode(data)
        data = str(data, "utf-8")

        logging.debug(f"Layer 4 received msg from Layer 3: {segment} -> {data} to port {dest_port} from port {src_port}")

        # Here is where ACKs will be implemented

        # Implement multiplexing based on the destination port in the header and send the data to Layer 5
        connections[dest_port](data)
        
