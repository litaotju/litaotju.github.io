---
layout: post
title: Linking static library and --whole-archive option
description: 
category: C++
tags: "static link"
---
{% include JB/setup %}

# Conflict between linker's default behavior and programmer's intention

By default the linker will omit one object file inside an static lib archive if every symbols inside that object are not used by the target binary directly or indirectly.

This is good and saves the generated code size and remove "dead code" in the target binary, but this default behavior has caused un-intended effects when combined with two things:
    - Static lib
    - Global object auto initialization has side effect which needs by the lib itself to run correctly. But that global object is not exported to client applications.

There is pattern that use global object intialization for self registered resource.

In that cases, we could solve this by two methods:

1. Declare the object to function local static variable, and export that function/functions. Then the client application calls the function.

2. Use the "--whole-archive" option of the linker when linking  with static lib, such that the object will not be omitted.

Note: the linker omits some object files of the .a archive, not based on the global object and reserve functions in same object file.


# Code Example

```cpp
// a.h
int f();

class A
{
    public:
    A();
};

class B
{
    public:
    B();
};

```

```cpp
//b.cpp
#include "a.h"
#include <iostream>
B b;
B::B()
{
    std::cout << "B::B" << std::endl;
}
```

```cpp
// a.cpp
#include <iostream>
#include "a.h"
int f()
{
    return 0;
}
A::A()
{
    std::cout << "A::A" << std::endl;
}
A a;

```

```cpp
//main.cpp
#include "a.h"

int main()
{
    return f();
}
```

After we comple the a.cpp and b.cpp and archive it into a libX.a,
when linking  "main.cpp" with libX.a
``` bash
$ g++ main.o libX.a -o main
$ g++ main.o -Wl,--whole-archive libX.a -Wl,--no-whole-archive -o main-whole-archive
$ g++ main.o libX.so -o main-dynamic
```

Running the generated executable, we can find:

- "./main" we can find only "A::A" is called, and "B::B" is not called, this means the object file b.o containing global object 'b' is not compiled into the lib.

  To verify it's the object file not contained, not just the global variable. You could add some functions inside the b.cpp, and see if that function can be find inside the target binary's symbols.

  To verify if any one symbols defined in a object file is used by main directly or indirectly, then all the symbols (codes) inside the object will be linked into target.

- "./main-whole-archive" and "./main-dynamic", we find both "A::A" and "B::B" are called.

    Means dynamic lib will not omit some global variable, and whole archive option can save it.


References:
- [1] [https://www.bfilipek.com/2018/02/static-vars-static-lib.html](https://www.bfilipek.com/2018/02/static-vars-static-lib.html)

- [2] [https://stackoverflow.com/questions/1229430/how-do-i-prevent-my-unused-global-variables-being-compiled-out](https://stackoverflow.com/questions/1229430/how-do-i-prevent-my-unused-global-variables-being-compiled-out)