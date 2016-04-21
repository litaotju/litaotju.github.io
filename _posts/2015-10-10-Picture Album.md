---
layout: post
title: "静态博客中图片的格式"
description: ""
category: lessons
tags: 
   - 图片
---
{% include JB/setup %}
>这是一个关于图片插入位置的博文
---

图片在博客中是一个比较重要的元素，但是Markdown语言本身对于图片的支持不是很完善，比如不能支持图片大小的设置等。
这对于Jekyll搭建github.io是一个弊端。所以要生成高质量的图片方案，必须配合**html**标签进行图片的插入。
例如下图的代码为:  

    <img src="/assets/pic/1.jpg" align="center" alt="图片1" style="max-width:100%;"/>

<img src="/assets/pic/2.jpg" align="center" alt="图片2" style="max-width:100%;"/>

如果使用如下的Markdown原生代码：

    ![图片1](/assets/pic/1.jpg)  
    
那么生成的图像不能根据网页的大小，和设备的分辨率来进行自动的调节位置和大小。如下图所示。

![图片1](/assets/pic/2.jpg)
