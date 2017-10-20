---
layout: post
title: Wired things when using jupyter to write tensorflow summary
description: 
category: 
tags: 
---
{% include JB/setup %}

When using jupyter notebook, and try to using 

```
tf.summary.scalar('loss', loss)
merged = tf.summary.merge_all()
with tf.Session() as sess:
    train_writer = tf.summary.FileWriter('./train', sess.graph)
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

This will success when the first time you open a notebook and run the code.
But will fail, when you want to run the same cell again

But same exactly code, will pass and generated correact report when directly running the code.
