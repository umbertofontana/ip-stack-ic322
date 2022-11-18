import sys
from socket import *
from threading import Thread, Timer

import RPi.GPIO as GPIO
import time
import getopt,sys, logging

# initialized board pins
GPIO.setmode(GPIO.BOARD)

def parse_args():
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

class EdgeCodesLayer1:
    def __init__(self, interface_number, layer_2_cb, enforce_binary=False):
        """Create a Layer 1 Object. This Layer 1 implementation is a "mock"
        in the sense that it does not connect to any GPIO pins. It connects
        with other processes running on the same computer through UDP sockets.

        `layer_2_cb` - Function. This layer will use `layer_2_cb` to pass data to Layer 2. `layer_2_cb`
                       must accept a single parameter `data`. If `enforce_binary` is True, this will be a
                       List of Integers in the form [0, 1, 1, 0, ...]. If `enforce_binary` is false it
                       will be a string.

        `interface_number`  - Integer. Specify the interface number this Layer 1
             instance will be associated with. The pins associated with this interface
             are set using command line arguments. As an example:
                --input1=13 --output1=14 --fliprate1=0.1 --noiserate1=0.1 --droprate=0.2

        `enforce_binary` - Does nothing. Included for backward-compatibility.
        """

        # The pin for interface 1 is defined as a command line argument --input1=12 or some such.
        # The output would be defined as --output2=13.
        args = parse_args()
        self.input_pin = int(args[f"input{interface_number}"])
        self.output_pin = int(args[f"output{interface_number}"])
        self.clock_interval = int(args[f"clock_interval{interface_number}"])

        self.layer_2_cb = layer_2_cb

        # Connect to input and output pins
        logging.debug(f"setting {self.input_pin} as input.")
        logging.debug(f"setting {self.output_pin} as output.")
        GPIO.setup(self.input_pin, GPIO.IN)
        GPIO.setup(self.output_pin, GPIO.OUT)

        # Keep track of the last time we saw the edge of a signal.
        # initialize to current time.
        self.time_last_edge_received = time.time_ns()

        # keep track of output state.
        # 0 = False, 1 = True
        self.output_value = False

        # Keep track of current message between bits.
        # This variable will be a list of 1 and 0 integers.
        self.received_message = []

        # Start listening on input pin
        GPIO.add_event_detect(self.input_pin, GPIO.BOTH, callback=self.receive_edge)
        logging.debug(f"Starting listener on pin {self.input_pin}")

        # Start checking the receive buffer to see if we're ready to send the current message
        # up to layer 2
        t = Thread(target=self.check_end_of_xmission, args=[self.clock_interval*4])
        t.run()


    def from_layer_2(self, data):
        """Receives a List of 1's and 0's from layer 2 and sends them over the interface.

        `data` - List of Integers. Example: [0, 1, 1, 0]
        """

        # Send the bits to a function that modulates the voltage on the pins.
        self.send_and_block(data)

    def receive_edge(self, channel):
        """Called on the rising edge of a signal."""
        # Measure the length of the last signal.
        # If it was 1 clock_interval, it's a 1.
        # If it was 2 clock_intervals, it's a 0.
        # If it's 0, it means it was noise.
        # >2 means restart from idle.
        signal_length = time.time_ns() - self.time_last_edge_received
        intervals = round(abs(signal_length/self.clock_interval))
        self.time_last_edge_received = time.time_ns()
        # logging.debug(f"Received edge after {signal_length}. Clock interval set to {self.clock_interval}. That's {intervals} intervals.")
        if intervals == 1:
            # logging.debug(f"That's a 1!")
            self.received_message.append(1)
            logging.debug(self.received_message)
        elif intervals == 2:
            # logging.debug(f"That's a 0!")
            self.received_message.append(0)
            logging.debug(self.received_message)
        else:
        # we do nothing if the signal was much less than a single clock interval (noise)
        # If the signal was much greater than 2 intervals (restart from idle)....?
            pass

    def check_end_of_xmission(self, check_interval):
        """This function should run every 3 or 4 clock intervals.
        If we have a non-empty message buffer and we haven't received a bit in over 2
        intervals, send the current message buffer up to layer 2.

        The running interval is probably set up in __init__()
        """

        while True:

            # save the value of this variable.
            msg = self.received_message
            #logging.debug(f"Checking if message is complete. Current message: {msg}")

            # do the math to see how long it's been since the last bit was received
            signal_length = time.time_ns() - self.time_last_edge_received
            interval_since_signal = round(abs(signal_length/self.clock_interval))
            
            # if it's been more than 3 intervals, well, the next bit would have to be
            # part of the next message. Send up this message!
            if interval_since_signal > 3 and len(self.received_message)>0:
                logging.debug(f"It's been {interval_since_signal} intervals. Time to send message")
                self.received_message = []
                self.layer_2_cb(msg)

            # Run this function again after the appropriate interval
            #time.sleep(check_interval/1000000000)
            t = Timer(check_interval/1000000000, self.check_end_of_xmission, [check_interval])
            t.start()
            return


    def send_and_block(self, data):
        """Sends data over the interface, but blocks while it does so.
        `data` should be a List of 1,0 values."""
        GPIO.output(self.output_pin, self.output_value)
        for d in data:
            self.output_value = not self.output_value
            logging.debug(f"setting {self.output_pin} to {self.output_value} ({d})")
            GPIO.output(self.output_pin, self.output_value)
            if d == 1:
                time.sleep(self.clock_interval/1000000000)
            if d == 0:
                time.sleep(self.clock_interval/1000000000 * 2)

        self.output_value = not self.output_value
        GPIO.output(self.output_pin, self.output_value)
