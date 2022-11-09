# This is a simple networked application that can both send and
# receive data. Think of it as "telnet".
#00 Weapon
#01 President
#10 Ops Team
#11

import logging
import rsa
import base64
class SimpleApp:
    def __init__(self, layer4):
        """Create a client "process".

        We pass a layer 5 object so that we don't instantiate
        more than one "network stack."
        """
        # Save the layer 4 object as a instance variable
        # so we can reference it later
        self.layer4 = layer4

        # Open a new socket to listen on. Here we're choosing
        # port 80 (just as an example.)
        self.layer4.connect_to_socket(42, self.receive)


    def receive(self, data):
        """Receive and handle a message.
        """
        data = byte(data)
        privKey = rsa.PrivateKey(7819447693201264481039135709488968747282944405313943398033872468126950849215594590967755285022917541482516924432020184769389411093638041450638040061176829, 65537, 3460329615304683956835024701261868434757464541295985266792474011941618145173371088476551933374319798417206937345642701483556248757612233703462454507890113, 5128041281895580149258749664511026672995211778228881629922278305644676752409858009, 1524841018891097170507505317541856826403695634601204816827138486427830981)
        data = rsa.decrypt(data, privKey)
        print(f"Client received message: {data}")

    def send(self, receiver_addr, data):
        """Sends a message to a receiver.
        """
        new_addr = receiver_addr
        if(receiver_addr == "00"): #if it's going to the wep, encrypt with wep pub key
            pubKey = rsa.PublicKey(7132882264518293891057255629051613923589872888832873160419632328344483711061723818042338348168726732969294981138661256440342905879066194621199275217348467, 65537)
            data = rsa.encrypt(data.encode(), pubKey)
        elif(receiver_addr == "01"):
            print("dest 01")
            pubKey = rsa.PublicKey(7819447693201264481039135709488968747282944405313943398033872468126950849215594590967755285022917541482516924432020184769389411093638041450638040061176829, 65537)
            #pubKey = rsa.PublicKey(7208473461486294561945896138899989959413379827135704181163710197248435963953303293438783361216926692179449857866766244851475281639904684175465179331677199, 65537)
            data - rsa.encrypt(data.encode(), pubKey)
        elif(receiver_addr == "10"):
            pubKey = rsa.PublicKey(7226451774345404469318632798730483825880947357790897649669550821736705117675745168820730295174216236921707135603651754203169010229196112982822752289498729, 65537)
            data = rsa.encrypt(data.encode(), pubKey)
            #data = base64.b64encode(data)
        #data = data.decode(encoding='IBM039')
        print(data)
        data = str(data)
        # Send the message to layer 4. We haven't implemented
        # proper addresses yet so we're setting the port numbers
        # and addr to None.
        self.layer4.from_layer_5(data=data, src_port=None,
                dest_port=None, dest_addr=new_addr)
