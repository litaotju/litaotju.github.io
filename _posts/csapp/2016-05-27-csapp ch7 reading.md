---
layout: post
title: 深入理解计算机系统-读书笔记(第七章)-链接
description: 
category: ComputerArch
tags: 
    - 链接
---
{% include JB/setup %}

## 什么是链接

**链接是将各种代码和数据部分收集起来变成一个单一的文件的过程**，这个文件可被加载到存储器并且执行。 
链接可以存在于*编译时*，可以存在于*加载时*，甚至也可以存在于*运行时*。在现代的操作系统中，链接由连接器执行。
编译时的链接静态链接，加载时和运行的链接称为动态链接。 静态链接将被链接的部分直接合成到一个文件中，因此如果多个程序调用了同一个库，
那么他们编译成的程序中每一个都直接存在这个库中它所调用的对象文件的所有代码和数据拷贝。动态链接最终文件中不直接保存所链接的对象文件，
而是包含对应的链接文件的位置信息和文件名等，在可执行文件被操作系统加载时直接加载被动态链接的文件，或者由应用程序在运行时直接显式的调用动态链接文件。

## 编译器驱动
编译器驱动是指一组编译器工具集，包含有 语言预处理器，编译器，汇编器和链接器。比如GNU编译系统（一般说的GCC）的每一个工具分别如下：

* C语言预处理器， cpp
* C语言编译器，ccl
* 汇编器， as
* 连接器， ld

## 静态链接

静态链接的示意图如下：
![静态链接](/img/in-post/static-ld.png)

链接器 ld 接受一组可重定位的目标文件和命令行参数，产生一个完全链接的可加载可运行的可执行文件。输入的可重定位文件由不同的段组成。
这些段基本可以分为数据段和程序段.text，其中数据段又分为 .data段和 .bss段。 .data段存储已经初始化的全局变量，.bss段存储未初始化的全局变量。
为了构造可执行程序文件，链接器的两个主要任务是：符号解析和重定位。

简而言之，符号解析就是确定每一个目标文件中未确定其真实定义的各种符号的真实位置。 比如 a.o中包含有一些全局变量和或者函数未在a.o中定义，而在b.o中定义，
符号解析就是确定a.o中未确定的符号到底是在哪一个目标文件中的哪一个已经定义的符号。

将不同目标文件中的相同名称的段合并之后，全局变量或者函数的真实地址已经发生改变，**重定位**的作用就是修改每一个符号引用的地址为新目标文件中的地址。

## 什么是目标文件
目标文件有三种形式：
* 可执行目标文件，包含代码和数据可以直接加载到存储器中并运行。一般是链接器的输出。（可执行程序）
* 可重定位目标文件， 包含二进制代码和数据，可以在编译时与其他可重定位目标文件合并起来，生成一个可执行目标文件。（静态库中的目标文件，linux下的.o文件，windows下的 .obj）
* 共享目标文件， 一种特殊的可重定位目标文件，可以在加载或者运行时被加载到存储器并链接。（动态链接库中的目标文件，linux的动态链接库为.so，windows下的动态链接库为.dll）

目标文件的基本组织形式是 "段"。不同的段中包含有不同含义和不同作用的二进制数据。

Linux ELF可重定位的目标文件的段的示意图如下：
![可重定位目标文件的段](/img/in-post/linkable-realoc.png)


Linux ELF可执行目标文件的段示意图如下：
![可执行的目标文件的段](/img/in-post/execable-realoc.png)


## 可执行目标文件的加载和运行时存储器映像
操作系统中由**加载器**负责将可执行目标文件加载到存储器空间中，并将控制权转移给应用程序。
也就是说加载器将**文件**变成了运行中的**活的程序**。 每一个程序有静态形式（文件系统中的存在形式）和运行时的形式。
典型的Linux系统中程序的运行时存储器映像如下：
![可执行文件的存储器影响](/img/in-post/elf-runtime.png)


## 从应用程序中加载和链接共享库（待续）
前面介绍了静态链接的概念，静态链接使得应用程序可以方便的使用大量的库函数。但是静态库的两个问题是：  
1 库函数所提供的代码和数据已经被链接到程序中去，如果要更新或者修复bug，调用相应库函数的应用程序必须进行显式的重新编译链接，很不方便。
2 如果多个程序共享一个库函数，比如几乎每一个C程序都会使用的printf和scanf，那么这些函数的代码需要被每一个程序拷贝一份，造成了存储器的浪费和低效。

