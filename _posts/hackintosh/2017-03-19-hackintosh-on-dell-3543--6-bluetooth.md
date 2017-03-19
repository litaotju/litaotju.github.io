---
layout: post
title: "Hackintosh on Dell 3543 - 6. Using Bluetooth after disable Discrete GPU
description: ""
category: 
tags: [Hackintosh]
---
{% include JB/setup %}

## Bluetooth问题

1. 在本系列的第4篇中，按照教程禁用了英伟达独立显卡之后，偶然发现蓝牙居然可用。于是果断的配上了小米蓝牙小钢炮音箱。
   可以通过蓝牙来进行外放了。
   - 手机蓝牙和电脑配对之后，如果要通过手机向电脑传输文件的话，应该打开电脑中的： 系统设置-》共享-》蓝牙共享。

2. 存在的问题
    - 长时间睡眠之后，无法再次连接蓝牙。暂时未找到方便的修复方法。在一篇帖子中看到，应该是休眠之后蓝牙的电源被系统的关闭，未能打开。
        所以可以**切换到Window中，关闭并打开蓝牙一次**。
    - 蓝牙只能保持打开，无法关闭。

