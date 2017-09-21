---
layout: post
title: "Hackintosh on Dell 3543 - 6. Update to 10.12.6"
description: ""
category: 
tags: [Hackintosh]
---
{% include JB/setup %}

# Major issue and fix:

1. Wifi找不到硬件, 按照之前的教程重新安装即可。

2. Audio 找不到硬件, 按照之前的教程重新安装VoodooHDA。

3. 背光调节。之前使用了 IntelBacklight.kext 在10.12.4之后无法使用。
   参照教程[Guide: Laptop backlight control using AppleBacklightInjector.kext] (https://www.tonymacx86.com/threads/guide-laptop-backlight-control-using-applebacklightinjector-kext.218222/) 。首先对ACPI中所有的DSDT 和SSDT 进行patch，GFX0 替换为IGPU. 然后按照网址所示教程即可。