共享库是为了解决上述的两个问题而产生的，共享库是一个目标模块，可以在**运行时加载到存储器当中的任意地址**，并**和一个在存储器中的应用程序链接起来**。
这个过程就叫做动态链接，是由一个叫做动态连接器的程序来完成的。
共享库也叫做共享目标（shared object）,因此在unix系统中用 .so后缀的文件存储，windows中大量的运用到了共享库，但是windows中叫做动态链接库（.dll后缀）。

### 动态链接库的生成
在gcc中可以使用 -fPIC和 -shared选项从源文件生成 动态链接库。
比如

    gcc -shared -fPIC -o dynamic.so a.c b.c
    
上面的指令将源文件a.c和b.c编译并生成可动态链接的共享库 dynamic.so

### 动态链接库的使用

#### 1.加载时动态链接方法 
指令示例：gcc -o p source.c ./dynamic.so

解释：在生成的程序p中保存一部分关于动态链接库dynamic.so的信息，在加载器加载p到内存中时，也同时加载dynamic.so的代码和数据到内存中。

加载时动态链接的示意图如下：
![动态链接](/img/in-post/dynamic-link-loadtime.png)

#### 2.运行时动态链接
运行时动态链接是指，在应用程序中显式的的读取动态链接文件，然后从该文件中析取出特定符号（变量或者函数）;

linux系统为动态连接器提供了接口，允许程序动态的加载和链接共享库，头文件和函数原型如下：


        #include "dlfcn.h"
        void * dlopen(int char *filename, int flag);
        //若成功则返回指向句柄的指针，若失败则返回NULL
        
        void * dlsym(void *handle, char *symbol);
        //handle是前面使用dlopen返回的共享库的句柄， symbol为想要加载的符号
        //若成功则返回指向符号的指针，若失败则返回NULL
        
        void dlclose(void *handle);
        //如果没有其他程序使用这个共享库，就卸载这个库
        
        const char * dlerror(void);
        //若前面的调用失败，则为错误消息，否则为NULL


### 运行时加载共享库-Example

一个使用动态链接的最简单c语言代码如下，本例子包含dynamic.c和main.c两个源文件，分别产生动态链接文件和可执行程序文件。
它们的代码和编译指令分别如下：


        // dynamic.c
        //int G = 0;
        int add(int a, int b){
            static int G = 0;
            G++;
            return G+a+b;
        }


编译指令： gcc dynamic.c -fPIC -shared -o dynamic.so
    

        // main.c
        #include "stdlib.h"
        #include "stdio.h"
        #include "dlfcn.h"

        int main(){
            int a, c;
            scanf("%d %d", &a, &c);
            //dynamic.so is pwd
            void *dynamic  = dlopen("dynamic.so", RTLD_LAZY);
            if(dynamic == NULL){
            printf("%s", dlerror());
            return -1;
            }
            int (* add)(int, int);

            //there is a funtion in dynamic.so
            //int add(int a, int c);
            add = dlsym(dynamic, "add");
            if(add == NULL){
                printf("%s", dlerror());
                exit(-1);
            }
            //call add func by dynamic linked symbol
            printf("%d", add(a,c));
            
            //close handle
            if(dlclose(dynamic) <0){
                printf("%s", dlerror());
                exit(-1);
            }
            return 0;
        }

编译选项：
    gcc -rdynamic main.c -o p -ldl

### Windows下动态链接库的使用

    #include <iostream>
    #include "windows.h"

    using namespace std;

    typedef int(* ADD)(int, int);

    int main(int argc, char *argv[]){

        HMODULE dll;
        LPCSTR dllname = "Dll1.Windows.dll";
        //加载动态库
        dll = LoadLibrary(dllname);
        if (dll == NULL){
            cerr << "Can not load " << dllname << endl;
            system("PAUSE");
            exit(-1);
        }
        //从已经加载的库中提取函数
        ADD add = (ADD)GetProcAddress(dll, "add");
        if (add == NULL){
            cerr << "Cannot find add function in " << dllname << endl;
            system("PAUSE");
            exit(-1);
        }
        //释放动态库
        FreeLibrary(dll);
        cout << "1 + 2 = " << add(1, 2) << endl;
        return 0;
    }
    
### 相关链接
>详情请参见 《深入理解计算机系统第七章》  
>[从C++到可执行文件](/c++/2015/10/12/From-Cpp-to-.exe/)




    