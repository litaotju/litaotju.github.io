---
layout: post
title: NN and Deep Learning
description: 
category: 
tags: 
---
{% include JB/setup %}

1 Chapter 6 Backpropagation Traning
Backpropragation其实就是随机梯度下降法（stochastic gradient descent）。
用于神经网络训练时，计算Error function对于每一个weight的梯度（在现有节点的偏导数），并根据
计算出的梯度来调整weights的方法。一般是将在现有的weights基础上减去learning\_rate 乘以梯度。

现有的很多深度神经网络训练使用该方法是因为这种方法可以有效的利用GPU来进行大规模的训练。（scale very well
on when running on GPU）
