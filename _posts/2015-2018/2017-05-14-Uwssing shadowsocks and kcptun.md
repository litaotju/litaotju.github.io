---
layout: post
title: Using shadowsocks and kcptun
description: 
category: 
tags: 
---
{% include JB/setup %}

Here is step of using shodowsocks and kcptun to cross the GFW.
shadowsocks itself is sufficient, but with the help of kcptun, the speed when watching video really boosted.

# I. Server side 

## 1. Get yourself a VPS 

You can using aws free tier for one year. Sign up an aws account, and instance an **EC2** vps.
The details of this step are all in the internet. If you consider using other vps or cloud vender, lot of people recommand the **banwagong** (搬瓦工）considering it's cheap price.


## 2. Install shadowsocks in sever

The basic flow is as simple as:

    apt-get update
    apt-get install python-pip
    pip install shadowsocks  
    vim /etc/shadowsocks.json # 建立配置文件
    sudo ssserver -c /etc/shadowsocks.json -d start

If you are using EC2 of aws, remember add the server port of shadowsocks to you network interface security group.

Here is an example of shadowsocks.json for you as a refrence
<pre>
  {
    "server":"0.0.0.0",
    "server_port": ss_server_port,
    "local_address":"127.0.0.1",
    "local_port":1080,
    "password":"ss_passwd",
    "timeout":300,
    "method":"aes-256-cfb",
    "fast_open":false
  }
</pre>

## 3. Tune the parameter of server 

To maxmize the performance of the shadowsocks server, you shoud edit the `/etc/sysctl.conf` to tune the kernel parameter and then use `sudo systcl -p` to load it.

The conf file you can refrence the [shadowsocks.org](https://shadowsocks.org/en/config/advanced.html)
or ref the [github shadocks_install](https://github.com/iMeiji/shadowsocks_install/wiki/shadowsocks-optimize)

If you are using EC2 in low latency region, like tokyo region. Remember to using assign the 
**net.ipv4.tcp_congestion_control= htcp** in the conf file.


## 4. Using kcptun to acceralate the shadowsocks

- wget  kcp_url #download kcptun from [github](https://github.com/xtaci/kcptun/releases)
- vim /etc/kcptun.json  # [confgure ref](https://wuwenhan.top/web/deploying-kcptun-to-make-shadowsocks-great-again/)
- nohup ~/kcptun/server_linux_amd64 -c /etc/kcptun.json >> /dev/null & 

Here is an example of the configure for kcptun
<pre>
{
    "listen": "0.0.0.0:kcp_server_port",
    "target": "127.0.0.1:ss_server_port",
    "key": "kcp_passwd",
    "crypt": "salsa20",
    "mode": "fast2",
    "mtu": 1400,
    "sndwnd": 2048,
    "rcvwnd": 2048,
    "datashard": 70,
    "parityshard": 30,
    "dscp": 46,
    "nocomp": false,
    "acknodelay": false,
    "nodelay": 0,
    "interval": 40,
    "resend": 0,
    "nc": 0,
    "sockbuf": 4194304,
    "keepalive": 10
}
</pre>


# II. client side

## For mac 

### 1. Install and using shadowsocks client
    pip install shadowsocks
    vim /etc/shadowsocks.json
    sslocal -c /etc/shadowsocks.json -d start

Herv is an example of ss local configure file
<pre>
{
     "server": "127.0.0.1",
     "server_port":ss_local_port,
     "local_address": "127.0.0.1",
     "local_port":1080,
     "password":"any password",
     "timeout":300,
     "method":"aes-256-cfb",
     "fast_open": true
}
</pre>

Here since you need the kcptun to be as an intermediate, so the server field here is "127.0.0.1".
If you don't want the kcptun, just fill the real server ip in "server" field.
**Now you can tell chrome plugin to use 127.0.0.1:1080** as a socks5 proxy.


### 2. Install and using kcptun
    get kcptun from github
    vim /etc/kcptun.json
    nohup ~/client_darwin_amd64 -c /etc/kcptun.json >> /dev/null &

Here is an example of kcptun confiure for client side
<pre>
{
        "localaddr": ":ss_local_port",
        "remoteaddr":"you_vps_ip:kcp_server_port"
        "key": "kcp_passwd"
        "crypt": "salsa20",
        "mode": "fast2",
        "mtu": 1400,
        "sndwnd": 2048,
        "rcvwnd": 2048,
        "datashard": 70,
        "parityshard": 30,
        "dscp": 46,
        "nocomp": false,
        "acknodelay": false,
        "nodelay": 0,
        "interval": 40,
        "resend": 0,
        "nc": 0,
        "sockbuf": 4194304,
        "keepalive": 10
}
</pre>

Please confirm here is kcptun local parameter is same with the kcptun configure in the server.
Also,  make sure the remoteaddr is match with the vps_ip and kcp_server_port in the vps. 

**The kcptun accelerate really make the speed of shadowsocks sevreal times faster. You can even watch
1080p video on youtube very smoothly.**

## For android

1. Install shadowsocks app and kcptun plugin of shadowsocks from google play
2. configure the app and using it. (as simple as that)

**The kcptun may consume more data, so you can configure more than one shadowsocks ports in the server
some of them is accelerated by kcptun, others are not. The port not using kcptun can be used when you are using data connection, and kcptun port can be used when you are using wifi.**

Other Reference:
>[AWS 上搭建免费每个月 15G 的 shadowsocks](https://juejin.im/entry/56cc1f922e958a00592fe4dd)  
>[使用kcptun对Shadowsocks加速](http://www.jianshu.com/p/78420fad1481)  
>[shadowsocks org](https://shadowsocks.org/en/download/servers.html)  
