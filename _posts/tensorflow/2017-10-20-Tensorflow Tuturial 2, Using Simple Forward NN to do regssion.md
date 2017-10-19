---
layout: post
title: Tensorflow Tuturial 2, Using Simple Forward NN to do regssion
description: 
category: machine learning
tags: tensorflow regression
---
{% include JB/setup %}


```python
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
```


```python
# 这个 note book 演示了使用一个全联接前驱神经网络处理
# 来学习一个regression 的问题
```


```python
x_data = np.linspace(-np.pi, np.pi, 100)[:, np.newaxis]
noise = np.random.normal(0, 0.02, x_data.shape)
y_data = np.sin(x_data) + noise
```


```python
#输入神经元
x = tf.placeholder(tf.float32, [None, 1])

y = tf.placeholder(tf.float32, [None, 1])


# 1-N-1 full connectet network,
# activation function using tanh
# 

# 隐含层的神经元个数
NUM_OF_HIDDEN = 20

# 激活函数类型
ACT_FUNC = tf.nn.tanh

#两层神经网络
W = tf.Variable(tf.random_normal([1, NUM_OF_HIDDEN]))
bias = tf.Variable(tf.zeros([1,NUM_OF_HIDDEN]))
z  = ACT_FUNC(tf.matmul(x, W)+bias)

W_output = tf.Variable(tf.random_normal([NUM_OF_HIDDEN,1]))
bias_output = tf.Variable(tf.zeros([1,1]))
predict = ACT_FUNC(tf.matmul(z, W_output)+bias_output)

#损失函数
loss = tf.reduce_mean(tf.square(y-predict))
train = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

```


```python
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for step in range(200):
        sess.run(train, feed_dict={x: x_data, y:y_data})
    prediction_value = sess.run(predict, feed_dict={x:x_data})
    
    plt.figure()
    plt.scatter(x_data, y_data)
    plt.plot(x_data, prediction_value, 'r-')
    plt.show()
```


![png](/img/in-post/tensorflow/nn_reg_1.png)



```python
with tf.Session() as sess:
    NUM_OF_HIDDEN = 5
    ACT_FUNC = tf.nn.sigmoid
    sess.run(tf.global_variables_initializer())
    for step in range(200):
        sess.run(train, feed_dict={x: x_data, y:y_data})
    prediction_value = sess.run(predict, feed_dict={x:x_data})
    
    plt.figure()
    plt.scatter(x_data, y_data)
    plt.plot(x_data, prediction_value, 'r-')
    plt.show()
```


![png](/img/in-post/tensorflow/nn_reg_2.png)

