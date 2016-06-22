---
layout: post
title: Flask 开发之 session
description: 
category: flask
tags: 
---
{% include JB/setup %}

# HTTP无状态，cookie， session
## 无状态
由于HTTP协议本身是无状态的，也就是说服务器只接受客户端的HTTP request，然后返回一个HTTP response。
这种无状态有好处也有坏处，好处就是简化了服务器端的功能，就是接受客户端请求然后返回一个响应。在web开始的时候，由于只需要返回静态类型的网页，所以这种设计是能够满足要求的。
但是随着web的发展，这种无状态的设计不能完成一些新出现的需求。如果全是无状态的设计，那么服务器和客户端之间的每一次通信就没有上下文信息。服务器只能对每一个请求都做出完全一样的响应。
同时， 比如用户要登陆一个网站，那么可能每一次打开浏览器都需要输入用户名和密码，然后通过HTTP的post协议发送这些信息给服务器。 等用户关闭了浏览器，再次需要登陆同一个网站的时候，仍然需要
再次输入用户名和密码。想一想，**每一次都需要输入用户名和密码这是多么蛋疼一件事**。

## cookies 就是键值对
为了解决 服务器 和客户端通信的上下文问题，有一个机智的家伙（也记不清是谁了）发明了一种叫做 cookie的技术，cookie就是服务器存储在客户端浏览器的一组键值对。现代的服务器都支持cookies.

cookies的工作方式是，客户端首次进入一个网址时，服务器根据其请求信息判断该客户端本地没有cookies，服务器返回正常的response,然而在response的 header中加入类似于：
```Set Cookies: keyA:valueA,keyB:valueB;```这样的信息，客户端浏览器收到该信息之后，将这一组键值对存储到本地中。以后再次登陆同一个网址时，在request header中发送cookies的键值对。
浏览器在request header中发现键值对之后，就知道该浏览器之前也访问过本网站，然后就可以根据这些键值对的信息做出个性化的响应。当然这些响应中又可以包含新cookies设置的信息等。这样每一次
从浏览器都服务器通信都在 header中夹带cookies的方法，完成了客户端都浏览器的上下文通信。 **使用cookies的方式，终于可以做到一次登陆再无忧愁啦。**

## session
session同样是为了解决服务器无法知道 在本次请求之前 客户端之前和服务器的通信情况的一种解决方法。 
session也是服务器将一部分信息存储在浏览器端，然后浏览器再次请求时携带这一部分信息供服务器查询。
session的实现方式有好几种，只要能起到将所需信息在第二次之后的请求中发送给服务器的功能就可以了。 session的实现方式中有一种是采用 cookies的方式。
在flask中， **session可以认为是存储在cookies中的 键为 "session"的一个加密字符串， 然后这个字符串本身又是一个 键值对。**

## 复杂一点的主题
采用cookies和session来完成 客户端服务器的上下文通信 不只是前面所说的那么简单，为了实现一些更丰富的功能。 cookies的属性还包含有 路径，过期时间等。
路径是为了判断 是由服务器端的哪一个 url 设置了 该cookies， 对于一个复杂的网站或者cookies中信息比较多时，可以减少传递不必要的信息。
过期时间是为了一定的安全性着想，默认情况下，关闭浏览器之后cookies即过期，也就是cookies是存储在客户端内存中的，但是可以设置过期时间为想要的时间，比如一个月，一年等，这样浏览器接受到
cookies之后，会将cookies存储在硬盘文件系统中。下次打开浏览器还可以接着读取这部分信息。

# Flask 使用session 代码片段
在flask中使用session的前提是给app指定了一个 secret_key属性，可以通过配置文件来设置此属性。
flask中session是一个全局对象，就像request一样，每一个请求的上下文中都有一个 session 全局对象。使用的方式如下：

```python

from flask import Flask, session, redirect, url_for, escape, request

app = Flask(__name__)

@app.route('/')
def index():
    # 判断本次请求的session中是否包含有 'username'属性
    if 'username' in session:
        # 如果有，从session中读取该属性
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        ## 将　‘username’属性放入 session中， 在本次request返回 response的时候，服务器发送了将 
        ## session放到 cookies的指令，将session存储到客户端浏览器
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # 如果会话中有用户名就删除它。
    # 同时从客户端浏览器中删除 session的 name属性
    session.pop('username', None)
    return redirect(url_for('index'))

# 设置密钥，复杂一点：
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

```
这里用到的 escape() 是用来转义的。如果不使用模板引擎就可以像上例 一样使用这个函数来转义。


### 参考链接
> [Flask说明手册-- 会话](http://dormousehole.readthedocs.io/en/latest/quickstart.html#sessions)