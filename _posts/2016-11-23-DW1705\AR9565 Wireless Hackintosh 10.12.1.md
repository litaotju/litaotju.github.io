---
layout: post
title: DW1705\AR9565 Wireless Hackintosh 10.12.1
description: 
category: 
tags: 
---
{% include JB/setup %}

# 全宇宙无解的Wifi网卡终于可以Hackintosh了

在查找资料的过程中，翻到了youtube上的一个牛人，在Serria上成功安装了 AR9565 Wifi网卡的
驱动，于是乎看到了 Dell 1705和AR9565实际上是一个无线网卡，1705采用了AR9565的芯片。
而且安装过程及其简单，所以抱着试一试的心态就装了一下。结果就成功了。


参考网址如下：
1. [Kext for wifi ar9565 for hackintosh macOS Sierra 10.12 (16A323)](https://www.youtube.com/watch?v=4Q_bLKSCFDU&index=1&list=PLOvTQVrAAYx-tSVQ_AXYzxF1M3mo00iSE
)

2. 下载链接是在中国的pcbeta上找到的，由于下载比较下，所以直接附上[AR9565kextsFor10.12](/assets/9565kexts.zip)


好像由于我自己的Clover设置，使得在 /EFI/Clover/kexts/10.12/ 系统不会加载，
所以我的安装步骤于原教程，略有不同，安装过程如下：


1. cd into S/L/E delete(or add .dackup to disable) IO80211Family.kext and IO80211FamilyV2.kext and corecapture.kext。在这一步中，我没有删除其中的kext文件夹，只是在每一个后面加入了一个 .backup 

2. use Kext Wizard to repair perm and clean cache, install these three kexts to /S/L/E

3. repair perm and clean cache

4. reboot


## 缺点

1. 好像安装好之后 wifi连接很不稳定，有时候即使连接着wifi也无法上网。（但是USB wifi也这样啊，所以基本无所谓了）。





