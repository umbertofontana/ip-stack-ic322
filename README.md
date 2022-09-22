# IC322 Project 1 Template


## 


## Initializing the network stack

We "run" the network stack by running an Application Layer (Layer 5) program. Each
layer imports the layer below: Layer 5 will import Layer 4, Layer 4 will import
Layer 3, and so-on.

## Communication Between Layers

At a basic level, each layer in the networking stack takes messages from
adjacent layers, makes a decision, and then forwards them to another layer.

This template makes this explicit. Each layer has two "receive" methods:
receive from the layer above, and receive from the layer below. The template
generally only includes one argument for these functions: `data`, which is the
message being passed.

### How/when are these "receive" methods called?

Let's take Layer 4 as an example.

If Layer 4 wants to send a message to Layer 3, Layer 4 will call Layer 3's
`from_layer_4()` method. This is pretty easy since Layer 4 `import`s Layer
3 and will maintain a Layer 3 object:

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
