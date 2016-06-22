---
layout: post
title: Flask 开发之 Extensions
description: 
category: flask
tags: 
---
{% include JB/setup %}

# 介绍
Flask是一个微框架，微的意思是什么呢？就是没有多余的代码，你可以使用简单的代码完成简单应用。完全可以不需要SQL数据层的网站也是可以的。
但是这并不意味着Flask的功能太弱小，Flask开发的一个好处是你完全可以使用自己想使用的任何插件或者模块完成你自己的任务。Flask只提供了一个
在Werkzeug和 Jinja2之间的一个连接。 关于Flask的插件，都可以在这个网站下载。[http://flask.pocoo.org/extensions/](http://flask.pocoo.org/extensions/)。

# 常用的几个扩展
在上一篇文章[Flask 开发之Model：Flask-SQLAlchemy](/flask/2016/06/21/Learning-Flask-ORM-SQLAlchemy/)中已经介绍了一个Model层的插件。
还有的几个常用的插件如下：
    
- Flask-Script #一个Flask Shell环境，包括比较常使用的 Manager类来方便的管理Flask Web应用
- Flask-Testing # 关于测试的插件，还没有详细看
- Flask-Uploads 
- Flask-Cache
- Flask-WTF
- Flask-SQLAlchemy

# 其他可能用到的插件
- Flask-Admin
- Flask-Login
- Flask-Migrate
- Flask-Oauth
- Flask-User

### 插件信息官网
>[http://flask.pocoo.org/extensions/](http://flask.pocoo.org/extensions/)。
