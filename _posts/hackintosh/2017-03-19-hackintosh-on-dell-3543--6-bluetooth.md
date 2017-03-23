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

2. 存在的问题及解决方案：
问题1：长时间睡眠之后，无法再次连接蓝牙。暂时未找到方便的修复方法。在一篇帖子中看到，应该是休眠之后蓝牙的电源被系统的关闭，未能打开。
        所以可以**切换到Window中，关闭并打开蓝牙一次**。        
解决方法:
    - 步骤1: 按照[网址]http://forum.osxlatitude.com/index.php?/topic/2925-bluetooth-firmware-uploader/的说法，下载BTFirmwareuploader.kext,并安装。由于osxlatitude论坛需要注册才可以下载，所以在github(https://github.com/nguyenlc1993/mac-os-k501l/releases) 上找到BTFirmwareuploader.kext并下载。
    - 步骤2: 修改 BTFirmwareuploader.kext/Contents/Info.plist, BTFirmwareUploader.kext/Contents/PlugIns/BluetoothDevQAtherosInjector.kext/Contents/Info.plist， 将这两个plist文件的IOPeronality部分中的任意一个AR3012部分的idProduct和idVendor修改成本机的蓝牙设备的ID。如下：
        <key>idProduct</key>
		<integer>54</integer>
		<key>idVendor</key>
		<integer>3315</integer>
    - 步骤3: 使用Kext Wizard安装BTFirmwareUploader.kext，并使用该工具Repair 权限和重建SLE Cache。

问题2: 蓝牙只能保持打开，无法关闭。
解决方法：暂无


3. 参考网址：
    - http://forum.osxlatitude.com/index.php?/topic/2925-bluetooth-firmware-uploader/
    - https://github.com/nguyenlc1993/mac-os-k501l/releases
    谢谢
