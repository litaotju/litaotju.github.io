---
layout: post
title: Hackintosh tutorial on Dell Ins 3543
description: 
category: 
tags: 
---
{% include JB/setup %}


# 电脑配置

- Dell Ins 3543
- CPU: Intel Core I5-5200u, HD5500 Graphics, (Broadwell架构)
- GPU: Nivdia GT 920m, (开普勒架构)
- Audio: Realtek High Defination Audio, 型号ALC3234
- Enthernet: Realtek PCIe Enthernet, 型号RTL8411b
- WireLess: Dell 1705 Wireless
- SD Card： Realtek, 型号RTS5170

# 系统安装

1. VMware虚拟机Mac 下载 macOS Sierra。
2. 使用Unibeast制作启动盘。
3. 安装过程中遇到 蓝牙键盘配对的问题，同时无法识别笔记本自带的PS2键盘和触摸板。此时，插入外接USB键盘，遇到配对问题时单击空格键两次就可跳过。
4. DiskUtil制作Mac分区，并安装系统到硬盘。没出现任何问题。

# 安装系统后的步骤

0. 使用USB启动盘再次启动，不过这次在Clover界面 选择 硬盘上的MAC。

1. 使用MultiBeast安装EFI到系统盘。
    由于MultiBeast 是针对CustoMac定制的，所以一些驱动不是很符合Dell 3543。所以这一步是为了创建一个EFI分区，MultiBeast安装到EFI分区的其他东西最后都被替换。

2. 挂载将EFI分区，并用PCBeta上下载的某网友的EFI文件夹 整个替换 MultiBeast安装的EFI文件夹。

3. 安装其他驱动。

# 安装其他驱动 

### 独立显卡: 顺利安装了WebDriver-367.15.10.15f03.pkg。

+ 但是安装之后，如果不修改config.plist 则系统显示只是启用了OSX自带驱动。

