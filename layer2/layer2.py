# Layer 2, Link Layer Project

# The goal of this program is to simulate the functionality of Layer 2
# Created by Katie Roland, Ben Negron, and Shannon Clancy

# Import Necessary Libraries
import math
import binascii
import hashlib
import logging
import sys
sys.path.append('../')
# Import Layers 3/1
# This is important because Layer 2's main role is to pass messages between Layers 1/3
import layer1.EdgeCodesLayer1 as Layer1
import layer3.layer3 as Layer3

# This is the Class for Layer 2
class StubLayer2:
    # Layer 2 Constructor
    def __init__(self, layer_3_cb): 
        """Create a Layer 2 Object.
        `layer_3_cb` - Function. This layer will use `layer_3_cb` to pass data to Layer 3. `layer_3_cb`
                       must accept a single parameter `data`.
        """
        # Save parameter inputs as instance attributes so they can be referred to later
        self.layer_3_cb = layer_3_cb
        
        # Connect to Layer 1 on interfaces 0, 1, 2, and 3
        # This is because the group for Network Layer 3 implemented it with 3 interface: 0, 1, 2, and 3
        self.layer1_interface_0 = Layer1.EdgeCodesLayer1(interface_number=0, layer_2_cb=self.from_layer_1)
        self.layer1_interface_1 = Layer1.EdgeCodesLayer1(interface_number=1, layer_2_cb=self.from_layer_1)
        self.layer1_interface_2 = Layer1.EdgeCodesLayer1(interface_number=2, layer_2_cb=self.from_layer_1)
        self.layer1_interface_3 = Layer1.EdgeCodesLayer1(interface_number=3, layer_2_cb=self.from_layer_1)

    # This function defines what the Layer 2 class will do when it receives a Layer 3 packet from the
    # specified interface
    # Layer 2 takes messages from Layer 3, converts the message to bits, and sends that
        # message down to Layer 1. Layer 1 will transmit the exact bitstream that it is sent.
        # So if your Layer 2 implementation will rely on any kind of "start pattern" (preamble), length
        # field (hash), or "end pattern" (postamble).
    def from_layer_3(self, data, interface):
        """Call this function to send data to this layer from layer 3"""
        logging.debug(f"Layer 2 received msg from Layer 3: {data}")
        
        # First, we take the data and compute its Hashed value using python's built in hashlib() function
        hash_object = hashlib.md5(data.encode())
        hash_value = hash_object.hexdigest()[0:5] # Take 5 digits from the Hash
        data = hash_value + data # Add the hash to the front of the data
        
        # Converts the input string to binary so that is can be sent to layer 1
        binary = ''.join(format(ord(i), '08b') for i in data)
        # add the preamble and postamble (24 bits each) to front/back respectively of the packet
        # This is so that layer 2 will ignore any "noise" it receives from Layer 1 on the wire
        binary = "010101010101111010001111" + binary + "000011110101000111010101"
        
        # Layer 3 is making the decision about which interface to send the data. Layer 2
        # simply follows Layer 3's directions (and receives the interface number as an
        # argument.
        # Pass the message down to Layer 1. 
        if interface == 0:# Send to interface 0
            self.layer1_interface_0.from_layer_2(binary)
        elif interface == 1: # Send to interface 1
            self.layer1_interface_1.from_layer_2(binary)
        elif interface == 2: # Send to interface 2
            self.layer1_interface_2.from_layer_2(binary)
        elif interface == 3: # Send to interface 3
            self.layer1_interface_3.from_layer_2(binary)
        
    # This is a helper function to convert a string of binary digits into a decimal value
    def BinaryToDecimal(self, binary):
        # Using int function to convert to a string
        string = int(binary, 2)
        return string
    
    # This function dictates what Layer 2 does when a Layer 1 packet arrives
     # The big goal of Layer 2 is to take incoming bits from Layer 1 and convert them into
        # Layer 3 messages. This is where you will put the logic for that. Think about:
        # 1. How will you know if the bits are actually part of a message, or just noise?
    def from_layer_1(self, data):
        """Call this function to send data to this layer from layer 1"""
        logging.debug(f"Layer 2 received msg from Layer 1: {data}")
        # Set variables for the data, preamble, and postamble
        myData = ""
        pre = -1
        post = -1
        # Look for the first 24 bits corresponding to the preamble
        # The purpose of this is so that if there is any noise from layer 1, it will be ignored
        for x in range(len(data)-23): 
            if(data[x:x+24] == "010101010101111010001111"): # Look for preamble bits
                pre = x+24
                break # Make sure it only grabs first occurrence, otherwise could be in the middle
            # of the packet's data and lose some of it

        # Look for the postamble to know when the end of the packet has been reached
        for x in range(len(data)-24):
            if(data[x:x+24] == "000011110101000111010101"):
                post = x
            
        # Get the hash (first 40 bits (5 Bytes) after preamble)
        binHash = data[pre:pre+40]
        # Get the Data payload (after hash)
        myData = data[pre+40:post-16]

        # Get the strings of the hash value and the string data
        ascii_string = "" # data string
        hashString = "" # hash value string - > Used for integrity / error checking

        # Convert each byte (8 bits) into a corresponding ASCII character
        # Print the decoding of each ASCII character
        for i in range(0, len(myData)-8, 8):
            an_integer = int(myData[i:i+8], 2)
            ascii_character = chr(an_integer)
            ascii_string += ascii_character

        # Compute the hash value of this data
        hash_Object = hashlib.md5(ascii_string.encode())
        hash_Value = hash_Object.hexdigest()[0:5]

        # Get the hash from the original message
        for i in range(0, len(binHash), 8):
            an_integer = int(binHash[i:i+8], 2)
            ascii_character = chr(an_integer)
            hashString += ascii_character

        # Check to see if the computed hash matches with the packet's hash value    
        if(hash_Value != hashString):
            print("ERROR: Bit error detected, your packet dropped :(")
            return
        else: # This means the given packet's hash matches the computed hash of the packet
            # Forward only data to layer 3
            self.layer_3_cb(ascii_string) # take off pre/post amble and hash 
            return
