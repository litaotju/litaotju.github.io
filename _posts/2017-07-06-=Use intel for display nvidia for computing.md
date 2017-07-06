---
layout: post
title: Use intel for display nvidia for computing
description: 
category: 
tags: 
---
{% include JB/setup %}


# Problems:

For a iGPU and Nvidia GPU system with Ubuntu 17.04 Desktop, cuda 8.0.  

If use prime-select nvidia, then nvidia GPU are both used as display and computing.  

If use prime-select intel, then nvidia-smi and deviceQuery will not found the Nvidia GPU in system.
and propmts that libnvidia-ml.so can not be found.


# Way to solve:

<pre>
    sudo echo "/usr/lib/nvidia-375" >> /etc/ld.so.conf.d/nvidia.conf
</pre>
note that the path is which contains the libnvidia-ml.so file in your system.


# Ads and Cons of use Intel for display

Normally the CPU fan will have a little noise when in idle mode than GPU in idle mode, if you do not use your system for heavy
tasks. The good thing is you will have more GPU memory for you cuda computing with out the display thing consume you nvidia GPU mem. This is better if you want to use you nvidia GPU for some machine learning tasks, which are normally more memory consuming if you want to exersize on read world data.

# Ref:
>[Nvidia-smi problem solved](https://standbymesss.blogspot.jp/2016/09/ubuntu-nvidia-smi-couldnt-find.html)
