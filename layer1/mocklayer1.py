# mock-layer-1.py is a layer 1 that does not send bits over the wire.
# instead, it sends bits between processes on the same computer.
from socket import *
from threading import Thread

class MockLayer1:
    def __init__(self, input_pin, output_pin, receiver_cb):
        """Create a Layer 1 Object. This Layer 1 implementation is a "mock"
        in the sense that it does not connect to any GPIO pins. It connects
        with other processes running on the same computer through UDP sockets.

        `input_pin`  - Integer. This layer will monitor a port associated with this
                       number and call `receiver_cb` whne data is received.
        `output_pin` - Integer. When calling `send`, this layer will send the data over
                       a port associated with this number.
        """

        self.input_pin = input_pin
        self.output_pin = output_pin

        # Connect to input pin
        self.input_socket = socket(AF_INET, SOCK_DGRAM)
        self.input_socket.bind(("127.0.0.1", self.input_pin))
        self.input_socket.setblocking(False) # set non-blocking

        # Connect to output pin
        self.output_socket = socket(AF_INET, SOCK_DGRAM)

        # Start Listener
        self.listen(receiver_cb)

    def from_layer_2(self, data):
        self.output_socket.sendto(data.encode(),("127.0.0.1", self.output_pin))

    def listen(self, callback):
        """Listens to the input queue and calls `callback` with
        data when something is received."""
        t = Thread(target=self.read, args = (callback,))
        t.start()
        return

    def read(self, callback):
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
