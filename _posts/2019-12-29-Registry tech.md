---
layout: post
title: Registry tech
description: 
category: 
tags: 
---
{% include JB/setup %}

## Key Points of the registry

- A template class with singleton pattern `Registry<T>` to perform registry for a type `T`.
  In our example `T==Op`.

- A macro `REGISTER_OP` to instance a global variable of type `Op`, the instance is created by a factory method `Registry<Op>::createObj`, such that the singleton can track all the `Op` objs.
  In reality, the factory method may not be in a seprate class, it can just be a static method of `T`. But put it under different 
  class matches the `single responsibility role`.

- The setters `Op` class returns `Op &`, such that the chain of setters can be used.

   ``` cpp
    class Op {
        ...
        Op& set_num_inputs(int32_t n) {num_inputs = n; return *this;}
    };

    REGISTER_OP(sub_op, sub)
        .set_num_inputs(2)
        .describe("Do substraction on inputs")
    ```

- The order of obj construction/main/desctuction are following:
-
    + Registry is constructed (global var).
    + Op A,B,C... is construted(in heap, by factory method of Registry).
    + `main` func called.
    + `main` returned.
    + Registry is destructed (automatically scheduled by compiler.), inside registry destructor, destory 
        all the Op A, B, C it cretaed.

```text
Registry<T>::Registry() called
Op::Op() called
Op::Op() called
main is called
Op: add, 0x7f9a66c02a80, desc: Do elementwise add, num_inputs: 0
Op: sub, 0x7f9a66c02ad0, desc: Do substraction on inputs, num_inputs: 2
main is returned
Registry<T>::~Registry() called
Op::~Op() called
Op::~Op() called
```
## Code

Following is the content of `registry.h`.
```
#include <string>
#include <vector>
#include <iostream>
using std::string;
using std::cout;
using std::endl;

class Op;

template <typename T>
class Registry
{
public:
   static Registry<T> &get()
   {
       static Registry<T> inst;
       return inst;
   }

   T& createObj(const string& name)
   {
       T * t = new T;
       t->name = name;
       mObjs.push_back(t);
       return *t;
   }

   void print()
   {
       for(auto k: mObjs)
       {
           std::cout << "Op: " << k->name << ", " << k << ", "
           << "desc: " << k->desc  << ", " 
           << "num_inputs: " << k->num_inputs << std::endl;
       } 
   }

   ~Registry()
   {
        std::cout << "Registry<T>::~Registry() called" << std::endl;
       for(auto k: mObjs)
       {
          if(k != nullptr)
          {
               delete k;
          } 
       }
   }
private:
   Registry()
   {
       std::cout << "Registry<T>::Registry() called" << std::endl;
   }
   std::vector<T*> mObjs;    
};

class Op
{
public:
    Op()
    {
        std::cout << "Op::Op() called" << std::endl;
    }
    ~Op()
    {
        std::cout << "Op::~Op() called" << std::endl;
    }
    Op& set_num_inputs(int32_t n) {num_inputs = n; return *this;}
    Op& describe(std::string desc) {this->desc=desc; return *this;}
private:
    template <typename T> friend class Registry;
    string name;
    int32_t num_inputs;
    string desc;
};

#define REGISTER_OP(objname, name) \
     Op& objname = Registry<Op>::get().createObj(#name)

#define PRINT_ALL_OPS \
    Registry<Op>::get().print();

```

Following is `main.cpp`, which demonstrate the usage of the registry.

```cpp
#include "registry.h"
#include <iostream>

REGISTER_OP(add_op, add)
    .describe("Do elementwise add");

REGISTER_OP(sub_op, sub)
    .describe("Do substraction on inputs")
    .set_num_inputs(2);

int main()
{
    std::cout << "main is called" << std::endl;
    PRINT_ALL_OPS;
    std::cout << "main is returned" << std::endl;
    return 0;
}
```