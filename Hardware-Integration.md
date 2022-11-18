# Hardware Integration Guide


## Step 1: Get your code onto the Raspberry Pis.

The Raspberry Pi 2's that we have do not include wifi. In order to get your code onto them, you will have to connect to them from a computer with internet access.

### Set a static IP on your Pi

Connect the Pi to a monitor, keyboard, and mouse. After it boots up, edit `/etc/dhcpcd.conf` and set the following lines. In this example we're adding the hardware in the 192.168.0.0/24 subnet.
```
interface eth0
static ip_address=192.168.0.10/24 # Make this different for every Pi
static routers=192.168.0.254
```

You will have to do this for every Pi you want to use.

### Physically connect your hardware

Connect each Pi to a Hub with an Ethernet cable. Then, connect your "internet" computer to the hub also using an Ethernet cable. 

### Set up a static IP on your "internet" computer

Whichever computer you're using to develop on, perhaps it's your laptop, set a static IP. This option may only become available *after* you plug in the Ethernet cable. The correct setting screen will vary between operating systems, but look for "Wired Connection" and set a "Manual" or "Static" IP in the same subnet as you set your Pis.

### SSH into the Pi to make sure you're connected

Connect to the Pi with the following command (substitute the correct IP address)

```
ssh pi@192.168.0.10
```

The default password for the Pis is `raspberry`.


### Mount the Raspberry Pi's filesystem

Use `sshfs` to mount the Pi's filesystem on your computer. This will allow you to save files on the Pis. I included a script called `mount-pi.sh` that helps out with this. You can use it using the following command:

```
./mount-pi.sh pi1 192.168.0.10
```

Where `pi1` is a nickname you're giving that Pi so you can keep track of multiple connections. This script will create a new folder *above* the one you run it in that has the Pi's filesystem mounted.

## Step 2: Connect the hardware

The new `EdgeCodesLayer1.py` layer should be a drop-in replacement for the `mocklayer1.py` code. The pin numbers are different, though. Now, instead of choosing arbitrary values, you have to choose the correct pin numbers used on the Raspberry Pi! Use this diagram to identify pin numbers (use the numbers in the middle, on the actual pins, not the numbers after "GPIO".)

[Raspberry Pi Pinout](https://learn.sparkfun.com/tutorials/introduction-to-the-raspberry-pi-gpio-and-physical-computing/gpio-pins-overview)

When connecting input pins to output pins, be sure to add a resistor between the input and output pins. If you make a mistake and accidentally connect an input pin to an input pin, you will create a lot of current and fry the board without these inline resistors.

Also connect the grounding pins on each board together.

