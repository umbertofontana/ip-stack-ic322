# mock-layer-1.py is a layer 1 that does not send bits over the wire.
# instead, it sends bits between processes on the same computer.
import sys
from socket import *
from threading import Thread

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
    def __init__(self, interface_number, layer_2_cb):
        """Create a Layer 1 Object. This Layer 1 implementation is a "mock"
        in the sense that it does not connect to any GPIO pins. It connects
        with other processes running on the same computer through UDP sockets.

        `layer_2_cb` - Function. This layer will use `layer_2_cb` to pass data to Layer 2. `layer_2_cb`
                       must accept a single parameter `data`.

        `interface_number`  - Integer. Specify the interface number this Layer 1
             instance will be associated with. The pins associated with this interface
             are set using command line arguments. As an example:
                --input1=13 --output1=14
        """

        # The pin for interface 1 is defined as a command line argument --input1=12 or some such.
        # The output would be defined as --output2=13.
        args = parse_args()
        self.input_pin = int(args[f"input{interface_number}"])
        self.output_pin = int(args[f"output{interface_number}"])

        # Connect to input pin
        self.input_socket = socket(AF_INET, SOCK_DGRAM)
        self.input_socket.bind(("127.0.0.1", self.input_pin))
        self.input_socket.setblocking(False) # set non-blocking

        # Connect to output pin
        self.output_socket = socket(AF_INET, SOCK_DGRAM)

        # Start Listener
        self.listen(layer_2_cb)

    def from_layer_2(self, data):
        self.output_socket.sendto(data.encode(),("127.0.0.1", self.output_pin))

    def listen(self, callback):
        """Listens to the input queue and calls `callback` with
        data when something is received."""
        t = Thread(target=self.from_wire, args = (callback,))
        t.start()
        return

    def from_wire(self, callback):
        while True:
            try:
                # the `address` value is an implementation detail here; we
                # will discard it.
                data, address = self.input_socket.recvfrom(2048)
                callback(data.decode())
            except BlockingIOError:
                pass

if __name__ == "__main__":
    pass
