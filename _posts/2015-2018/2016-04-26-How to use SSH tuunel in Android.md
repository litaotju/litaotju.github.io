---
layout: post
title: How to use SSH tuunel in Android
description: 
category: 
tags: 
    - 自由
    - GreateWall
---
{% include JB/setup %}

# 据说中国发出的第一个电子邮件是：
    Across the Great Wall we can reach every corner in the world.

但是，到了现在，我们仍然还有一个GreatWall在哪里。无论如何，中国人民的智慧是无穷的，下面借助一些工具，来达成我们
Acrooss the GreatWall的目的,请依次完成以下三个步骤:

# 方案1: Server + PC + Android

## 一、可以SSH的 Server

1. 首先你要有一个SSH Server，当然：需要在墙外。OpenShift是一个不错的选择。

## 二、你的PC

1. 在你的电脑上安装SSH客户端，连接到Server.
    * windows下可以使用Putty
    * Ubuntu下直接使用 ssh 命令行工具
2. 使用你的SSH客户端连接到 Server，同时设置 Port Forwarding，以及允许其他客户端共享这个Forwaring（必不可少，因为，Android需要连接次电脑的这个端口）

>参考链接：  
>[如何使用OpenShift的SSH功能进行自由浏览](http://www.freehao123.com/openshift-vagex/)  
>[Get out using ssh dynamic forwarding with openshift](http://drinkey.github.io/%E5%B7%A5%E5%85%B7%E4%B8%8E%E6%8A%80%E5%B7%A7/2014/09/05/ssh-proxy-openshift/)   
>[SSH远程操作和端口转发原理与应用](http://www.ruanyifeng.com/blog/2011/12/ssh_port_forwarding.html)
    
## 三、Android手机
在执行完上面两个步骤之后，可以有有两个方法。实现Android手机共享PC SSH。方法如下：

1. 安卓可以不借助客户端，PC装 **Privoxy**
   * 在PC上安装一个 **Privoxy** 软件。  
   在安装好Prioxy之后，在Main Configuration里面添加如下两句:
        forward-socks5 / 127.0.0.1:8899 .
        listen-address 0.0.0.0:8080
   
   >参考链接:[共享电脑ssh代理Android手机上Google play](http://www.xidige.com/other/340)

   * 设置安卓的Wifi代理：长按Wifi名->修改网络->显示高级选项->代理->手动->
        代理服务器主机名为：PC的局域网地址
        代理服务器端口：8080  
   * 保存。就可以欢快的上Google以及Google Play服务了
   
   >参考连接: [Android代理设置方法](http://jingyan.baidu.com/article/219f4bf7ff97e6de442d38c8.html)

2. PC端不需要装软件，在安卓手机上安装 ProxyDroid（！汗想要安装这个软件，首先要能上Google Play。所以如果你之前不能上，请果断选择方法1）
   使用这个方法可以指定哪些软件必须经过代理，那些不用代理。所以比较方便。不影响手机上其他软件上国内网站的速度。
   * Root你的安卓手机  
        root的方法请自行查阅资料。之所以需要root是因为 ProxyDroid需要 root权限，才能执行
        
    >荣耀手机可以参考连接:  
        * [获取华为手机解锁码](https://www.emui.com/plugin.php?id=unlock&mod=step)   
        * [如何root你的手机](http://www.mytechgarbage.net/2015/05/honor-4x-che2-l11-how-to-root-honor-4x.html)
        
   * 安装并设置ProxyDroid
   * 在ProxyDroid上设置代理：host为PC的IP地址。 port为在PC的 Putty上设置的 Dynimic Port
   * 启用上面的代理设置。就可以欢快的上Google以及Google Play服务了。
   
方案1亲测有效。

# 方案2：Server + Android

## 屡试屡败的方案
本方案比方案1来说，可以省略PC这个中间环节，所以理论上速度应该更高。同时，对于没有Wifi的时候，可以直接采用移动网络自身。
之所以能省略是因为将PC上的SSH转发工具，移到了Android手机上。方法如下：

1. 在手机上安装 **Serverauditor** SSH客户端。设置 Host，以及 Forward。经测试可以直接连接上服务端的ssh。
2. root你的手机
3. 在手机上安装 **ProxyDroid**。 设置Host，端口，以及连接方式。

方案2正在测试。经过测试，本方案无法直接无法上网。为测试是Serverauditor的端口转发还是ProxyDroid全局代理的问题，做了如下测试：

1. 直接使用Serverauditor可以SSH登陆连接OpenShift。
2. 使用Serverauditor，进行端口转发 设置 0.0.0.0:8899,使用电脑可以共享手机的这个SSH转发功能。说明 Port Fowarding没有问题
3. 设置Serverauditor端口转发之后，再设置ProxyDroid的代理到 127.0.0.1:8899。无论是全局代理还是应用程序代理，被代理的都无法连接网络。任何网络都无法连接。
4. 不使用Serverauditor，直接使用ProxyDroid共享电脑的SSH Forwarding, ProxyDroid可以正常使用。

所以症结就在于： ProxyDroid和 Serverauditor，单独使用，都可以完成自己的功能。 ProxyDroid可以设置代理（代理服务器不在本机）， 
Serverauditor可以进行端口转发(0.0.0.0:8899)，但是ProxyDroid和 Serverauditor却无法配合起来。即无法完成:既拿手机当SSH Forwarding的中转，同时对手机自身的流量进行转发的功能。

## 在此 Almost绝望的时候， Google来了一个教程
>[Setting Up A Global SSH Proxy on Android with ConnectBot and ProxyDroid](https://pthree.org/2015/08/26/setting-up-a-global-ssh-proxy-on-android-with-connectbot-and-proxydroid/)

这个家伙想干同样的事情，同样使用 ProxyDroid来设置全局代理，不同点就是它的 SSH客户端是 ConnectBot 而不是Serverauditor。抱着试一试的心态
就下载了 ConnectBot， 按照教程中的方法设置，其实就是前面 Serverauditor设置的翻版， 但是居然成功了。
这说明以下的问题： 

1. ProxyDroid可以设置本地 SSH Forwarding的端口为代理。 而前面直接用 ProxyDroid设置PC的 Forwarding端口为代理时也可以。说明 ProxyDroid完全没有问题；  
2. Serverauditor可以进行SSH Forwarding， 也可以将此分享给电脑（设置自己的地址为0.0.0.0）, 但是无法将Forwarding的端口分享给自己。

结论：是Serverauditor的问题。
所以根据不同需求的最终方案是：   

1. 光手机翻： 纯粹使用手机的话，直接使用ConnectBot 和 ProxyDroid。  
2. 电脑和手机一起翻：使用PC的SSH客户端，做转接， （1）使用 Putty + ProxyDroid。 （2）或者 Putty + Prioxy + 手机设置Wifi代理  
3. 光电脑翻：使用Android的SSH客户端为PC做转发， 使用Serverauditor。但是这样做没有意义啊，如果电脑和手机在一个局域网里面，手机可以上网，电脑自然可以，不需要手机做转接。
如果电脑本身无法上网，手机可以通过移动网络上网，但是这样电脑怎么连接到手机的IP地址？Serverauditor。太麻烦了，即使可以使用，也太费流量，一般没有必要。所以**Serverauditor可以直接扔掉了**。

# Tips
在ssh登陆到到OpenShift之后，如果长时间没有在终端操作，openshift会自动断开ssh连接。
不论使用什么ssh客户端（手机或者电脑，Putty或者ssh），在登陆之后，在终端输入如下指令：

    unset TMOUT

禁止掉服务器端的 TMOUT环境变量，就可以防止被踢了。
