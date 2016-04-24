---
layout: post
title: 在Openshift上搭建Flask应用程序
description: 
category: python
tags: 
    - python
---
{% include JB/setup %}
# 申请OpenShift账号
如标题。 https://www.openshift.com

# 搭建SSH环境和rhc CLI工具
使用Putty SSH远程登陆OpenShift.
rhc是openshift提供的一个gem 命令行工具，用于管理用户的opensift应用。

    gem install rhc

**注意**：安装rhc需要 ruby2.0.0以下，使用 ruby2.2.0总是出现require<top>一些包的依赖的问题

安装完之后运行：

    rhc setup

设置用户账户，下次可以不用输入账号密码之间管理部署在openshift上的app。

# 创建应用

openshift作为一个PAAS 平台，支持多种语言和开发环境，在创建一个app时，需要指定这个app的运行时，如果不是openshift的标准gear，也可以自己定制。
如下图：
![create-app](\img\in-post\rhc_create-app.png)

# 使用git管理应用
使用 ```rhc git-clone```可以方便的从openshift网站将自己的git目录克隆到本地。
可用到本地之后，就可以方便的使用标准的git方法来推送自己的代码到opensihft。每一次
使用 ```git push``` openshift接受到代码提交之后，自动终止当前运行的app，然后，应用变更。利用新的代码重新启动应用。
