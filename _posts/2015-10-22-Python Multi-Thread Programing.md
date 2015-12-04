---
layout: post
title: "Python多线程编程"
description: 
category:  python
tags: 
---
{% include JB/setup %}
## 简要介绍
多线程类似于同时执行多个不同程序，多线程运行有如下优点：  

* 使用线程可以把占据长时间的程序中的任务放到后台去处理。
* 用户界面可以更加吸引人，这样比如用户点击了一个按钮去触发某些事件的处理，可以弹出一个进度条来显示处理的进度
* 程序的运行速度可能加快
* 在一些等待的任务实现上如用户输入、文件读写和网络收发数据等，线程就比较有用了。在这种情况下我们可以释放一些珍贵的资源如内存占用等等。

线程在执行过程中与进程还是有区别的。每个独立的线程有一个程序运行的入口、顺序执行序列和程序的出口。但是线程不能够独立执行，必须依存在应用程序中，由应用程序提供多个线程执行控制。

每个线程都有他自己的一组CPU寄存器，称为线程的上下文，该上下文反映了线程上次运行该线程的CPU寄存器的状态。
指令指针和堆栈指针寄存器是线程上下文中两个最重要的寄存器，线程总是在进程得到上下文中运行的，这些地址都用于标志拥有线程的进程地址空间中的内存。
线程可以被抢占（中断）。

在其他线程正在运行时，线程可以暂时搁置（也称为睡眠） -- 这就是线程的退让。  

## 与Python多线程编程有关的模块
下面列出了与Python多线程编程有关的模块。  

* thread， 基本的低级别的线程模块
* threading, 高级别的线程和同步对象
* Queue， 供多线程使用的同步先入先出（FIFO）队列
* mutex， 互斥对象
* SocketServer , 具有线程控制的TCP和UDP管理器

## 一个简单的例子
下面的例子例化了两个 Thread对象，并且将loop函数作为target参数传递给Thread的构造函数
，同时将loop运行所需要的参数打包成一个tuple传递给args.也就是下面的语句：

    t = threading.Thread(target = loop, args = (i, loops[i]))
    
完整的代码如下。

<pre><code>

    import threading
    from time import sleep, ctime
    
    def loop(nloop, nsec):
        print "Start Loop", nloop, 'at:', ctime()
        sleep(nsec)
        print "Loop ", nloop, 'done at:', ctime()
            
    class MyThread:
        
        def __init__(self):
            pass
            
    def main():
        loops = [4, 2]
        print 'Start at time:', ctime
        threads = []
        nloops = range(len(loops))
        
        for i in nloops:
            t = threading.Thread( target = loop, args = (i, loops[i]))
            threads.append(t)
    
        for i in nloops:
            threads[i].start()
        
        for i in nloops:
            threads[i].join()
        
        print "all Done at", ctime()
        
    if __name__  == "__main__":
        main()

</code></pre>

##可调用的类
重载了特殊方法 __call__的类，该类的对象可以作为Thread初始化时所对应的target实参。

##参考网址  
[菜鸟教程](http://www.runoob.com/python/python-multithreading.html)