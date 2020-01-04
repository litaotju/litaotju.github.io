---
layout: post
title: Why-we-need-D_GLIBCXX_USE_CXX11_ABI=0
description: 
category: C++ 
tags: 
---
{% include JB/setup %}

# Background
When you try to build tensorflow, there is an prompt tell that you need to add "-D_GLIBCXX_USE_CXX11_ABI=0" flag, if you are using GCC 5 or higher, to keep the compatibility of your build tensorflow and official tensorflow build.

>The official TensorFlow packages are built with GCC 4 and use the older ABI. For GCC 5 and later, make your build compatible with the older ABI using: --cxxopt="-D_GLIBCXX_USE_CXX11_ABI=0". ABI compatibility ensures that custom ops built against the official TensorFlow package continue to work with the GCC 5 built package

It's complicated to explain very detailedly and formally on what's the `ABI`. Long story short, on my understanding, it's an agreement/protocal between compilers, on how to find routings/symbols from another compile unit, and how to pass paramters, get return values between routines,  how to functions/symbols names are explained (source files and compiler intermiediate binary files have different names for same functions/classes). 

If all the codes/complenents of your software are compiled from single compilers on your machine, the ABI compatibility is not a concern at all, since the compiler will handle all the dirty details. But if you are writing a library which will be distributed to various users will many potential configs/envs, the ABI should be definately  one of the important thing you need to consider.

Suppose you are writing a libary in c++, and you don't want to distribute out the source code of your library. You can compile it into dynamic libary (.so files in linux), and then give the dynamic library and header files to your users. Users then use the his/her compiler to compile his source files included your header files to object files, then use your dynamic library to link againt his/her objects files to exectubles/libraries. Here the questions comes:
* Suppose you are using GCC compiler with version X,  but user is using another version Y. In this case, Y need to know the binary format of your libary compiled by X.


# About the C++11_ABI flags
The article here explaines it. [https://developers.redhat.com/blog/2015/02/05/gcc5-and-the-c11-abi/](https://developers.redhat.com/blog/2015/02/05/gcc5-and-the-c11-abi/) . 

The basic idea is
>Users that depend on third-party libraries or plugin interfaces that still use the old ABI can build their code with -D_GLIBCXX_USE_CXX11_ABI=0 and everything should work fine. In most cases, it will be obvious when this flag is needed because of errors from the linker complaining about unresolved symbols involving “__cxx11


# Examples
### Step 1. Write and compile the lib
Suppose you are writing a lib with only one cpp file `mylib.cpp`, and export your API by `mylib.h`
```cpp
//mylib.cpp
#include <string>
#include <iostream>
void print_string(const std::string & a)  {
    std::cout <<__FILE__ << __LINE__ << " content of a:"  << a << std::endl;
}
```

```cpp
#ifndef __MYLIB_H
#define __MYLIB_H
#include <string>
void print_string(const std::string & a);
#endif
```

Using the following command to compile the cpp files to dynamic libraries.
```bash
    g++ -fPIC mylib.cpp -dynamic -o libmy.so
```


### Step 2. Write and compile and application
Suppose the cpp files of your application are named by `myapp.cpp`, and it's in same direcotory as `mylib.cpp` and `mylib.h` and `mylib.so` in step 1.
With the following content.
```cpp
#include <string>
#include "mylib.h"
int main(){
    print_string("FromMyApp");
    return 0;
}
```
Using the following command to compile the cpp file to executable.
```bash
g++ myapp.cpp -o myapp -lmy -L./ -I./
```
The command will generate a `myapp` exectuble under current directory and the exetuble works really well, you can just execute it.


### Step 3. Change the ABI of the libary will affect the application
But what if I channged the libary compiling command to following command
```bash
g++ -fPIC mylib.cpp -shared -o libmy.so -D_GLIBCXX_USE_CXX11_ABI=0
```
After this, if I execute the same command as in step.2 to compile the app `g++ myapp.cpp -lmy -L./ -o myapp`.
The compiler give the following errrors

```bash
/tmp/ccDPFccW.o: In function `main':
myapp.cpp:(.text+0x43): undefined reference to `print_string(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)'
collect2: error: ld returned 1 exit status
```

That's a obvious indication that I need to use same compile flags as the libary compileing command.
```bash
g++ myapp.cpp -lmy -L./ -o myapp -D_GLIBCXX_USE_CXX11_ABI=0 
```

### 4. Back to the tensorflow example.

Now let's go back to the tensorflow example, since the official pre-built tensorflow library (.so) are compiled by older GCC, (which equals to newer version of GCC wht flag -DGLIBCXX_USE_CXX11_ABI=0).  So if an existing uplevel application/library using the official tensorflow are expecting to compiled by NO CXX 11 ABI, if you are expecting the application/library also works with your compiled tensorflow so, you either need to compile it with older compiler or use the new compiler with flag `-DGLIBCXX_USE_CXX11_ABI=0`.


# Reference materials
* [ABI wikipedia](https://en.wikipedia.org/wiki/Application_binary_interface)
* [Name mangling](https://en.wikipedia.org/wiki/Name_mangling)
* [Name mangling from IBMi website](https://www.ibm.com/support/knowledgecenter/en/ssw_ibm_i_72/rzarg/name_mangling.htm)
* [gcc5-and-the-c11-abi](https://developers.redhat.com/blog/2015/02/05/gcc5-and-the-c11-abi/) 