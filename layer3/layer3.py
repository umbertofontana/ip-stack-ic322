# This is a stub for Layer 3.

# Import Layers
import sys
from threading import Timer
sys.path.append('../')
import layer2.layer2 as Layer2
import logging
import re


class StubLayer3:
    def __init__(self, layer_4_cb):
        """Create a Layer 3 Object.

        `layer_4_cb` - Function. This layer will use `layer_4_cb` to pass data to Layer 4. `layer_4_cb`
                       must accept a single parameter `data`.
        """
        # Save parameter inputs as instance attributes so they can be referred to later
        self.layer_4_cb = layer_4_cb

        # Connect to Layer 
        self.layer2 = Layer2.StubLayer2(self.from_layer_2)

        # Do you want to send a message without waiting for Layer 4 to call? You
        # can do that any time by calling:
        # get address
        d = self.parse_args()
        self.address = d["addr"]
        #print("my address is :" + self.address)
        #logging.debug(f"the address is {self.address}")


        # self.layer2.from_layer_3("connection successful", interface=2)
    #    t = Timer(30, self.send_discovery_message)
    #    t.start()
    def parse_args(self):
        """A very simple command line argument parser. It supports arguments in the form of
                --key=value
        It will return a Dict such that Dict[key]=value.
        """

        cmd_line_key_values = {}
        for full_arg in sys.argv[1:]: # the first argv value is the process name.
            # strip leading hyphens and split on equal signs
            try:
                k, v = full_arg.strip("-").split("=")
            except ValueError as e:
                raise("Your command line argument {full_arg} is wrong. Make sure you follow the format --key=value and you don't use spaces.")

            cmd_line_key_values[k] = v

        return cmd_line_key_values 
    # sends discovery message to all connected places
    #def send_discovery_message(self):
    #    data = self.create_header("", 0, 1, 2)
    #    ######################DEBUG 
    #    self.layer2.from_layer_3(data, interface=0) 
    #    self.layer2.from_layer_3(data, interface=1) 
    #    #self.layer2.from_layer_3(data, interface=2) 


    #create header
    #message type 1 = ICMP
    def create_header(self, data, destaddr, messagetype, TTL):
        data = str(destaddr) + str(messagetype) + str(TTL) + data
        return data
    
    def delete_header(self, data):
        return data[3:]

    #gets from layer 4
    def from_layer_4(self, segment):
        """Call this function to send data to this layer from layer 4"""
        logging.debug(f"Layer 3 received msg from Layer 4: {segment}")

        # The major job of Layer 3 is to decide which interface to send messages on.
        # You want to "map out" the network (probably using your own Layer 3 messages)
        # and then use some kind of routing algorithm to decide which interface to use.
    
        # Pass the message down to Layer 2; use interface 1.
        # I need to get the destination address and source address from Layer 4 header
        #logging.debug(segment)
        ack, srcaddr, destaddr, srcport, destport, callback, sequencenumber, message = segment.split("|")
        data = f"{ack}|{self.address}|{destaddr}|{srcport}|{destport}|{callback}|{sequencenumber}|{message}"

        data = self.create_header(data, destaddr, 0, 2)
        
        self.layer2.from_layer_3(data, interface=0) 
        #####################DEBUG##################### 
        self.layer2.from_layer_3(data, interface=1) 
        #self.layer2.from_layer_3(data, interface=2) 
        #send data to from_layer_2 while it wait for ack from_layer_2(self, data)

    def from_layer_2(self, data):
        """Call this function to send data to this layer from layer 2"""
        logging.debug(f"Layer 3 received msg from Layer 2: {data}")

        # Is this data addressed to this host? If so, pass it up to the next layer.
        # If not, pass it back down to the correct interface on Layer 2.
        destIP = int(data[0])
        messType = int(data[1])
        TTL = int(data[2])
        #print(str(destIP) + str(messType) + str(TTL))
        data = self.delete_header(data)
        #logging.debug(f"DestIP:{destIP},MessType:{messType},TTL:{TTL},MyAddr:{self.address} -- {data}")
        #logging.debug((destIP == self.address and TTL > 0 and messType == 0))
        #logging.debug(type(self.address))
        #self.layer_4_cb(data)
        if (destIP == int(self.address) and TTL > 0 and messType == 0):
            #logging.debug("Sending to layer 4 now")
            self.layer_4_cb(data)
        elif(messType == 0): #if TTL has expired
            #self.layer_4_cb(data)
            return
        elif(messType == 1):
            TTL -= 1
            #self.layer_4_cb("Connected to computer " + self.address)
        else:
            TTL = TTL - 1
            data = self.create_header(data, destIP, messType, TTL)
            #############DEBUG 
            self.layer2.from_layer_3(data, interface=0) 
            self.layer2.from_layer_3(data, interface=1)
            #self.layer2.from_layer_3(data, interface=2)

    
        # If you're using some kind of "Layer 3 message" to communicate between different
        # hosts' layer 3's (perhaps to do some kind or routing or discoverability), you'll also
        # need to decide whether this data is destined to go to an application (in
        # which case you pass it up to Layer 4) or if it's supposed to be used here in Layer 3.
        # Hopefully you added your own header to it!

        # For now let's just forward this up to layer 4.
        # self.layer_4_cb(data)
