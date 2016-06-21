---
layout: post
title: Flask 开发之Model：Flask-SQLAlchemy
description: 
category: flask
tags: 
---
{% include JB/setup %}

## 介绍
SQLAlchemy 是一个 Python语言的ORM包，它支持多种数据库，比如 MySQL和 SQLite。而 Flask-SQLAlchemy是一个用于
Flask框架的ORM插件，它依赖于 SQLAlchemy。使用Flask开发框架可以自己直接 SQLAlchemy，也可以使用Flask-SQLAlchemy插件。
一般来讲后者更加方便。所以这里只介绍Flask-SQLAlchemy的使用。关于SQLAlchemy的使用本身，可参考该包的文档。

## 安装
首先需要安装这三个包。 第一个是 MySQL数据的Python Driver，适用于python3.

    pip install mysqlclient-1.3.7-cp35-cp35m-win32.whl (下载地址可参见前一篇Django后台数据库切换)
    pip install SQLAlchemy
    pip install flask-sqlalchemy

## 基本使用
Flask-SQLAlchemy插件一般需要在 一个Flask APP中使用。一个最小的使用步骤如下：
1. 导入所需要的包

```python
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
```
2. 声明app和 SQLAlchemy对象

```python
    app = Flask(__name__)
    ## 配置 flask_sqlalchemy包需要的app环境变量
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
```
3. 声明一个 继承自SQLAlchemy.Model的类，并按照模型的要求写清楚字段的约束。下文中均使用 db代称在这里创建的 SQLAlchemy对象。

```python
    db = SQLAlchemy(app)
    class User(db.Model):
        ## 每一个字段的都是 db.Column的实例
        ## 声明一个字段时可以用到的关键字参数有：  primary_key, nullable, unique
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True)
        email = db.Column(db.String(120), unique=True)
        
        ## 构造函数可选，可以不定义构造函数，一般有需求时才定义，可以在构造函数中制定 字段的默认值等
        def __init__(self, username, email):
            self.username = username
            self.email = email
        
        ## 对象的打印格式
        def __repr__(self):
            return '<User %r>' % self.username
```
4. 创建表和删除表

```
    db.create_all() 
    db.drop_all()
```

经过观察发现 db.create_all() 在一个表的名称已经存在的情况下是不会修改原来的表的。所以每一次Python db.Model子类的
修改，可能需要手动的修改数据表。或者直接 drop_all() 之后，再使用 create_all() 创建

5. session的使用
定义好对象之后，可以直接实例python对象，然后使用 db.session.add(Obj)将对象添加到数据库中。
但值得注意的是，使用 db.session.add(Obj)没有完成一个事务，还可以撤销。完成事务需要 db.session.commit()函数。
具体的代码片段如下：

```
    >>>user = User('admin', 'admin@jkl.com')
    >>>db.session.add(user)
    >>>db.session.commit()
```

如果想从数据库中删除这个对象，可以使用：
```
    >>> db.session.delete(user)
```

6. Query
每一个 db.Model的子类，都有一个 query对象。可以使用如下的方式从数据库中 query对象

```
    >>> users = User.query.all()
    [<User u'admin'>, <User u'guest'>]
    >>> admin = User.query.filter_by(username='admin').first()
    <User u'admin'>
```
7. 关系和其他主题 比如增删查改可参见文后的参考链接

## 详细文档
>[Flask-SQLAlchemy文档](http://flask-sqlalchemy.pocoo.org/2.1/)  
>[Flask-SQLAlchemy环境变量设置](http://flask-sqlalchemy.pocoo.org/2.1/config/)  
>[模型声明和关系](http://flask-sqlalchemy.pocoo.org/2.1/models/)  
>[Select Insert Delete](http://flask-sqlalchemy.pocoo.org/2.1/queries/)  
