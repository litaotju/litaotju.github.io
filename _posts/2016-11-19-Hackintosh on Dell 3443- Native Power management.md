---
layout: post
title: Hackintosh on Dell 3443- Native Power management
description: 
category: 
tags: 
---
{% include JB/setup %}

电源管理对于电脑的功耗的动态调节，尤其是笔记本尤其重要。在Dell 3543上安装好各种驱动之后，一直想着可以去激活电源管理。
为此，进行了如下步骤：

1. 参照了如下的网址和教程[Rehabman Guide:Native Power Management for Laptops](https://www.tonymacx86.com/threads/guide-native-power-management-for-laptops.175801/)
但是使用教程中的./ssdtPRGen.sh脚本去生成 ssdt时，爆出了一个提示错误 “BroadWell 不支持 Macbook Air 6，2” system defination。所以可能产生的SSDT对于电源管理有错误。
具体的错误和解决方法和 ssdtPRGen.sh脚本的作者在github上有人提出的issue很类似，见网址：https://github.com/Piker-Alpha/ssdtPRGen.sh/issues/209。

使用 "./ssdtPRGen.sh -show"， 其中输出的一部分信息截取如下：

    Broadwell
    Mac-9F18E312C5C2BF0B / MacBookAir7,1
    Mac-937CB26E2E02BB01 / MacBookAir7,2
    Mac-E43C1C25D4880AD6 / MacBookPro12,1
    Mac-A369DDC4E67F1C45 / iMac16,1
    Mac-FFE5EF870D7BA81A / iMac16,2
    Mac-BE0E8AC46FE800CC / MacBook8,1
    Mac-F305150B0C7DEEEF / MacBook8,2

可以看到 Broadwell well只支持上述的系统定义，而使用pcBeta上某网友提供的EFI中的配置，SMBIOS是 Macbook Air 6,2。
所以需要修改 ／CLOVER/config.plist中的 SMBIOS部分，为上述系统的中的一个。
可参见： https://clover-wiki.zetam.org/Configuration/SMBIOS

2. 修改SMBIOS
    - 下载Clover Configurator
    - 按照 http://www.insanelymac.com/forum/topic/302347-clover-imessagefacetime-fix-for-yosemite/ 中的方法修改。
    - 重启电脑，SMBIOS已经改完了。

3. 按照步骤1的链接Rehabman：guide重新运行 ./ssdtPRGen.sh 脚本， 生成SSDT.aml放到 ／ACPI／pacthed中去。并重启电脑。

4. 验证电源管理安装正确，参考网址：http://osxarena.com/2016/04/guide-how-to-test-powemanagement-hackintosh/