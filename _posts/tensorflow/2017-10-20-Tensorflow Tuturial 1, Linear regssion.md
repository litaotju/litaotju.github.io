---
layout: post
title: Tensorflow Tuturial 1, Linear regssion
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
# linera regression model

#定义变量
x_data = np.random.rand(100)
y_data = x_data * 0.1 + 0.2
b = tf.Variable(0.)
k = tf.Variable(0.)

y = k*x_data + b

# 二次代价函数
loss = tf.reduce_mean(tf.square(y_data - y))

#定义一个梯度下降算法来进行优化
optimizer = tf.train.GradientDescentOptimizer(0.2)

#最小化代价函数
train = optimizer.minimize(loss)
```


```python
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for step in range(100):
        sess.run(train)
        if step % 20 == 0:
            print(step, sess.run([k, b, loss]))
    predict = sess.run(y)
    plt.figure()
    plt.scatter(x_data, y_data)
    plt.plot(x_data, predict, "r")
    plt.show()
```

    (0, [0.049643345, 0.098832183, 0.015791332])
    (20, [0.10022645, 0.19988607, 4.0441082e-09])
    (40, [0.10013604, 0.19993165, 1.4586133e-09])
    (60, [0.10008168, 0.19995897, 5.2587124e-10])
    (80, [0.10004906, 0.19997536, 1.8971365e-10])


![png](/img/in-post/tensorflow/linear_reg.png)

