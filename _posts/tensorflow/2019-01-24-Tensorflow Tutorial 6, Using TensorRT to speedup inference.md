---
layout: post
title: Tensorflow Tutorial 6, Using TensorRT to speedup inference
description: 
category: 
tags: 
---
{% include JB/setup %}

# Workflows to use TensorFlow-TensorRT (TF-TRT)

There are three workflow to use TF-TRT, based on the Tensorflow model format. They are SavedModel, metagraph/checkpoint, frozen_graph.

## TF-TRT workflow using SavedModel
If you have a SavedModel representation of your TensorFlow model, you can create a TensorRT inference graph directly from your SavedModel, for example:
```python
# Import TensorFlow and TensorRT
import tensorflow as tf
import tensorflow.contrib.tensorrt as trt
# Inference with TF-TRT `SavedModel` workflow:
graph = tf.Graph()
with graph.as_default():
    with tf.Session() as sess:
        # Create a TensorRT inference graph from a SavedModel:
        trt_graph = trt.create_inference_graph(
            input_saved_model_dir=”/path/to/your/saved/model”,
            input_saved_model_tags=[”your_saved_model_tags”],
            max_batch_size=your_batch_size,
            max_workspace_size_bytes=max_GPU_mem_size_for_TRT,
            precision_mode=”your_precision_mode”) 
        # Import the TensorRT graph into a new graph and run:
        output_node = tf.import_graph_def(
            trt_graph,
            return_elements=[“your_outputs”])
       sess.run(output_node)
```
Where, in addition to `max_batch_size`, `max_workspace_size_bytes` and `precision_mode`, you need to supply the following arguments to create_inference_graph:

* input_saved_model_dir  
    Path to your SavedModel directory.
* input_saved_model_tags  
    A list of tags used to identify the MetaGraphDef of the SavedModel to load.
And where:
*  [“your_outputs”]  
    A list of the name strings for the final result nodes in your graph.

## TF-TRT Workflow With A Frozen Graph
If you have a frozen graph of your TensorFlow model, you first need to load the frozen graph file and parse it to create a deserialized GraphDef. Then you can use the GraphDef to create a TensorRT inference graph, for example:
```python
# Import TensorFlow and TensorRT
import tensorflow as tf
import tensorflow.contrib.tensorrt as trt
# Inference with TF-TRT frozen graph workflow:
graph = tf.Graph()
with graph.as_default():
    with tf.Session() as sess:
        # First deserialize your frozen graph:
        with tf.gfile.GFile(“/path/to/your/frozen/graph.pb”, ‘rb’) as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
        # Now you can create a TensorRT inference graph from your
        # frozen graph:
        trt_graph = trt.create_inference_graph(
            input_graph_def=graph_def,
            outputs=[“your_output_node_names”],
            max_batch_size=your_batch_size,
            max_workspace_size_bytes=max_GPU_mem_size_for_TRT,
            precision_mode=”your_precision_mode”)
        # Import the TensorRT graph into a new graph and run:
        output_node = tf.import_graph_def(
            trt_graph,
            return_elements=[“your_outputs”])
        sess.run(output_node)
```

Where, again in addition to max_batch_size, max_workspace_size_bytes, and precision_mode, you need to supply the following argument to create_inference_graph:
* outputs  
    A list of the name strings for the final result nodes in your graph.
And where:
* “/path/to/your/frozen/graph.pb”  
    Path to the frozen graph of your model.
* [“your_outputs”]  
    A list of the name strings for the final result nodes in your graph. Same as outputs above.

