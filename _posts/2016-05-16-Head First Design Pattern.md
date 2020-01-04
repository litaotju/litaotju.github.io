---
layout: post
title: Head First Design Pattern - 观察者模式
description: 
category: Design Pattern
tags: 
    - Design Pattern
    - 观察者模式
    - Java
---
{% include JB/setup %}

## 简单介绍什么是观察者模式

观察者模式定义了一种一对多的数据依赖关系，当被观察者的状态发生改变时，会将状态逐个通知观察者。观察者模式就像生活中的订阅报纸的过程。
每当新的一期报纸产生时，所有的订阅者都会收到最新的信息。

## 例子

可被观察的类，Observable 在这里充当了“报纸”或者说是信息源的角色，Observable必须实现能够动态的添加和移除观察者（“订这个报纸的用户”）。
所以将这些观察者放在一个 ArrayList<Observer> observers中，在状态发生改变之后，挨个的调用 observers中的每一个对象的update方法，将信息发布出去。
代码如下：

{% highlight java %}
    import java.util.ArrayList;

    public class Observable{
        private int state;
        private ArrayList<Observer> observers = new ArrayList<Observer>();
        
        public void registerObserver(Observer obser){
            // 将obser添加到 observers;
            observers.add(obser);
        }
        public void removeObserver(Observer obser){
            // 将obser从observers移除;
            int i = observers.indexOf(obser);
            observers.remove(i);
        }
        public void setState(int state){
            this.state = state;
            stateChanged();
        }
        
        public int getState(){
            return this.state;
        }
        public void stateChanged(){
            Observer obj;
            for(int i=0; i < observers.size(); i++){
                obj = observers.get(i);
                obj.update(this.getState());
            }
        }
    }
{% endhighlight %}

Observer定义了一个观察者接口，所有的观察者必须重写 update函数供信息发布者（Observable调用）。代码如下：

{% highlight java %}
    public interface Observer{
        public void update(int state);    
    }
{% endhighlight %}

MyObserver实现了 Observer的，在接收到信息 state 之后，简单的将自己的名字和 接受的信息打印到屏幕。
每一个MyObservser对象，必须首先将自己注册到 Observable的observers中，然后才能在Observable变化时得到通知。
{% highlight java %}
    public class MyObserver implements Observer{
        private String name;
        public MyObserver(Observable obs, String name){
            obs.registerObserver(this);
            this.name = name;
        }
        public void update(int state){
            System.out.println(name+"::"+state);
        }
    }
{% endhighlight %}

ObserverTester类展示了观察者模式的基本用法。
{% highlight java %}
    public class ObserverTester{
        public static void main(String [] args){
            Observable sub = new Observable();
            
            //在初始化观察者时，必须指定所观察的对象
            Observer o1 = new MyObserver(sub, "O1");
            Observer o2 = new MyObserver(sub, "O2");
            
            //设置观察对象的状态，观察都谁收到了信息
            sub.setState(100);
            sub.setState(200);
            
            //动态的添加观察者
            Observer o3 = new MyObserver(sub, "O3");
            
            //设置新的状态, o1,o2,o3将都能接受到新的状态
            sub.setState(300);
            
            //动态的移除观察者
            sub.removeObserver(o2);
            sub.setState(400);
        } 
    }
{% endhighlight %}

## 其他

### 应用

观察者模式在JDK的代码中可以很常见，包括Swing等**GUI框架里面常常用到观察者模式**。只不过在GUI里面习惯将观察者叫做 **listener**。
注意在安卓里面我们也能经常看到 \*Listener的名字，实际上就是某种类型的观察者。

### Java Built-in 观察者模式
在java.util包中自带有 **抽象类Observable** 和 和**Observer**，分别实现了被观察者和观察者的角色。

