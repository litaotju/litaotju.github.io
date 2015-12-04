---
layout: post
title: "Python property 装饰器"
description: ""
category: python
tags: [python]
---
{% include JB/setup %}

## 1. 函数装饰器的基本概念
装饰器实际上就是函数的包装，在一个函数前添加装饰器，在调用被装饰函数的时候，实际上
调用了装饰器定义的包装函数。所以装饰器存在有助于将多个不同函数的共同代码，被最大化
的复用。
下面是一个装饰器的例子：  
        
        def A( func ):
            def __call():
                print "This is a decorator call"
                return func()
            return __call
        @A
        def x():
            print "This is a X func()"
        
        @A
        def y():
            print "This is a Y func()"
            
        x()
        y()
        
上述的例子将输出如下的信息：

    This is a decorator call
    This is a X func()
    This is a decorator call
    This is a Y func()
    
[源代码:decDemo.py](\assets\src\decDemo.py)

装饰器基本原理：在函数x()前加装饰其@A，相当于执行了语句 x = A(x).

## 2.带参数的装饰器

上面的例子显示了x, y不带参数的是的情况，实际上不可能每一个需要装饰器的函数都不带参数.
带参数的例子如下：

       def A(func):
            def __call(*args, **kwds):
                print "This is a decorator call with paras"
                return func(*args, **kwds)
            return __call
       @A
       def x(a, b):
           print "Sum of %d and %d is: %d" %(a, b, a+b)
        
       x(1,2)

上述的例子讲输出如下的信息
    This is a decorator call with paras
    Sum of 1 and 2 is: 3
    
[源代码:decDemopara.py](\assets\src\decDemopara.py)

参考来源
>[廖雪峰的技术博客](http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/0014318435599930270c0381a3b44db991cd6d858064ac0000)

## 3. 类当中特殊的装饰器
在python的新式类中(继承自object的类), 有一个特殊的装饰器，@property, 该装饰器的
基本作用是可以将getter函数当作对象的属性来调用.
一个基本的例子如下：

       class C(object):
       
           def __init__(self):
               self._x = None
           
           @property
           def getx(self):
               return self._x
           
           @x.setter
           def setx(self, val):
               if x <0 or x>100:
                   raise ValueError, "Wrong val for x"
               self._x = val
           
           @x.deleter
           def deletex(self):
               del self._x

上述例子中分别定义了C类的数据属性_x的getter, setter, deleter函数.如果都不加装饰器
那么设置C类实例c 的_x属性的方法分别为：
 
    c.getx()
    c.setx(val)
    c.deletex()

但是有了property装饰器可以大大的简化这一代码：
    
    #获取的c的_x属性
    c.x
    #设置c的_x属性
    c.x = 100
    #删除c的_x属性
    del c.x

参考:  
>[Python276.chm](\assets\python276.chm)  
>[廖雪峰的技术博客](http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/00143186781871161bc8d6497004764b398401a401d4cce000)
    
           