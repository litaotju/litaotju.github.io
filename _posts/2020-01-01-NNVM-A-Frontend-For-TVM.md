---
layout: post
title: NNVM-A-Frontend-For-TVM
description: 
category:  AI
tags: TVM NNVM
---
{% include JB/setup %}

>Note:
NNVM is depracated as of 2020.01, the new frontend is called `relay` in TVM stack.See [Relay from mxnet](https://docs.tvm.ai/tutorials/frontend/from_mxnet.html)

NNVM is a front end compiler for tvm, it could take the models from different DL frameworks, convert into TVM ops, and then use tvm to generate the run-able host/device code. 
Currently (2020.01), it supports the caffe2, coreml, darknet, keras, mxnet, onnx, and tensorflow model format, although not every op of these framework are supported.

See [nnvm/tutorials/from_mxnet.py](https://github.com/litaotju/incubator-tvm/blob/master/nnvm/tutorials/from_mxnet.py)

The main routines called by this script are as followings:

```py
# From mxnet
from mxnet.gluon.model_zoo.vision import get_model
block = get_model('resnet18_v1', pretrained=True)

## compile graph
sym, params = nnvm.frontend.from_mxnet(block)
# we want a probability so add a softmax operator
sym = nnvm.sym.softmax(sym)

import nnvm.compiler
target = 'cuda'
shape_dict = {'data': x.shape}
with nnvm.compiler.build_config(opt_level=3):
    graph, lib, params = nnvm.compiler.build(sym, target, shape_dict, params=params)

##　Run the model using tvm.contrib.graph_runtime

from tvm.contrib import graph_runtime
ctx = tvm.gpu(0)
dtype = 'float32'
m = graph_runtime.create(graph, lib, ctx)

# set inputs
m.set_input('data', tvm.nd.array(x.astype(dtype)))
m.set_input(**params)
# execute
m.run()

# get outputs
tvm_output = m.get_output(0)
top1 = np.argmax(tvm_output.asnumpy()[0])
print('TVM prediction top-1:', top1, synset[top1])
```
