---
layout: post
title: Django 开发之 Model：后台数据库切换配置
description: 
category: Python
tags: 
---
{% include JB/setup %}

# 从SQLite切换到 MySQL
Django可以使用 SQLite, MySQL等作为后台的数据库，新建一个project默认的配置如下：
    
    #使用了SQLite作为数据库    
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }

可以切换为 MySQL作为后台数据库，切换的步骤如下:

- 安装MySQL Server
- 安装MySQL的Python接口, 需要安装MySQL-python包，但是PyPi上只有python2的安装包，所以需要另外找到兼容python3的安装包
    + http://www.lfd.uci.edu/~gohlke/pythonlibs/ 可以使用这个网址下载 MySQL-client，它能够兼容python3
    + 下载之后使用 `pip install ****.whl`安装

- 使用命令行新建名为 mysite 的数据库
    + ` mysql -u root -p`登陆myspl
    + `create database mysite`


- 修改django工程的 setting.py 改成如下

```python
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mysite',  # 数据库名
        'USER':'root',     # mysql用户名
        'PASSWORD':'yourpassword**', # 密码
        'HOST':'',         # mysql的 host，空则默认为 localhost
        'PORT':'3306',     # mysql监听的端口，一般为3306
    }
```

- 进行数据库迁移：
    + `manage.py migration` 此命令会在上面新建的 mysite数据库中新建django需要的表。
