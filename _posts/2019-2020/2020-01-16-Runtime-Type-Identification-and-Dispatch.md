---
layout: post
title: Type packing and unpacking. Or upcast and downcast.
description: 
category: 
tags: 
---
{% include JB/setup %}

Is this post. `upcast` means convert a type to a more general type. `downcast` means convering a type from a general type to more concrete type.
The motivation for `upcast` is shareing interfaces/procedures/algorithms between a group of types which are similar in some aspects.
The mostivation to `downcast` is to use the unique aspects of the different types to acommplish the software business logic.

# 1 `void *` based method.

In C++/C, the `void *` can be covered from and to any type. So the `void *` can be used as a intermediate type.
But the `void *` lost any type info of the downstream type infomation. And maybe dangerous to use, when using the `void *`, developer lost the compability and help of the compiler tool chain. It relies haviyly on the `protocol` of developers, and there is no `forced` way. This protocal can be code document, or just implicit sharing knowledge between a group of developers.

## Why use the `void *` at the first place.

- Hide the internal detail of a struct from users, while the lib/api provider knows exactly what this object is.
  Normally the object itself is created by an API provided by the lib, and manipulated by a group of API provided in the lib. 
  To enhance the readbility, normally this kind of `void *` will be aliased into a meaningful name, like `xxxHandle`. This alias does not provide any type safety to the compiler, it's just helps the human. If you want to shoot yourself on the foot, just pass any random created by yourself to the API accept the `void *`, compile will pass silently, while the runtime error is unknown.

- Really simple and easy to understand, no tricks.

- It's c legacy. Use `std::any` if you can use the c++17.


# 2 `union`

The `void *` can be converted from/to `any` type, which offen makes people or tool chain's confusion, this confusion is root caused by the complete lost of the source/target type. `union` limits the allowed type from `any` to a `finite set`. and the compiler use the maxim memory size of the type included in this set. When the `union` type is used, it's always referenced by one of the concrete type included in the set.

However, when the cycle happens.
    concrete type =>  `upcast` -> union -> `downcast` -> concrete type.

There is no gurantee that the first upcast and second downcast share the same concrete type. Take the following code as example.
In the caller `main` function, the union is actual an int, while the callee actually make the assumption that the union A is `float`.

```cpp
#include <iostream>
union A
{
    int iA;
    float fB;
};

void printUnion(A a)
{
    std::cout << a.fB << std::endl;
}

int main()
{
    A a;
    a.iA = 100;
    printUnion(a);

    A a1;
    a.fB = 100;
    printUnion(a1);
}
```

To make the `type` info more complete. We can further add an `enum` representing every one of the allowed type in the `union`.
In the following example, `TypedA` contains the union as container of actual data , while keep another field `type` as the type information.

```cpp
#include <iostream>
#include <cassert>

union A
{
    int iA;
    float fB;
};

enum Type
{
    kINT = 0,
    kFLOAT = 1
};

struct TypedA
{
    A data;
    Type type;
};


void printTypedA(TypedA a)
{
    if (a.type == kINT)
    {
        //downcast happens here.
        std::cout << a.data.iA << std::endl;
    }
    else
    {
        assert(a.type == kFLOAT);
        std::cout << a.data.fB << std::endl;
    }
}

int main()
{
    TypedA a;
    a.data.iA = 100;
    a.type = kINT;

    //upcast happens here.
    printTypedA(a);

    TypedA a1;
    a1.data.fB = 123.1234f;
    a1.type = kFLOAT;
    printTypedA(a1);
}
```

## Why use `union` in the first place?

# 3. class public inheritance

This is provided by the c++ languange. `upcast`: subclass can be safety convered into parent class automatically. 
While the `downcast` can be down by `dynamic_cast` or `static_cast`.

Note: `static_cast` can be dangerous then `dynamic_cast`, because it may fail silently. While `dynamic_cast` can be used to downcast safely.

```cpp
#include <iostream>
#include <exception>

class Parent
{
public:
    virtual ~Parent() {};
};

class Child1 : public Parent
{
};

class Child2 : public Parent
{
};


void AlgA(Parent& A)
{
    std::cout << &A << std::endl;
    auto c1 = static_cast<const Child1&>(A);
    auto c2 = static_cast<const Child2&>(A);
};

void ReqC1(Parent& A)
{
    std::cout << &A << std::endl;
    auto c1 = dynamic_cast<const Child1&>(A);
};

void ReqC2(Parent& A)
{
    std::cout << &A << std::endl;
    auto c2 = dynamic_cast<const Child2&>(A);
};

int main()
{
    Child1 c1;
    AlgA(c1);

    Child2 c2;
    AlgA(c2);

    //no exceptions will be throwed here. 
    ReqC1(c1);
    ReqC2(c2);

    //dynamic cast throw
    try
    {
        ReqC2(c1);
    }
    catch(const std::bad_cast &e)
    {
        std::cout << e.what() << std::endl;
    }

    try
    {
        ReqC1(c2);
    }
    catch(const std::bad_cast &e)
    {
        std::cout << e.what() << std::endl;
    }
}
```

# 4. Template.
    Seprate code will  be generated for each instance of the template.

Quiz:
    - Can the template member function be `virtual`? Why or why not? If it can be, when to use it?

    - For a template member function,  does this means the view of the class (at least the number of member functions, and their signature) are different when different translation units which instanced this member function with different types?

    - When template are instanced/expanded?
      - There is not doubt, it's not preprecess, not link time. It's compile time. And to be more perticular, its the language frontend doing it.

# 5. Virtual table.
   Run-time type identification.