## TF-TRT workflow with a metagraph/ checkpoint files
If you don’t have a SavedModel or a frozen graph representation of your TensorFlow model but have separate MetaGraph and checkpoint files, you first need to use these to create a frozen graph to then feed into the create_inference_graph function, for example:
```python
# Import TensorFlow and TensorRT
import tensorflow as tf
import tensorflow.contrib.tensorrt as trt
# Inference with TF-TRT `MetaGraph` and checkpoint files workflow:
graph = tf.Graph()
with graph.as_default():
    with tf.Session() as sess:
        # First create a `Saver` object (for saving and rebuilding a
        # model) and import your `MetaGraphDef` protocol buffer into it:
        saver = tf.train.import_meta_graph(“/path/to/your/model.ckpt.meta”)
        # Then restore your training data from checkpoint files:
        saver.restore(sess, “/path/to/your/model.ckpt”)
        # Finally, freeze the graph:
               your_outputs = [“your_output_node_names”]
        frozen_graph = tf.graph_util.convert_variables_to_constants(
            sess,
            tf.get_default_graph().as_graph_def(),
            output_node_names=[“your_outputs”])
        # Now you can create a TensorRT inference graph from your
        # frozen graph:
        trt_graph = trt.create_inference_graph(
            input_graph_def=frozen_graph,
            outputs=[“your_outputs”],
            max_batch_size=your_batch_size,
            max_workspace_size_bytes=max_GPU_mem_size_for_TRT,
            precision_mode=”your_precision_mode”)
        # Import the TensorRT graph into a new graph and run:
        output_node = tf.import_graph_def(
            trt_graph,
            return_elements=[“your_outputs”])
        sess.run(output_node)
``` 
Where, again in addition to max_batch_size, max_workspace_size_bytes and precision_mode, you need to supply the following argument to create_inference_graph:
* outputs  
    A list of the name strings for the final result nodes in your graph.
And where:
* “/path/to/your/model.ckpt.meta”  
    Path to the MetaGraphDef protocol buffer of your model. This is usually created and saved during training.
* “/path/to/your/model.ckpt”  
    Path to your latest checkpoint file saved during training.
* [“your_outputs”]  
    A list of the name strings for the final result nodes in your graph. Same as outputs above.

# Change the facenet model to use TF-TRT
To change the facenet model to use TF-TRT, you need to change the load_model, to make it return the graph_def of a frozen_graph.
The complete code is here: https://github.com/litaotju/facenet/tree/tf-trt

## Return froze_graph graph_def for load_model
```diff
-def load_model(model, input_map=None, use_trt=False):
+def load_model(model, input_map=None):
     # Check if the model is a model directory (containing a metagraph and a checkpoint file)
     #  or if it is a protobuf file with a frozen graph
+    # input_map: the input_map provied to tf.import_graph_def to replace a list of tensors
+    # return: None
     model_exp = os.path.expanduser(model)
+    graph_def = tf.GraphDef()
     if (os.path.isfile(model_exp)):
         print('Model filename: %s' % model_exp)
         with gfile.FastGFile(model_exp,'rb') as f:
-            graph_def = tf.GraphDef()
             graph_def.ParseFromString(f.read())
             if input_map is not None:
                 nodes_names = [node.name for node in graph_def.node]
                 for i in input_map:
                     assert i in nodes_names, "%s is not in graph" % i
-            tf.import_graph_def(graph_def, input_map=input_map, name="")
-
     else:
         print('Model directory: %s' % model_exp)
         meta_file, ckpt_file = get_model_filenames(model_exp)
         
         print('Metagraph file: %s' % meta_file)
         print('Checkpoint file: %s' % ckpt_file)
-      
-        saver = tf.train.import_meta_graph(os.path.join(model_exp, meta_file), input_map=input_map)
-        saver.restore(tf.get_default_session(), os.path.join(model_exp, ckpt_file))
+
+        # The graph and the session will be destroyed when exiting the context
+        with tf.Graph().as_default():  
+            with tf.Session() as sess:
+                saver = tf.train.import_meta_graph(os.path.join(model_exp, meta_file), clear_devices=True)
+                tf.get_default_session().run(tf.global_variables_initializer())
+                tf.get_default_session().run(tf.local_variables_initializer())
+                saver.restore(tf.get_default_session(), os.path.join(model_exp, ckpt_file))
+                graph_def = sess.graph.as_graph_def()
+                graph_def = freeze_graph_def(sess, graph_def, 'embeddings,label_batch')
+        assert graph_def
+    return graph_def
```

