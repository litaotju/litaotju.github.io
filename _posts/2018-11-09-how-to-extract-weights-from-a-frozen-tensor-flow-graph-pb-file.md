---
layout: post
title: How to extract weights from a frozen tensor flow graph pb file 
description: ""
category: AI
tags: 
  - Code snippets
---


```
import tensorflow as tf
import sys


## In tensorflow the weights are also stored in constants ops
## So to get the values of the weights, you need to run the constant ops
## It's a little bit anti-intution, but that's the way they do it

#construct a GraphDef
pbFile = sys.argv[1]
graph_def = tf.GraphDef()
with open(pbFile, 'rb') as f:
    graph_def.ParseFromString(f.read())

#import the GraphDef to the global default Graph
tf.import_graph_def(graph_def, name='')


# extract all the constant ops from the Graph
# and run all the constant ops to get the values (weights) of the constant ops
constant_values = {}
with tf.Session() as sess:
    constant_ops = [op for op in sess.graph.get_operations() if op.type == "Const"]
    for constant_op in constant_ops:
        value =  sess.run(constant_op.outputs[0])
        constant_values[constant_op.name] = value

        #In most cases, the type of the value is a numpy.ndarray.
        #So, if you just print it, sometimes many of the values of the array will
        #be replaced by ...
        #But at least you get an array to python object, 
        #you can do what other you want to save it to the format you want

        print constant_op.name, value
```
