---
layout: post
title: Cuda Streams Context MPS
description: 
category: AI
tags: CUDA Parallel-Compute
---
{% include JB/setup %}


Cuda 编程模型中存在不同的并行度.
从cuda thread到block，到grid，再到cuda stream，然后上面是cuda context。以及cuda MPS技术。

# Block/Grid
block/grid都是针对一次launch kernel中的不同cuda thread的， cuda programmding model不保证一个kernel中的不同thread的执行顺序，user必须显式的制定同步方式。 block内部，相比block之间（grid内部）有更方便的同步机制，但是GPU也不保证同一个block中的所有threads的执行顺序。Block中的threads是以wrap为单位被schedule到GPU上的SM中的multi processor上的。

# cuda stream 与context
>A CUDA program starts by creating a CUDA context, either explicitly using the driver API or implicitly using the runtime API, for a specific GPU.
有些cuda 程序没有显式的create cuda context那是因为cuda runtime API 已经implicitly帮助user create了一个cuda context。

> All work on the GPU launched using CUDA is launched either explicitly into a CUDA
 stream, or implicitly using a default stream. A stream is a software abstraction that
represents a sequence of commands, which may be a mix of kernels, copies, and other
commands, that execute in order. Work launched in two different streams can execute
simultaneously, allowing for coarse grained parallelism.

> The GPU also has a time sliced scheduler to schedule work from work queues belonging
to different CUDA contexts. Work launched to the compute engine from work queues
belonging to different CUDA contexts cannot execute concurrently.

同一个cuda stream上的 memory/compute task按照顺序执行。不同的cuda stream之间的执行顺序任意。同一个context中的不同stream 可以并发执行,可以并行的占有GPU resource。

但是不同的context，默认是不并发执行的，默认情况下不同context之间按照time slice的方式轮流使用GPU。

但是有了MPS技术之后，不同的context也可以并发的执行，同时使用GPU的资源，这进一步提升了并行的灵活性。pre-Volta GPUs的MPS是通过软件的方式实现的，post volta的GPU，将MPS 的schedule部分直接实现在硬件上，进一步提升了MPS的性能,减少了overhead。


# How to enable MPS
This is not discuss when and how to use MPS to improve the cocurrency, just how to enable mps.
It's very simple:

## Start MPS daemon
```bash
export CUDA_VISIBLE_DEVICES=0 # Select GPU 0.
nvidia-smi -i 0 -c EXCLUSIVE_PROCESS # Set GPU 0 to exclusive mode.
nvidia-cuda-mps-control -d # Start the daemon.
```
任何一个时段，mps control daemon保证只有一个UID能够有一个 MPS server，并且只接受同样的UID的 MPS Client。

MPS Server的创建是由daemon自动的完成的，对user program一般是transparency的。

## Shutdown MPS 

```bash
echo quit | nvidia-cuda-mps-control
```

# Reference
> https://docs.nvidia.com/deploy/pdf/CUDA_Multi_Process_Service_Overview.pdf
