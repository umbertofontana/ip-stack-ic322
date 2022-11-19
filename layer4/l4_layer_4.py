# Layer 4 Protocol

# Import Layers 
import sys
sys.path.append('../')
import layer3.stub_layer_3 as Layer3
import logging
import base64
import time
import random

# Dictionary that correlates a port number to the object layer_5_cb
connections = {}
# Dictionary used to check if we are waiting for an ACK. If 0 we are not waiting for an ACK, if 1 we are waiting for an ACK
ackcheck = {"ACK":0}
# Dictionary that stores sequence numbers received from a specific socket
sequence = {}
sequencenumber = random.randint(1000,10000)

class StubLayer4:

    # Create a Layer 4 object and initialize the attributes of the class
    def __init__(self):
        # Connect to Layer 3
        self.layer3 = Layer3.StubLayer3(self.from_layer_3)

    # Connect an application to a socket.
    def connect_to_socket(self, layer_5_cb, port):
        self.layer_5_cb = layer_5_cb
        logging.debug(f"Socket connected")
        # Based on the port value (0 for chat client, 1 for weapon control) assign the right socket and save it
        connections[port] = self.layer_5_cb

    # Timeout function
    def timeout(self):
        start = time.time()
        while ackcheck["ACK"] == 1:
            if time.time() - start < 3:
                continue
            else:
                return False # Ack did not arrive in the expected time
        return True # Ack arrived in the expected time
    
    # Function to send an ACK
    def sendack(self, srcaddr):
        logging.debug(f"Helloooooooooo {srcaddr}")
        ack = "ACK"
        segment = f"{ack}||{srcaddr}|||||"
        self.layer3.from_layer_4(segment)

    # Call this function to send data to this Layer from Layer 5.
    def from_layer_5(self, data, destport, srcport, destaddr):
        global sequencenumber
        logging.debug(f"Layer 4 received msg from Layer 5: {data}")
        # Header implementation
        # Encode the data in base64
        data = base64.b64encode(data.encode("utf-8"))
        data = str(data, "utf-8")
        # Dropped ACKs: implement sequence numbers here
        # The socket is used as unique identifier
        # Header implementation: ACK | [srcaddress] | destaddress | srcport | destport | callback | sequencen
        header = f"|{destaddr}|{srcport}|{destport}|{self.layer_5_cb}|{sequencenumber}"
        sequencenumber = sequencenumber + 1
        segment = f"|{header}|{data}"
        # Pass the message down to Layer 3
        self.layer3.from_layer_4(segment)
        # Now that I've sent the message, I need to stop and wait for the ACK
        ackcheck["ACK"] = 1
        self.timeout() # I want to pass this function to the timeout function and call it back when it's done
        while self.timeout() == False: 
            self.layer3.from_layer_4(segment) # Send segment again

    # Call this function to send data to this Layer from Layer 3
    def from_layer_3(self, segment):
        # Decode the header information and the data
        logging.debug(segment)
        ack, srcaddr, destaddr, srcport, destport, callback, sequencenumber, data = segment.split("|")
        if ack == "ACK":
            # We have received an ACK: can proceed to send next segment
            ackcheck["ACK"] = 0 # Reset the dictionary
            # Send next segment
            logging.debug(f"ACK received")
        else:
            # The segment received is a new segment: pass it to Layer 5
            if callback in sequence: # The socket is already there. Let's check if it's the same sequence number
                if sequence[callback] == sequencenumber:
                    # It's the same. Drop the packet and send another ACK
                    self.sendack(srcaddr)
                else:
                    # It's not the same. Pass the message to layer 5 and update the dictionary
                    sequence[callback] = sequencenumber
                    destport = int(destport)
                    data = base64.b64decode(data)
                    data = str(data, "utf-8")
                    logging.debug(f"Layer 4 received msg from Layer 3: {segment} -> {data} to port {destport} from port {srcport}")
                    # Then, send an ACK back to srcport: in order to recognize the packet as an ACK, the first field is ACK and all others are empty
                    self.sendack(srcaddr)
                    # Implement multiplexing based on the destination port in the header and send the data to Layer 5
                    if destport == 0: # This message is directed to the chat. Let's make it nicer
                        msgformat = "[*] Chat: "
                    else: # This message is directed to the weapon control.
                        msgformat = "[*] Weapon: "
                    connections[destport](data, msgformat)
            else:
                # The socket is not in the dictionary: update the dictionary and pass the message to Layer 5
                sequence[callback] = sequencenumber
                destport = int(destport)
                data = base64.b64decode(data)
                data = str(data, "utf-8")
                logging.debug(f"Layer 4 received msg from Layer 3: {segment} -> {data} to port {destport} from port {srcport}")
                self.sendack(srcaddr) 
                if destport == 0:
                    msgformat = "[*] Chat: "
                else:
                    msgformat = "[*] Weapon: "
                connections[destport](data, msgformat)