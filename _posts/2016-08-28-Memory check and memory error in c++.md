---
layout: post
title: Memory check and memory error in c++
description: 
category: 
tags: 
---
{% include JB/setup %}

## C++中的内存检测工具valgrind
可以使用 valgrind工具集来进行c++/c程序的内存相关错误检查和程序运行的profile，进而帮助诊断程序中的错误或者程序调优。
### valgrind 中的memcheck工具的用法举例：

1. 假设有一段程序leak.cpp 代码如下

```c++
    #include <cstdlib>

    void leak(){
        int * a = (int *)malloc(100*sizeof(int));
        a[100] = 100;
    }
    int main(){
        leak();
        return 0;
    }
```
很明显看到其中与有一段内存泄漏的代码。使用memcheck进行程序检查的方法如下：

2. 带调试选项编译代码： g++ -g -O0 leak.cpp -o leak
3. 使用valgrind进行内存检查： valgrind --tool=memcheck  ./leak

## Linux下的 segment fault错误
当程序访问到不该访问的内存地址时，会出现段错误，也就是segment fault, 出现这个错误之后，操作系统会把程序出错时程序内存空间中的数据
和相关的信息保存到文件中，称之为core.这个过程称之为core dump。 总结一下就是： **segment fault是出错的原因，core dump是一个过程也是一个现象，core文件一个文件实体**。
### segment错误出现的可能原因
1. 使用了非法的地址，如访问操作系统的拥有的地址，或者访问了 0地址， NULL地址。
2. 用完了堆或者栈空间。
3. 内存访问越界。
4. 指针的错误释放引起的错误。