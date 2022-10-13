# IC322 Project 1 Template

## Contributing

This repo belongs to your class section. You will be pulling and pushing code to this shared repository. This is how we will share code - remember, you will need to integrate with the layers above and below you; your group won't be operating in a vacuum!

Right now we will all be members of the project with permissions to `push` to the master branch, no "pull request" required. There is a separate folder for each layer. Please only push changes into the folder of the layer your team is assigned to, unless you've spoken to the team that owns the layer you're editing.

When starting work on your protocol, try not to make changes to the existing "mocklayer" files. These mock layers are simple proofs-of-concept that are used to develop *other* layer protocols. In other words, if you make changes to the mock protocols and someone else's layer isn't working, it will be unclear which layer is the problem. 

If you're not familiar with `git`, these last few paragraphs may have been very confusing. Here are some online guides to get you started with `git` quickly:

* [git - the simple guide](https://rogerdudler.github.io/git-guide/)
* [An Intro to Git and GitHub for Beginners](https://product.hubspot.com/blog/git-and-github-tutorial-for-beginners)

If you need push access to this repo, [send an access request](https://docs.gitlab.com/ee/user/project/members/#request-access-to-a-project).

## Quick Start

This template will run a simple networked "application stack". The `run-applications` program will run two Layer 5 applications: a server and a messenger. Run is like this:

```
python3 ./run-applications.py --input1=1201 --output1=1202
```

Each "local process running on your computer" represents a single Raspbery Pi. Open up another terminal window and run another process:

```
python3 ./run-applications.py --input1=1202 --output1=1201
```

Notice that the input1 "pin" on one process is set to the output1 "pin" on the other process. This is how we will simulate connections between Raspberry Pis. When we implement this on real hardware, expect pin numbers to be low numbers, like "3" or "12". When testing on your local computer, set the pin numbers as high numbers like "8000" and "8001". Behind the scenes, this test harness is using local sockets to simulate GPIO pins.

If type a message in one window and press **Enter**, the message should appear in the other window.

## Initializing the network stack

We "run" the network stack by running an Application Layer (Layer 5) program. Each
layer imports the layer below: Layer 5 will import Layer 4, Layer 4 will import
Layer 3, and so-on.

## Communication Between Layers

At a basic level, each layer in the networking stack takes messages from adjacent layers, makes a decision, and then forwards them to another layer. This template makes this explicit. Each layer has two "from_layer" methods: receive from the layer above, and receive from the layer below. The template generally only includes one argument for these functions: `data`, which is the message being passed.

### How/when are these "`from_layer`" methods called?

Let's take Layer 4 as an example.

If Layer 4 wants to send a message to Layer 3, Layer 4 will call Layer 3's `from_layer_4()` method. This is pretty easy since Layer 4 `import`s Layer 3 and will maintain a Layer 3 object:

```python
self.layer3 = Layer3.StubLayer3(self.from_layer_3)
```

This code is written inside the Layer 4 class. It stores a new `StubLayer3` object in an instance variable called `self.layer3`. To call layer 3's `from_layer_4()` method, you can do this:

```python
self.layer3.from_layer_4(data) 
```

But, when we created the `StubLayer3` object, why did we pass it `self.from_layer_3`? This is a method, and it's wierd to send a method as an argument, isn't it?

The answer is that in order for Layer 3 to send a message up to Layer 4, it must know what method to call. By passing Layer 4's `from_layer_3()` method to Layer 3, Layer 3 is able to call that method to send data up to Layer 4. Passing functions to call when "something happens" like this is often called a *callback function*. Which is why the argument name in Layer 3 is called `layer_4_cb`. `cb` stands for "callback". 

`from_layer_4()` method.


### A slight complication: multithreading

Layer 1 will constantly be receiving bits
from over the wire so it must constantly be checking for new data.
To do this, Layer 1's `from_wire()` method is run in its own thread. It will call Layer 2's
`from_layer_1` method when it has new data.

The implication is that in general, data going *up* the layers is running in a different
thread than data going *down* the layers. To be honest, I'm not sure if this will become
a problem for us. But it's good to know!

## Logging

Logging will come in *very* handy during development. It's similar to sprinkling `print` statements throughout your code, except you can trun log output on and off depending on if you're debugging or running production code. You can also very easily choose whether your logs get printed to `stdout` or to a file. 

The example code includes some simple logging statements to get you started.

## Command Line Arguments

I propose we use a very simple command line argument scheme. The Quick Start section has a good example:

```
python3 ./run-applications.py --input1=1201 --output1=1202
```

Each key=value pair is separated by a space and begins with one or more hyphens. Here's how to parse it:

```python
cmd_line_key_values = {}
for full_arg in sys.argv[1:]: # the first argv value is the process name.
    # strip leading hyphens and split on equal signs
    try:
        k, v = full_arg.strip("-").split("=")
    except ValueError as e:
        raise("Your command line argument {full_arg} is wrong. Make sure you follow the format --key=value and you don't use spaces.")
    cmd_line_key_values[k] = v
```
