---
layout: post
title: How I optimized my python profile program
description: 
category: python
tags: Optmization Parallel Profile Acceleration
---
{% include JB/setup %}

## Background

In this article, I am trying to describe a short journey on how I optimize my python program. Which is using `opencv`, `numpy` and `tensorflow` for a cv tasks around a deep Learning model. This article only focus on the **inference** part, training part is outside the scope.

TODO: what programming we are targeted. What's the workload? and What's the betteneck?

## How to profile and the APOD cycle

### Different profiling tools, and quick start

- cProfile
- profilehooks
- Intel VTune
- Nvidia Nsight system
- time.perf_counter()
- `%timeit` in ipython and jupyter

#### Hotspot and uarch exploration

```bash
## This will collect the hw metrics.
amplxe-cl -c uarch-exploration -- $cmd

## This will collect the hotspot of the program
amplxe-cl -c hotspots -knob sampling-mode=hw -- $cmd
```

### How to find the botteneck?

- Is my program I/O bound, memory bound or compute bound?

- What's the SOL?

## Different Optimization experiments

#### Reduce the necessary workload

- Only do the preprocess/inference/post-process on cropped ROI. And then fill the original image back.

#### Batch the workload

The tensorflow inference part is easy to batched, but the other parts of the program is not easy. First, try to refactor code into smaller functions
Change the function sigature of each function to accept `vectors` of the original target data. 
The essential part is always use testing in WIP refactor code. For a code snippets which already known to be correct and with no side effect, keep running both of them and assert same results, after that. replace the WIP refactored ones to be default and delete old ones.

For my target program, turns out batch the job does not enhance the speed at all.
? Why is this?

#### GPU accerlation libs

- OpenCV builtin UMat, which can run functions on OpenCL devices.
Use `UMat` is easy, most python opencv functions accept the `UMat` as well as the numpy ndarray. 
A pitfall is that, not all routines involved are using opencv, many of them are using `numpy` functions direactly, while the numpy daoes not operate on GPU.
Thus you always need a `UMat::get()` to transfer the data from GPU to CPU, which makes the benefits of the GPU parallel computing less appealing.

Findings and conclusion:

- Tranfer data between CPU/GPU with small math/mem ratio is bad.
- OpenCL sucks on Nvidia GPU??? Use Cuda!!
- OpenCV on CPU code is not that bad? They are using mmx/sse/avx for improc? How to find it?

- Cupy lib. Targeted to be the numpy of GPU
TODO: insert `CuPy` link here. And why we are not using it.

- Use nvidia DALI for image proprecess.
TODO: insert the `DALI` link here. And states why we not using it.

- Delegating the preprocess/postprocess to `tensorflow` GPU operators as much as possible.
TODO: states which can be done, which can not be done.

#### Numba JIT

TODO: insert numba link.

Conclusion: numba jit is that easy to use as committed. `nopython` mode does not work for our program in many case. `@numba.jit` a big routine almost always leads to program crash.

#### Cython

TODO: insert cython link as bg.

- Why the cython extension works ? The numpy `universal` function protocal? 

- Numpy native extension protocal directly ??
  The code is ugly and cost much more than cython.

TODO: add one example on how the cython works faster than the just numpy.
Conclusion: cython works for us, since many the numpy `umath` routine can be fused together to enhance the cache locality.
Fusion works on CPU for memory bound functions. I am seeing very good results on using cython.


#### Use Intel Distributed Python

TODO: link. and quick start. Intel python distribute is easy to use in [conda]() environment.

But initial profiling shows not much benefit for our program. 
TODO: why?


#### JPEG decoding.

### Conclusions

* Will a better CPU solves my problem?

* Will a better GPU solves my problem?

## Appendix and Reference


### My HW/SW config

- Intel Core I5-7500 CPU, 4 core, 4 thread, 3.4GHz
- Python 3.
- 2x8GB two channel DDR4 memory.
- Nvidia GTX 1060 6GB GPU.
- Cuda 10.0
- TensorFlow 1.3
- OpenCV 4.1
- Numpy 1.7
- Numba [TODO: version here]
- Cython [TODO: version here]
- Intel Distriuted Python [TODO: version]
- Nvidia Driver [TODO: version] with OpenCL..
- Ubuntu 18.04.02
