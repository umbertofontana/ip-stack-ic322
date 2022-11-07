[*] INITIAL STEPS

> l4-run-applications.py
Assuming that there's a chat client, that interacts with other chat clients and can be used to send messages, and a weapon interface that can only receive commands.
The chat client is started on port 0, and the weapon is started on port 1. They can be easily changed, but they need to be standardized in order to know where to send the data.
Both threads, when opened, call SimpleApp passing their port numbers and the object Layer 4.
The chat client waits for a message, asks if it is for the other chat client or if it is a command for the weapon, and sends it by calling the send function with the source port, the destination port and the message as arguments.

> l4_simple_app.py
The first time simple_app gets called, it calls the connect_to_socket function from Layer 4, passing the receive function as callback and its own port. 
 
> l4_layer4.py
When connection_to_socket gets called, it updates its connections dictionary with the values {port:layer5_cb(receive function from above)}. By doing that, it will know which callback function to call when data is destined to a certain port (basically, which socket to use).

The sockets are now set-up.

[*] SEND A MESSAGE/COMMAND

> l4-run-applications.py
After typing a message, the script asks for the port to send it to (chat or weapon). It then passes those values to the send function of SimpleApp.

> l4_simple_app.py
Simple_app simply calls the function from_layer_5 of layer4, passing the message, the source port, the destination port and the destination address as arguments. For now, the receiver address is set to None, but it can be easily implemented.

> l4_layer4.py
The first step is to attach its header, that has the format "{dest.port}|{src.port}|{callback.function}|{sequencenumber}". This header gets attached to the message, that is now encoded in Base64. The whole segment is then passed to layer3, the sequence number is increased by 1, and it starts to wait for an ACK by updating ackcheck to 1. 
The timeout function is then called: if the ACK is not received in the intended time, the segment will be sent again (stop-and-wait protocol). 

Now, on the other client, the segment will eventually arrive. Layer 3 calls the from_layer_3 function, passing the segment as argument. 
The header information and the encoded data is retrieved. First, Layer 3 checks if the segment is an ACK. 
In this case it's not, so it will ignore it. 
Then, it will check if the sequence number is the same as the last segment received from that address (at this stage I'm using callback functions as a way to identify an address. It will be easy to implement the address system developed by layer3 by changing the header format (switch callback.function to source.address).

If the sequence number is the same, an ACK will be sent to that address and the message will not be passed to Layer 5 (in order to avoid duplicate messages).

If the sequence number is new, the sequence dictionary is updated, the message is decoded from Base64, an ACK is sent to the source address (in this case, since the source address is a callback function, we do not pass anything). Multiplexing is then implemented, by evaulating the destination port and choosing the right thread (callback function) to send the message to.