##  Change evluation fucntion
```bash
+    always_print = True
 
-    input_map = {'image_batch': image_batch, 'label_batch': label_batch, 
+    graph_def = facenet.load_model(args.model, input_map=None)
+
+    if always_print:
+        for node in graph_def.node:
+            print("TF", node.name, node.op)
+
+    if args.use_trt:
+        print("Using TensorRT to speedup inference")
+        graph_def = trt.create_inference_graph(
+            input_graph_def=graph_def,
+            outputs=["embeddings"],
+            max_batch_size=100,
+            max_workspace_size_bytes=2<<10,
+            precision_mode="FP32")
+        if always_print:
+            for node in graph_def.node:
+                print("TF-TRT", node.name, node.op)
+
+    batch_size_placeholder = tf.placeholder(tf.int32, name='batch_size')
+    phase_train_placeholder = tf.placeholder(tf.bool, name='phase_train')
+    image_batch, label_batch, initializer = create_dataset(image_paths_array, 
+                        labels_array, control_array, image_size, batch_size)
+    input_map = {'image_batch': image_batch, 
                   'phase_train': phase_train_placeholder,
                   'batch_size':  batch_size_placeholder}
-
-    # Load the model,
-    # Replace the original graph's input with the dataset batches generate by 
-    # tf.data.Iterator.get_next()
-    facenet.load_model(args.model, input_map=input_map, use_trt=args.use_trt)
-    logdir = "./logdir_pb" if os.path.isfile(args.model) else "./logdir_ckpt"
-    writer = tf.summary.FileWriter(logdir, sess.graph)
-    writer.close()
+    if not args.use_trt:
+        input_map['label_batch'] = label_batch
+    tf.import_graph_def(graph_def, input_map=input_map, name="")
```

##  Perfmance comparison

### Configs

Here the configs and perf number results before/after using TensorRT optimized flow.

* GPU: Nvidia GTX 1060 6GB
* Nvidia Driver: 410.78
* CPU: Intel I5-7500
* OS: Ubuntu 18.04 with Linux kernel 4.15.0-43
* TensorRT: 4.0.1.6
* Cuda: 9.0
* Cudnn: cudnn_version_7_1_4_18_c24081344_m0_e0
* TensorFlow-GPU: 1.10
* Python: 3.6.6  
* Facenet: [e24b16e](https://github.com/litaotju/facenet/commit/e24b16ef053f0bd070660816f2742561c5ec4909)

*** Results:
At batch 100, image_size 160*160, on LFW dataset, using `time.process_time` to measure the time per batch run, and compute the mean of all batches
of 12000 images.
*  TF - Checkpoint flow [TIME] Avg runtime per batch: 0.27434
*  TF - Frozen Graph flow [TIME] Avg runtime per batch: 0.29229
*  TF-TRT - Checkpoint flow [TIME] Avg runtime per batch: 0.24401
*  TF-TRT - Frozen Graph flow [TIME] Avg runtime per batch: 0.24620

The speed up is about 1.125 on FP32 precision, without any acurray loss.

# Tips of using TF-TRT

* Do not add anything to default graph before using trt.create_inference_graph
* Pass infomation using serailizable graph_def object
* Convert the restored session's graph to frozen_graph graph_def, and then use frozen_graph flow.
* Pay attention to the `outputs` parameter, TensorRT will optimize away the unused tensor/operation not contributed to output.
* Pay attention to `max_batch_size` parameter, use the batch size you most likely to use. If you are not sure, save servel batch_size TensorRT optimized graph.
  Then use the matched one to do inference. This is because  `batch_size` matters for optimization.

## Reference
> [https://docs.nvidia.com/deeplearning/dgx/integrate-tf-trt/index.html#using-metagraph-checkpoint](https://docs.nvidia.com/deeplearning/dgx/integrate-tf-trt/index.html#using-metagraph-checkpoint)
