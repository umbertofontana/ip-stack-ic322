# Layer 2, Link Layer Project
# The goal of this program is to simulate the functionality of Layer 2
# Created by Katie Roland, Ben Negron, and Shannon Clancy

# This is a stub for Layer 2.
# Import necessary Libraries
import math
import binascii
import hashlib
import logging
import sys
sys.path.append('../')
# Import Layers 3/1 - > For the next phase of the project
import mocklayer1 as Layer1
#import stub_layer_3 as Layer3

# Layer 2 Stub Layer
class StubLayer2:
    # Layer 2 Constructor
    def __init__(self): # need to pass a layer_3_cb object as well! (once implement)
        #self.layer3 = Layer3.StubLayer3(self.from_layer_3)
        """Create a Layer 2 Object.

        `layer_3_cb` - Function. This layer will use `layer_3_cb` to pass data to Layer 3. `layer_3_cb`
                       must accept a single parameter `data`.
        """
        # Save parameter inputs as instance attributes so they can be referred to later
        #self.layer_3_cb = layer_3_cb

        # Connect to Layer 1 on interfaces 0,1,2, and 3
        self.layer1_interface_0 = Layer1.MockLayer1(interface_number=0, layer_2_cb=self.from_layer_1)
        self.layer1_interface_1 = Layer1.MockLayer1(interface_number=1, layer_2_cb=self.from_layer_1)
        self.layer1_interface_2 = Layer1.MockLayer1(interface_number=2, layer_2_cb=self.from_layer_1)
        self.layer1_interface_3 = Layer1.MockLayer1(interface_number=3, layer_2_cb=self.from_layer_1)

    # This function defines what this class will do when it receives a Layer 3 packet
    def from_layer_3(self, data, interface):
        """Call this function to send data to this layer from layer 3"""
        logging.debug(f"Layer 2 received msg from Layer 3: {data}")
        # Layer 2 takes messages from Layer 3, converts the message to bits, and sends that
        # message down to Layer 1. Layer 1 will transmit the exact bitstream that it is sent.
        # So if your Layer 2 implementation will rely on any kind of "start pattern", length
        # field, or "end pattern", you'll need to add it here -> aka preamble,
        # postamble, and hash information .

        # First, we take the data and compute its hash
        hash_object = hashlib.md5(data.encode())
        hash_value = hash_object.hexdigest()[0:5] # Take 5 digits from the Hash
        data = hash_value + data # Add the hash to the front of the data
        
        #FOR TESTING - > PRINT OUT THE HASH 
        #print("data with computed hash in front: " + str(data))
        
        # converts the string to binary so that is can be sent to layer 1
        binary = ''.join(format(ord(i), '08b') for i in data)
        # add the preamble and postamble (24 bits each) to front/back respectively of the packet
        binary = "010101010101111010001111" + binary + "000011110101000111010101"
# PRINT THE DATA IN BINARY FOR TESTING
        #print("Data in binary: (Ready to send to layer 1)  " + binary)
        # Layer 3 is making the decision about which interface to send the data. Layer 2
        # simply follows Layer 3's directions (and receives the interface number as an
        # argument.

        # PASS THIS MESSAGE TO LAYER 1
        # Pass the message down to Layer 1. 
        # Send the binary string of data down to layer 2
        if interface == 0:
            # Send to interface 0
            self.layer1_interface_0.from_layer_2(binary)
        elif interface == 1:
            self.layer1_interface_1.from_layer_2(binary)
        elif interface == 2:
            self.layer1_interface_2.from_layer_2(binary)
        elif interface == 3:
            self.layer1_interface_3.from_layer_2(binary)
        
        

    # Use this function to convert a string of binary (0's and 1's into a decimal value)
    def BinaryToDecimal(self, binary):
        # Using int function to convert to
        # string
        string = int(binary, 2)
        return string

    # This function dictates what to do when a Layer 1 packet arrives
    def from_layer_1(self, data):
        """Call this function to send data to this layer from layer 1"""
        logging.debug(f"Layer 2 received msg from Layer 1: {data}")

        # The big goal of Layer 2 is to take incoming bits from Layer 1 and convert them into
        # Layer 3 messages. This is where you will put the logic for that. Think about:
        # 1. How will you know if the bits are actually part of a message, or just noise?
        myData = ""
        pre = -1
        post = -1
        # Look for the first 24 bits corresponding to the preamble
        # The purpose of this is so that if there is any noise from layer 1, it will be ignored
        for x in range(len(data)-23):
            if(data[x:x+24] == "010101010101111010001111"):
                pre = x+24
                break # Make sure it only grabs first occurrence, otherwise could be in the middle
            # of the packet's data

        # Look for the postamble to know when the end of the packet has been reached
        for x in range(len(data)-24):
            if(data[x:x+24] == "000011110101000111010101"):
                post = x
            
        # Get the hash (first 40 bits after preamble)
        binHash = data[pre:pre+40]
        # Get the Data payload (after hash)
        myData = data[pre+40:post-16]

        # Get the strings of the hash value and the string data
        ascii_string = ""
        hashString = ""

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
        else:
            # PACKET IS GOOD - > SEND TO LAYER 3 ONCE IT IS RECEIVED
            #    self.layer_3_cb(data)
            print("Packet forwarded to layer 3!")
            # Make sure to only forward to payload 
            #DON'T WANT TO ACCIDENTLY FORWARD THE PREAMBLE/POSTAMBLE/HASH TO
            #LAYER 3 AS WELL B/C IT WON'T KNOW WHAT IT MEANS.
            return
        
        #print(myData)
        # 2. How will you know when a message (a Layer 2 frame) begins?
        # 3. How will you know when a message ends?
        # 4. You will almost certainly *not* receive an entire frame at once. You will
        #    need to save incoming data in some kind of buffer (variable).
        # 5. How will you detect errors? What will you do if you detect an error?

        # Let's just forward this up to layer 3.

# SELF TESTING
# This is the Layer 2 Test Demo
#theData = "Header"
#dataTest = StubLayer2()
#print("Layer 2 Test Demo \n")
# Get the string the user wants to enter 
#userInput = input("Message to Layer 3: ")
#dataTest.from_layer_3(userInput, 6)
#print("\n")

# Get String of binary from layer 1
#userIn = input("Binary from Layer 1: ")
#dataTest.from_layer_1(userIn)
#print("\n")

#userIn2 = input("Binary from Layer 1: ")
#dataTest.from_layer_1(userIn2)
#print("\n")

#dataTest.from_layer_3("Hello World", 6)
#dataTest.from_layer_1("01010101010111101000111101100010001100010011000001100001001110000100100001100101011011000110110001101111001000000101011101101111011100100110110001100100000011110101000111010101")
#dataTest.from_layer_1("100110011Hello Wolrd000011110")
#print(binascii.b2a_uu(0o0011001101100001011000010011000100110100001101100100100001000101010110010100111100001111))
#Sprint(theData)
