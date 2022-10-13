# mock-layer-1.py is a layer 1 that does not send bits over the wire.
# instead, it sends bits between processes on the same computer.
import sys
from socket import *
from threading import Thread
import random, string

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

class MockLayer1:
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
             `fliprate` indicates the probability that a bit will be flipped.
             `noiserate` indicates the probability that a bit will be added or subtracted from the message.
             `droprate` indicates the probability that an entire message will be dropped. This is useful for
                        testing Layer 4 reliable data transfer.

        `enforce_binary` - Bool. Defaults to False. If set to True, this Layer will expect `data` from
                           Layer 2 to be a List of 1's and 0's in the form [0, 1, 0, 1, 1, ...].
                           If set to False, it will expect `data` from Layer 2 to be a string.
        """

        # The pin for interface 1 is defined as a command line argument --input1=12 or some such.
        # The output would be defined as --output2=13.
        # `fliprate` indicates the probability that a bit will be flipped.
        # `noiserate` indicates the probability that a bit will be added or subtracted from the message.
        args = parse_args()
        self.enforce_binary = enforce_binary
        self.input_pin = int(args[f"input{interface_number}"])
        self.output_pin = int(args[f"output{interface_number}"])
        if f"fliprate{interface_number}" in args.keys():
            self.flip_rate = float(args[f"fliprate{interface_number}"])
        else:
            self.flip_rate = 0

        if f"noiserate{interface_number}" in args.keys():
            self.noise_rate = float(args[f"noiserate{interface_number}"])
        else:
            self.noise_rate = 0

        if f"droprate{interface_number}" in args.keys():
            self.drop_rate = float(args[f"droprate{interface_number}"])
        else:
            self.drop_rate = 0

        # Connect to input pin
        self.input_socket = socket(AF_INET, SOCK_DGRAM)
        self.input_socket.bind(("127.0.0.1", self.input_pin))
        self.input_socket.setblocking(False) # set non-blocking

        # Connect to output pin
        self.output_socket = socket(AF_INET, SOCK_DGRAM)

        # Start Listener
        self.listen(layer_2_cb)

    def from_layer_2(self, data):
        """Receives a List of 1's and 0's from layer 2 and sends them over the interface.

        `data` - List of Integers. Example: [0, 1, 1, 0]
        """

        # Simulate packet dropping
        if random.randint(0, 100) < self.drop_rate * 100:
            return

        # Convert the List of Ints into a string. (The if statement isn't strictly needed,
        # but it makes the code clearer.)
        if self.enforce_binary:
            data_string = "".join([str(x) for x in data])
            # simulate bit flips and noise
            for i,b in enumerate(data):
                if random.randint(0, 100) < self.flip_rate * 100:
                    data_string = data_string[0:i] + str((int(data_string) + 1) % 2) + data_string[i+1:]
                if random.randint(0, 100) < self.noise_rate * 100:
                    if random.randint(0,1) == 0: 
                        # add bit
                        data_string = data_string[0:i] + str(randint(0,1))+ data_string[i:]
                    else:
                        # drop bit
                        data_string = data_string[0:i] + data_string[i+1:]
        else:
            data_string = data
            # simulate bit flips and noise
            for i,b in enumerate(data):
                if random.randint(0, 100) < self.flip_rate * 100:
                    data_string = data_string[0:i] + random.choice(string.ascii_letters) + data_string[i+1:]
                if random.randint(0, 100) < self.noise_rate * 100:
                    if random.randint(0,1) == 0: 
                        # add bit
                        data_string = data_string[0:i] + random.choice(string.ascii_letters) + data_string[i:]
                    else:
                        # drop bit
                        data_string = data_string[0:i] + data_string[i+1:]

        self.output_socket.sendto(data_string.encode(),("127.0.0.1", self.output_pin))

    def listen(self, callback):
        """Listens to the input queue and calls `callback` with
        data when something is received.
        """
        t = Thread(target=self.from_wire, args = (callback,))
        t.start()
        return

    def from_wire(self, callback):
        while True:
            try:
                # the `address` value is an implementation detail here; we
                # will discard it.
                data, address = self.input_socket.recvfrom(2048)
                
                # convert data from a string to a List of Ints
                if self.enforce_binary:
                    parsed_data = [int(x) for x in data.decode()]
                else:
                    parsed_data = data.decode()
                callback(parsed_data)
            except BlockingIOError:
                pass

