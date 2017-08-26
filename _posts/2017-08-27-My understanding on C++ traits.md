---
layout: post
title: My understanding on C++ traits
description:  
category: 
tags: 
---
{% include JB/setup %}

## Talk is cheap, please see the code.

```cpp
#include <iostream>
#include <string>

template <typename T>
class ClockTraits {
public:
    typedef std::string nameType;
    typedef float periodType;
    nameType getName() const = 0;
    periodType getPeriod() const = 0;
};


class AClock {
public:
    AClock(const char * name, int prd) :
        name(name), prd(prd){
        }
    const char * getName() const {
        return name;
    }
    int getPrd() const {
        return prd;
    }
private:
    const char * name;
    int prd;
};

class Bclock {
public:
    Bclock(const std::string & name, float prd) :
        _name(name), _prd(prd){
    }
    std::string getClockName() const {
        return _name;
    }
    float getPeriod() const {
        return  _prd;
    }

private:
    std::string _name;
    float _prd;
};


template <>
class ClockTraits<AClock> {
public:
    typedef const char * nameType;
    typedef int periodType;
    ClockTraits(const AClock & a) : _clock(a) {}
    nameType getName() {return _clock.getName();}
    periodType getPeriod() { return _clock.getPrd();}
private:
   const AClock & _clock;
};

template <>
class ClockTraits<Bclock> {
public:
    typedef std::string nameType;
    typedef float periodType;
    ClockTraits(const Bclock & b) : _clock(b) {}
    nameType getName() {return _clock.getClockName();}
    periodType getPeriod() { return _clock.getPeriod();}

private:
    const Bclock & _clock;
};

// 为什么需要traits? 代码重用。
//    假如这里的printClock是一种非常复杂的流程和算法，但是我们又不希望
//    printClock 只能应用于某一种类型的clock上面。那么在不依赖于任何clock类型的
//    情况下，怎么写代码？
//
//    1. 直接调用clock对象的成员函数。那么对clock类的要求都寄托在这些成员函数上。
//       如果一个类没有实现这样的成员函数，就不能应用printClock
//
//      template <typename C>
//      void printClock(const C &clock) {
//        std::cout << "Name: " << clock.getName() <<std::endl;
//        std::cout << "Period: " << clock.getPeriod() << std::endl;
//      }
//
//    2. 寄希望于ClockTraits这个类，只要typename C特化了 ClockTraits模版类
//       便能用应用printClock
//
//    1 于 2 的区别在于什么：
//      （1) 1 中printClock直接依赖于clock的类型C，要求C类型具备某些相同的接口。
//            对于代码库中已经拥有的现成的类型， 假设为A B C D，如果A B C D
//            都想应用printClock函数, 要求A B C D都必须有 返回值可以直接<< 的
//            getName（） getPeriod（）函数，
//            如果其中一个不满足，就无法应用于printClock算法。为了使用必须对
//            A B C D类进行修改。这不满足开闭原则。
//
//            **同样的功能可以用运行期多态实现。即 printClock的原型变为：
//                void printClock( const ClockInterface & clock)
//              每一个应用于printClock的类型都必须时ClockInterface（子）类。**
//
//           2 中printClock 依赖于 模版类 ClockTraits<C>
//              如果A B C D 接口不同，那么给任何一个类定义模版类的特化就好了。
//              不需要修改A B C D类型本身。 只拓展，没修改。
//              如果有新的类型加入， 给新的类型定义一个 ClockTraits 特化，照样可以使用
//              printClock模版类，达到代码的重用。
//
//     1 与 2 各自的优缺点
//         1 可能少写了一些 Traits类的特化的代码，但是1 对应用与其中的类直接做了限制。
//           在不修改已有代码的前提下，无法将模版函数直接应用于多个不同的类。
//            **因此 在没有很多欠账和历史包袱的情况下，用1更写的似乎更快。**
//
//         2 代码量稍多。但是相当于在 模版类型参数C 与 算法之间多了一层隔离，即ClockTraits。
//           也明确的告诉printClock 的潜在用户： 如果你想用我这个模版函数，你的C类型
//           必须满足 ClockTraits 的条件嗷。 
//           ** 在系统中已经有很多各式各样的Clock 类，且不属于同一个继承体系的话。
//              用2实现可以不破坏已有代码。 **

template <typename C>
void printClock(const C &clock) {
    typedef typename ClockTraits<C>::nameType nameType;
    typedef typename ClockTraits<C>::periodType periodType;
    nameType name = ClockTraits<C>(clock).getName() ;
    periodType period = ClockTraits<C>(clock).getPeriod();
    std::cout << "Name: " << name <<std::endl;
    std::cout << "Period: " << period << std::endl;
}

// When I finishes the printClock function and all the above classes
// Someday, I need to add a new clockType to this system, so I can use printClock
// I only need to do is:
//  class NewClockType{
//      ....
//  };
// template <>
// class ClockTraits<NewClockType> {
//    typedef typename someType nameType;
//    typedef typename someOtherType periodType;
//    nameType getName() {...} 
//    periodType getPeriod() {...}
// };
//
//  As long as I define a ClockTraits template specilizaiton for my new class
//  I can use the existing **printClock** template functiona and 
//
//  总的来说，就是，让模版类（函数）(在这里指printClock)依赖于模版(在这里指
//  ClockTraits) 而不是具体类的接口。
//  换一个思路讲， 每一个能调用printClock的类，都在不需要继承的情况下(只需要模版特化）
//  满足了ClockTrats的接口（编译期多态）。

int main() {
    AClock a("clk1", 10);
    Bclock b("clk2", 100);
    printClock<AClock>(a);
    printClock<Bclock>(b);
    return 0;
}
```
