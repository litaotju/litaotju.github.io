---
layout: post
title: "Hackintosh on Dell 3543 - 5. Disable Nvidia GPU on laptop"
description: ""
category: 
tags: []
---
{% include JB/setup %}

## 独立显卡无法使用而又耗热的问题 

1. 独立显卡既然不能正常使用，为了减少发热，不如直接disable掉。
参考教程链接://www.tonymacx86.com/threads/guide-disabling-discrete-graphics-in-dual-gpu-laptops.163772/
我的做法步骤：
    (1). 按照教程在ssdt-9.dsl的_INI方法中加入_OFF方法调用。 (未修改_OFF方法和_REG方法，因为我的SSDT比较简单，没有涉及作者所陈述的依赖问题)
    (2). 将config.plist中的 DropOEM=true
    (3). 将**所有的(无论是未patch过的还是patch过的)**SSDT.*.aml 放入EFI/CLOVER/ACPI/patched/文件夹。方便clover调用。

2. 如何验证独立显卡已被禁用
    - 打开System Profiler -》图形卡/显示器 一栏， 里面只有Intel显卡，而无Nvidia显卡，在本教程操作之前，是有
    Nviadia显卡的信息的。
3. Unsolved Problem:
    - 暂未发现

