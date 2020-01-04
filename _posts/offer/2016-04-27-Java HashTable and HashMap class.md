---
layout: post
title: HashMap 和HashTable的区别
description: 
category: Software
tags: java
---
{% include JB/setup %}

1. HashTable是线程安全的， HashMap不是。
2. HashMap允许键和值为null, 但是HashTable不允许。
3. HashMap是轻量级的HashTable，两者都实现了Map接口，完成键值对映射，但是HashMap的效率高于HashTable。

>参考链接: [HashMap和HashTable的区别](http://www.cnblogs.com/langtianya/archive/2013/03/19/2970273.html)
    