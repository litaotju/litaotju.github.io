---
layout: post
title: Flask开发之Flask-Login 用户登录管理
description: 
category: Web Dev
tags: 
---
{% include JB/setup %}

# 使用Flask-Login的几个基本步骤

## 定义安全的用户模型
- 不要直接在数据库中保存用户的密码，应该存储他们的哈希值。werkzeug.security 模块中的 <code>generate_password_hash, check_password_hash</code>函数来进行哈希值产生和验证。
- 密码应该是只写的， 只有写入和验证两个选项。

```python
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from myapp import db, login_manager

class User(UserMixin, db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True, index=True)
    email = db.Column(db.String(64), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    def __init__(self, username, email, password, role_id):
        self.username = username
        self.email = email
        self.password = password
        self.role_id = role_id

    @property
    def password(self):
        raise AttributeError("Error, password is a write only attribute")

    @password.setter
    def password(self, password):
        print "password", password
        self.password_hash = generate_password_hash(password)
        print "password hash:" , self.password_hash

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
```

## 使用FLask-Login插件包装app，定义一个 login_manager

在app定义的地方加入如下代码：

```python
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.session_protection = "strong"
## 在这里 auth 为一个 bluepint, login是其中的一个 function
login_manager.login_view = "auth.login"
login_manager.init_app(app)
```

## 定义 login_manager的user_loader函数

```python
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
```

## 使用 flask_login.login_required 保护一些只能被登入用户看到的视图

```python
from flask_login import login_required
@app.route("/secret")
@login_required
def secret():
    return "Only logined user can view this"
```

## 使用 flask_login.login_user 函数使用户登入

```python
from flask_login import login_user

@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    # 验证表单，的每一项是否符合要求
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('hello'))
        flash('Invalid username or password.')
    #如果来的是get请求，那么直接返回模板
    return render_template('auth/login.html', form=form)
```

## 其他相关主题
- Flask-Login可以搭配使用Flask-WTF进行登陆表单的生成和验证
一种简单的表单使用方式如下

### 继承一个 flask_wtf.Form 类
```python
# coding: utf-8

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email, Length
# 每一个form都可以用flask_wtf.Form里面的一些属性和方法
# 但同时需要引入 wtforms 包来完善功能

class LoginForm(Form):

    email = StringField("Email", validators=[Required(), Length(1,64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField("Keep me login")
    submit = SubmitField("Login")
```

### 在模板中渲染表单
```
    ## 在模板的开头导入 wtf
    \{\%  import "bootstrap/wtf.html" as wtf \%\}
    
    # 在模板中需要写表单的地方生成表单
    \{\{ wtf.quick_form(form) \}\}
    
```

### 在view函数中使用 form对象
- 可参见本页上面的 auth.login视图


## 参考网址
> [Flask-Login文档在线阅读](https://flask-login.readthedocs.io/en/latest/)  
> [Flask-Login Github](https://github.com/maxcountryman/flask-login/)  