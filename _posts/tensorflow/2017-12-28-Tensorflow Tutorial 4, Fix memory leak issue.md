---
layout: post
title: Tensorflow Tutorial 4, Fix memory leak issue
description: 
category: AI
tags: 
---
{% include JB/setup %}

# Problems and soloving method
Orignally, I use the code like the following code.
I found that the memory will increase as the training goes on, and finally my computer will run out of memory
and stuck there when many training steps was done.

```
#...import 
#...build your model

with tf.Session() as sess:
    logdir = "./train"
    train_writer = tf.summary.FileWriter(logdir, sess.graph)
    sess.run(tf.global_variables_initializer())
    #...
    for step in range(200):
        #use some functions like, tf.reshape, tf.image.resize
        #inside the for loop
        summ, _ = sess.run([merged, train], feed_dict={x: x_data, y:y_data})
        train_writer.add_summary(summ, step)
        #...
    #...
```

Google searched that, using the functions like "tf.reshape(), tf.image.resize()" etc. will add new operations to the graph.
Since each iteration there are new operation added to graph, the graph will becose bigger and bigger, and memory will drain out.

So I changed my code to structure like following

```
#...import 
#...build your model

with tf.Session() as sess:
    logdir = "./train"
    train_writer = tf.summary.FileWriter(logdir, sess.graph)
    sess.run(tf.global_variables_initializer())
    #...
    #move the tf.reshape, tf.image.resize outside the for-loop
    someTensor = tf.reshape(someOtherTensor)
    
    #use tf.Graph.finalize() to freeze the graph, make sure the for-loop 
    #do not change the structure of the graph, only the value will be updated.
    sess.graph.finalize()
    for step in range(200):
        #evaluation the resize/reshape tensor
        val = sess.run(someTensor)
        #...use the val

        summ, _ = sess.run([merged, train], feed_dict={x: x_data, y:y_data})
        train_writer.add_summary(summ, step)
        #...
    #...
```

# Tips

1. Put all the tensor that adds new op to graph outside the for-loop for training
2. Use tf.Graph.finalize() to freeze the graph, and confirm no one changes it inside the for-loop.
3. Keep an eye on the tensor inside training loop, only evaluation should be done.
    Keep as litte as code in-side for-loop, so you can have neat control.
