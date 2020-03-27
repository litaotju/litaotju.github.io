---
layout: post
title: OpenWRT-ss-v2ray-transprency-proxy
description: 
category: 
tags: 
---
{% include JB/setup %}


## Install OpenWRT to RasPi 3b+

As of 2019.06, 3B+ only supported snapshot install of OpenWRT

### Download snapshot image and gunzip it 
```
$ wget https://downloads.openwrt.org/releases/18.06.2/targets/brcm2708/bcm2710/openwrt-18.06.2-brcm2708-bcm2710-rpi-3-ext4-factory.img.gz
$ gunzip xxx.gz
```
### Flash the image to a tfcard
In ubuntu this can be down by `dd` command.

### Install Shadowsocks-libev
Find the ipk, and install it.

### Install v2ray-plugin for ss-libev
* Install `go` in a host where google website can be reached (download the v2ray go package when building the plugin). I did it in vaultr machine.

* git clone v2ray-plugin github repo
* export GOOS=linux; export GOARCH=arm64; go build # will genrate the v2ray-plugin for arm64  openwrt system
* copy the binary to openwrt /usr/bin

### Config the ss, chinadns, dns-forward

* https://www.youtube.com/watch?v=cwaT3GnV7Xw
* https://cokebar.info/archives/664
* https://my.oschina.net/CasparLi/blog/487458


> https://blog.wanfajie.com/2018/08/%E7%94%A8%E6%A0%91%E8%8E%93%E6%B4%BE%E5%81%9A%E4%B8%80%E4%B8%AA%E7%A7%91%E5%AD%A6%E4%B8%8A%E7%BD%91%E9%80%8F%E6%98%8E%E4%BB%A3%E7%90%86%E8%B7%AF%E7%94%B1%E5%99%A8/