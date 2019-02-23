---
layout: post
title: Tensorflow Tutorial 3, Visualizing your model and training
description: 
category: 
tags: 
---
{% include JB/setup %}

```
# coding: utf-8
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os

x_data = np.linspace(-np.pi, np.pi, 100)[:, np.newaxis]
noise = np.random.normal(0, 0.02, x_data.shape)
y_data = np.sin(x_data) + noise

# 将var 的各种计量加入到 name scope下的summary
def variable_summaries(var,name):
    with tf.name_scope(name):
        mean = tf.reduce_mean(var)
        tf.summary.scalar('mean', mean)
        with tf.name_scope('stddev'):
            stddev = tf.sqrt(tf.reduce_mean(tf.square(var-mean)))
        tf.summary.scalar('stddev', stddev)
        tf.summary.scalar('max', tf.reduce_mean(var))
        tf.summary.scalar('min', tf.reduce_mean(var))
        tf.summary.histogram('histogram', var)

def variables_summaries(iterable):
    for var,name in iterable:
        variable_summaries(var, name)

#输入神经元
x = tf.placeholder(tf.float32, [None, 1], name="x")
y = tf.placeholder(tf.float32, [None, 1], name="y")

# 1-N-N-1 full connectet network,
# activation function using tanh

# 隐含层的神经元个数
NUM_OF_HIDDEN = 20

# 激活函数类型
ACT_FUNC = tf.nn.tanh

#两层神经网络
with tf.name_scope("layer1"):
    W = tf.Variable(tf.random_normal([1, NUM_OF_HIDDEN]), name="weight")
    bias = tf.Variable(tf.zeros([1,NUM_OF_HIDDEN]), name="bias")
    z  = ACT_FUNC(tf.matmul(x, W)+bias, name="activity")
    variables_summaries([(W, 'weight'), (bias, 'bias'), (z, 'z')])


with tf.name_scope('layer2'):
    W_output = tf.Variable(tf.random_normal([NUM_OF_HIDDEN,1]), name="weight")
    bias_output = tf.Variable(tf.zeros([1,1]), name="bias")
    predict = ACT_FUNC(tf.matmul(z, W_output)+bias_output, name="predict")
    variables_summaries([(W_output, 'weight'), (bias_output, 'bias'), (predict, 'output')])

#损失函数
loss = tf.reduce_mean(tf.square(y-predict), name="loss")
train = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

variables_summaries([(loss, 'loss')])
merged = tf.summary.merge_all()

with tf.Session() as sess:
    logdir = "./train"
    train_writer = tf.summary.FileWriter(logdir, sess.graph)
    sess.run(tf.global_variables_initializer())
    for step in range(200):
        summ, _ = sess.run([merged, train], feed_dict={x: x_data, y:y_data})
        train_writer.add_summary(summ, step)
    prediction_value = sess.run(predict, feed_dict={x:x_data})
    plt.figure()
    plt.scatter(x_data, y_data)
    plt.plot(x_data, prediction_value, 'r-')
    plt.show()
```
