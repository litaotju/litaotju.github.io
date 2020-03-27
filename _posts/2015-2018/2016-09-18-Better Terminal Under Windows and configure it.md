---
layout: post
title: Better Terminal Under Windows and configure it
description: 
category: 
tags: 
---
{% include JB/setup %}

# Windows下一个好用的Teriminal

ConEmu是Windows一个比较好用的Terminal，且是免费和开源的。比CMD自带的不知道高到哪里去了。

# 配置

1. 修改Setting, 增加右键的Context，也就是如下的效果。
![图片](/img/in-post/terminal-context.png)

2. 修改Setting，将默认的右键Setting换成MingW-Bash
![图片](/img/in-post/conemu-setting.png)

# 问题

经过如上操作之后，每一次右键，进行ConEmu-Bash Here时，默认的路径总是用户的路径。也就是 $HOME路径。如下所示。
![图片](/img/in-post/conemu-home.png)

想要每一次启动之后，在当前的路径运行bash必须还要有额外的一步。

# 解决方法
从ConEmu启动的bash之后发现，环境变量里面多了 $CONEMUWORKDIR 也就是当前打开ConEmu的路径。所以需要进行的额外的修改。判断当前的Bash是否从
ConEmu启动的，如果是，则cd到 $CONEMUWORKDIR的路径。实施的方法如下：

修改"C:\MinGW\msys\1.0\etc\profile"。 在其末尾增加如下语句

```shell
    #此语句判断如果 $CONEMUWORKDIR 环境变量不存在
    if [ "x$CONEMUWORKDIR" == "x" ]; then
        cd $HOME
    else
        cd $CONEMUWORKDIR
    fi
```
