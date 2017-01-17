---
layout: post
title: "Hackintosh on Dell 3543 - 4.Shutdown Problem"
description: ""
category: 
tags: []
---
{% include JB/setup %}

## 电脑无法正常关机的问题

1. 在正常使用了一段时间之后，关闭电脑时会出现显示器关闭，但是硬盘灯一直亮的情况，风扇也在响说明电脑无法正常关机。在TonymacX86上搜索时，发现了一个帖子。有人因为安装VirtualBox而出现Hackintosh无法关闭的情况。经过测试，发现确实是VirtualBox的问题。卸载后可以正常关机，安装后无法关机。所以只能和VBox说再见了。
参考链接：https://www.tonymacx86.com/threads/solved-shutdown-restart-takes-too-long-clover-10-10-5.170933/

2.（补充） 卸载了VirtualBox之后，使用了一段时间之后，还是出现了无法关机的问题。又在网上看到教程说是，和bios的设置有关系。尝试着设置bios，将NIC disable掉之后关机果然正常了。同时，再次将NIC enbable，无法关机的问题会重现。所以，只能在bios中disable掉NIC。但是disable之后，以太网卡会无法识别。所以将无法使用App Store。 只能在使用App Store的时候，Enable NIC，使用完继续disable。
