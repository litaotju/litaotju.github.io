---
layout: post
title: Dell Windows10 Synaptics Touchpad Gesture Bug
description: 
category: 
tags: 
---
{% include JB/setup %}

# 问题描述

在Dell Ins 15-4523 电脑安装Windows 10后，DellTouchPad 的多手指手势操作非常方便。
Windows10 系统提供了2 3 4个手指的各种手势操作，其中与Windows7/8相比，很好用的3手指手势有：

- 3手指上划：预览显示目前所有的打开任务，并可使用鼠标选中进行切换。  
- 3手指下划：隐藏所有应用并显示桌面。  
- 3手指左右划动： 在任务之间进行切换。  

但是在电脑运行过程中，总会**时不时的出现**：将电脑休眠之后再启动，3手指手势变成如下的错误设置：

- 3手指上划：打开Cortana  
- 3手指下划：打开Windows Setting  
- 3手指左右划动： 在桌面中不起任何作用，在Chrome中能够切换网页的 前进和后退。  

该情况的出现比较随机，有时睡眠后设置正确，有时睡眠后设置错误。甚至有时候把有线鼠标插入和拔出都会造成设置的变化。

# 做过的尝试

为了解决此为问题，看了很多网上的教程。一些社区的专业人士比如Dell或者Microsoft的工作人员的建议都比较扯淡。

### 完全不管用的方法有：

1. 严格按照"BIOS，显卡(包括集成显卡和独立显卡)驱动，触摸板驱动"的顺序进行驱动的重新安装。

### 有用但是做起来比较痛苦的方法

2. 当出现错误的设置时，打开任务管理器，找到"Synaptics TouchPad 64-bit Enhancements"，右键点击“结束任务”。关键是每次出现错误都使用这种方法的话，用起来简直痛苦。

3. 把方法2写成一个脚本或者设置成一个Windows常规任务。每次出现错误时运行脚本，或者每次结束休眠后运行Trigger触发任务。


# 最终地解决方法(目前为止有效)

经过google搜索，果然有不少同志都出现了相同的情况。除过Dell的电脑外，其他Lenovo的电脑也出现过，共同点是都使用了Synaptics的触摸板。

## 网友建议

网友说是注册表中 “HKEY_LOCAL_MACHINE\SOFTWARE\Synaptics\SynTP\Defaults\AppProfiles\Google Chrome” 中的设置出现了问题。
以至于每次Windows结束休眠加载这些注册表项中的设置覆盖了正确的设置。
所以给出的建议是 在注册表项的文件夹名“HKEY_LOCAL_MACHINE\SOFTWARE\Synaptics\SynTP\Defaults\AppProfiles\Google Chrome”后面加一个后缀“-save”。
这样，系统找不到错误的注册表项也就不会覆盖正确的设置。

## 尝试和更彻底的方法

**经过观察**： “HKEY_LOCAL_MACHINE\SOFTWARE\Synaptics\SynTP\Defaults\AppProfiles”有很多的软件，除过Chrome之外还有诸如 Word, Excel, PPT等软件。

**提出假设**： “在休眠之前，只要正在运上面这个文件夹中出现的软件在前台，系统休眠结束后就会出现手势设置错误”。  

**验证假设**：  
    1. 确定手势为正确设置的，打开Chrome，使之运行在前台并休眠，唤醒电脑。手势设置果然错误。将手势设置为正确结果。  
    2. 重复步骤1多次，每次均能重现。  
    3. 将Chrome换成 AppProfiles下的其他软件，比如Excel，Word， PPT。重复步骤1多次，每次唤醒电脑后，手势都变为错误的设置。  
    4. 将其他未出现在AppProfiles下的软件置于前台并休眠， 每次唤醒后手势都仍然为为正确结果。  

**初步结论**： 所提的假设正确，问题的关键是休眠时正在前台运行的软件。这些软件的默认手势设置在休眠后重启时都会覆盖正确的手势设置。

**解决方案**： 

    1. 为了不造成系统功能的问题，在修改前导出注册表项：“HKEY_LOCAL_MACHINE\SOFTWARE\Synaptics\SynTP\Defaults\AppProfiles”，保存为一个 “XXX.reg”文件，方便之后再将该项导入。  
    2. 直接删除注册表项： “HKEY_LOCAL_MACHINE\SOFTWARE\Synaptics\SynTP\Defaults\AppProfiles”。  

**实施后的结果**：  
    1. 分别将Chrome, Word, Excel, PPT等原来导致手势错误的软件置于前台，休眠电脑，再次激活电脑。发现手势已经不会变为错误设置。      
    2. 将未出现再Appfiles中的其他应用置于前台，休眠电脑并再次激活电脑。发现手势也不会变为错误设置。  
    3. 重启电脑，再次验证多次，问题已消失。  


# 参考  

[1. Windows 10 touchpad gestures no longer working as expected (XPS 13 9333)](http://en.community.dell.com/support-forums/laptop/f/3518/t/19646398)

[2. Touchpad gestures keep automatically changing to wrong settings](http://en.community.dell.com/support-forums/laptop/f/3518/t/19645958)

[3. Synaptics Touchpad 3 Finger Gestures not working in Windows 10 with Lenovo Flex 3](http://answers.microsoft.com/en-us/windows/forum/windows_10-other_settings/synaptics-touchpad-3-finger-gestures-not-working/2ae44c53-9b88-4e7e-9c45-6f58c89c515a?page=2)