+ 如果按照[网页](https://www.tonymacx86.com/threads/new-method-for-enabling-nvidia-web-drivers-in-clover.202341/)修改config.plist则，
            系统显示 还是只启用了OSX自带驱动，同时，亮度无法调节。

 + 所以最后又将config.plist修改为原位，使得可调节亮度。

### USB无线网卡：可正常工作。但是重新启动后，有时无法发现USB网卡，需要插拔一下。 

 - 安装TL-WN725N_V2_160128.zip里面的 Package, 不修改任何config.plist. 

 - 下载链接：[TP-LINK US](http://www.tp-link.us/download/TL-WN725N_V2.html#Driver) 

### PS2键盘与触摸板：可正常工作， 但是触摸板**不能触击只能点击**。  

- 可正常工作.

- 使用Kext Wizard 安装 RehabMan-Voodoo-2016-0616.zip 中的 VoodooPS2Controller.text。

- 下载链接：[RehabMan Bitbuket](https://bitbucket.org/RehabMan/os-x-voodoo-ps2-controller/downloads)

- 安装方法参考[RehabMan大神的Github](https://github.com/RehabMan/OS-X-Voodoo-PS2-Controller/wiki/How-to-Install)

### 修复触摸板触击无效，系统设置中触摸板为空：可正常工作  

 - 下载 OSX 10.11的 TrackPad.prefPane 替换 S/L/PreferencePanes/TrackPad.prefPane。

 - 参考安装方法： http://bbs.pcbeta.com/forum.php?mod=viewthread&tid=1699479&page=1 

### 修复触击必须要开机后打开系统偏好》触摸板》设置，才能正常工作：  

 - 下载Rehabman 的 ioio， 拷贝到/usr/bin

 - 写一个脚本使用ioio激活触摸板。（trackpad.sh）

 - 设置开机(/Librarys/LaunchDeamon)和登陆自动执行(Automater)该脚本。

### 背光调节：可正常工作  

 - 使用Kext Wizard安装 RehabMan-IntelBacklight-2016-0506.zip 中的 IntelBacklight.kext。

 - 在config.plist中ACPI/DSDT/Fixes 添加“AddPNLF_1000000”项为“True”。 

 - 下载链接：[RehabMan Bitbuket](https://bitbucket.org/RehabMan/os-x-intel-backlight/downloads)

 - 安装方法参考[RehabMan大神的Github](https://github.com/RehabMan/OS-X-Intel-Backlight)

### 电池状态：可正常工作  

 - 使用 Kext Wizard 安装RehabMan-Battery-2016-0628.zip中的 ACPIBatteryManager.kext。

 - 下载链接：[RehabMan BitBuket](https://bitbucket.org/RehabMan/os-x-acpi-battery-driver/downloads) 

 - 安装方法参考[RehabMan大神的Github](https://github.com/RehabMan/OS-X-ACPI-Battery-Driver)

### 声卡：可正常工作  

 - 删除 S/L/E下的 AppleHDA.kext，使用 Kext Wizard 安装 VoodooHDA.kext (版本289)， Repair Permissions and Rebuild Cache, 重启。

 - 下载链接：[Source Forge VoodooHDA](https://sourceforge.net/projects/voodoohda) 

### 以太网卡：可正常工作  

 - 经过验证发现，按照Windows下的说明，查找的以太网卡号RTL8111b 与mac下DCPIManager识别的型号不同。 所以本来一直视图安装Mieze和Rehabman的提供的RealtekRTL8111.kext完全无法驱动网卡。

 - 在Insanelymac论坛上找到 Mieze写的 RealtekRTL8100.kext

 - 把Clover/kexts下的， S/L/E和/L/E下 旧的RealtekRTL8111.kext完全删除，Rebuild Cache。

 - 使用Kext Wizard安装 RTL8111.kext，重新启动。直接可发现以太网卡。

# 解决的其他问题：

### App Store无法登陆：

1. 步骤1
    - ifconfig发现电脑里面没有 en0
    - 按照Rehabman的说法，删除 System》Preferences》Network中的所有接口, 删除 L/Preferences/SystemConfiguration中的 NetworkInterfaces.plist文件
    - 重启。

2. 步骤2.
    - 删除 Clover/kexts中的 IOBluetoothFamily.kext。重复步骤1，并重启电脑。 System》Preferences》Network首先添加以太网，就好了。

3. 步骤3. 
    - 把 IOBluetoothFamily.kext放回去。（不影响其他系统功能，其实好像也可以不放）

### 触摸板三个手指手势的问题

安装VoodooPS2Controller.kext之后，发现在Safari之下，三只手指触击可直接在后台新的标签页打开网页。同时，由于Dell 3543带Synaptics在Windows可以识别三个手指的手势，说明在触摸板在硬件上支持3手指手势且已经被Hackintosh识别了三指触击。所以试图实现与Windows10 类似的手势识别方案。

在翻了无数帖子之后，发现VoodooPS2Controller驱动实际上将三个手指的触摸板手势映射为键盘中的组合键。它的定义在
"/System/Library/Extensions/VoodooPS2Controller.kext/Contents/PlugIns/VoodooPS2Keyboard.kext/Contents/Info.plist"文件中的几个键 “ActionSwipeUp”， "ActionSwipeDown", "ActionSwipeLeft", "ActionSwipeRight"中，具体的定义片段如下:

	<key>ActionSwipeDown</key>
	<string>3b d, 37 d, 7d d, 7d u, 37 u, 3b u</string>
	<key>ActionSwipeLeft</key>
	<string>3b d, 37 d, 7b d, 7b u, 37 u, 3b u</string>
	<key>ActionSwipeRight</key>
	<string>3b d, 37 d, 7c d, 7c u, 37 u, 3b u</string>
	<key>ActionSwipeUp</key>
	<string>3b d, 37 d, 7e d, 7e u, 37 u, 3b u</string>

注意其中的值 “3b d, 37 d, 7d d, 7d u, 37 u, 3b u”形式表示了分别同时按下编码为 “3b 37 7d”的按键，然后同时松开三个键。所以只需要将“3b 37 7d”的三个按键找到，并在快捷键中设置为想要的行为，就可以实现三个手指的手势识别。
那么出现在上述的定义中的编码分别表示那个按键。但是着了半天也没看到，因为苹果系统定义的按键编码和其他PC机不知道是否相同。

但是怎么知道某一个手势到底对应那几个按键呢？

答案是，打开 系统偏好设置》键盘》快捷键， 然后随意的双击某一个快捷键的设置，在双击之后，用三个手指上（或者下，左，右）划动触摸板。因为驱动把触摸板手势映射为组合键，所以手势之后必然相当于同时按下了几个键，进而就可以成功的设置手势识别。
经过实验发现:

	向上划动映射为 "Ctrl + Alt + 上方向键"
	向下划动映射为 "Ctrl + Alt + 下方向键"
	向左划动映射为 "Ctrl + Alt + 左方向键"
	向右划动映射为 "Ctrl + Alt + 右方向键"
	
进而，对Mission Control的快捷键部分进行如下的设置，可以实现“向下显示桌面，向左和向右切换桌面，向上打开Mission Control”部分的功能。

![快捷键设置](/assets/pic/trackpad_gesture.png)


### 电脑无法正常关机的问题

在正常使用了一段时间之后，关闭电脑时会出现显示器关闭，但是硬盘灯一直亮的情况，风扇也在响说明电脑无法正常关机。在TonymacX86上搜索时，发现了一个帖子。有人因为安装VirtualBox而出现Hackintosh无法关闭的情况。经过测试，发现确实是VirtualBox的问题。卸载后可以正常关机，安装后无法关机。所以只能和VBox说再见了。
参考链接：https://www.tonymacx86.com/threads/solved-shutdown-restart-takes-too-long-clover-10-10-5.170933/
