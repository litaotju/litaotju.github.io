---
layout: post
title: Modern C++ -- Variadic Templates
description: 
category: 
tags: 
---
{% include JB/setup %}

Synopsys 培训时，候捷老师讲解了 "可变参数模版"这一个课题。
本文记录了两个例子来说明可变参数模版的用法。

# 可变参数模版函数

```cpp
//这个不接受任何参数的函数是必须的，
//因为下面接受人任意个参数的函数的递归调用最终都会调用到此函数
//如果不定义，直接编译无法通过
void print() {
}

// T 为一个， ...Types 为一包
// 每次处理第一个，然后递归的调用更小的一包
template <typename T , typename...Types>
void print(T & first, Types& ... args) {
    cout<<first << endl;
    print(args...);
}

//下面为上述模版函数的用法
//可以给任意个参数，但是要注意，模版实际上生成了不同的函数
//并不是一个函数接受任意多个参数。这实际上会增加代码的体积，
//具体生成多少个函数，取决于，调用时给了最多参数的函数。
int a = 10;
float b = 20.0;
print(a,b);

string c = "abcd";
print(a,b,c);

double x = 23.0;
print(a,b,c,x);

```

# 可变参数模版类

```cpp
// This is must needed. If no this,  the specialization following will not compile
// Since the compiler don't recognize MyClass as a teplate class
template <typename ... Types> class MyClass;

// The specialization does nothing。Simply for all the classes to inheriate from this class
template <> class MyClass<> {};

// 与函数相同，分为一个参数T和一包参数...Types
// 继承自一小包为 参数的模版父类.该父类又继续递归继承自含有更少模版参数的父类
// 直到可变参数的个数为0, 也就是 template <> class MyClass<> {}; 所定义的最特化的类
template <typename T, typename...Types>
class MyClass<T, Types...> : 
  private MyClass<Types...>
{
public:
    typedef MyClass<Types...> inheriated ;
    MyClass(T  first, Types  ...args) :
        firstData(first), inheriated(args...) {}
    T  head() {return firstData;};
    inheriated & tail() {
        return *this;
    }
private:
    T firstData;
};

//应用
// 注意可变模版参数的模版类必须在实例化时，使用 <>指定模版的实参
// 而上个例子中的模版函数则不需要直接指定模版实参.
void test() {
    int a = 10;
    float b = 20.0;
    string c = "abcd";
    double x = 23.0;

    //以下的代码将生成完全不同的两组类.
    // MyClass<int, string>  
    //    -> MyClass<string> -> MyClass<>
    MyClass<int, string> obj1(a,c);

    // MyClass<int, float, string, double> 
    //      -> MyClass<float, string, double>
    //       ->  MyClass<string, double> 
    //         ->  MyClass<double>  -> MyClass<>
    MyClass<int, float, string, double> obj(a,b,c,x);

    cout << obj.head() <<endl;
    cout << obj.tail().head() << endl;
    cout << obj.tail().tail().head() << endl;
    cout << obj.tail().tail().tail().head() << endl;
    return 0;
}
```

