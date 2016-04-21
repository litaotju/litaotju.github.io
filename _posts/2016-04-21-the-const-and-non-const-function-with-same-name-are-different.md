---
layout: post
title: "The const and non const function with same name are different"
description: ""
category: C++
tags: []
---
{% include JB/setup %}

# 从一个考题说起

一个考试题如下：

```cpp
    #include <iostream>
    using namespace std;

    class A{
        public:
        virtual void f(){
            cout<<"A::f()"<<endl;
        }
        void f() const{
            cout<<"A::f()const"<<endl;
        }
    };
    
    class B: public A{
    public:
        void f(){
            cout<<"B::f()"<<endl;
        }
        void f() const{
            cout<<"B::f()const"<<endl;
        }
    };

    void g(const A * a){
        a->f();
    }

    int main(int argc, char * argv[]){
        
        A const *a = new A();
        a->f();
        A  *aa = new A();
        aa->f();
        //以上输出
        //A::f()const
        //A::f()
        //说明 1.加const和不加const的函数是不一样的。
        //     2. const指针，调用了对应的加const修饰的函数
        
        g(a);
        g(aa);
        //以上输出
        // A::f() const
        // A::f() const
        //说明：传递给函数的指针在函数内部已经const化了
        
        
        A *ab = new B();
        ab->f();
        g(ab);
        //以上输出
        //B::f()
        //A::f()const
        //因为: virtual void f()函数可以多态因为前面加了 virtual关键字，void f() const函数没有多态
            
        
        A const *const_ab = new B();
        const_ab->f();
        g(const_ab);

        //以上输出
        //A::f() const
        //A::f() const
        //因为 void f() const没有多态， 直接调用父类型
    } 
```

从以上的代码运行结果可以得出结论：

* 在函数名称，参数，返回值 相同的情况下，加了const和不加const修饰符的函数，不是同一个函数。（编译器把他们当作两个函数看待）
* 在其他条件相同的情况下，const对象或const指针调用 加const修饰符的函数。
    非const对象调用非const修饰符的函数
* const修饰形参时， 非const的实参在函数会被转换为const（这一转换为函数内有效）