---
layout: post
title: Flask开发之Memcached
description: 
category: Web Dev
tags: 
---
{% include JB/setup %}

# 介绍和基本使用

Memcached是一个分布式缓存系统，可以提高动态网站的访问速率，因为服务器将经常访问的页面或者需要从数据库中提取的在第一次访问时计算好，然后以键值对的形式放到内存之中。之后服务器端根据用户的请求，判断所需的数据是否已经在内存中，如果在直接从内存中将数据返回。避免了再次计算，提升了服务器的响应速度。

在Flask中使用缓存可以直接使用　Wekzeug自带的缓存类，使用如下的类似代码片段来进行缓存的存和取。

```python
    fromo werkzeug.contrib.cache import　MemcachedCache
    cache = MemcachedCache(["localhost:11211"])
    #
    #设置过期时间为６０秒
    timeout_seconds = 60
    cache.set('key','value',timeout = timeout_seconds)
    
    #从缓存中取　‘key’
    value = cache.get('key')
    assert(value=='value')
```

# Ubuntu环境下Memcached安装

1.安装memcached

```shell
    # memcached依赖与libevent
    sudo apt-get install libevent
    sudo apt-get install memcached libmemcached-dev
```

2.安装memcached python客户端

```shell
    #如果没有安装　libpython-dev python的开发库可能无法安装　pylibmc所以可以使用下面的方式安装　
    #如果是python2则使用　sudo apt-get install libpython-dev
    sudo apt-get install libpython3-dev
    sudo pip install pylibmc
```

# 参考网址  
[Flask-Cache](http://dormousehole.readthedocs.io/en/latest/patterns/caching.html)  
[Memcached.org](https://memcached.org/)

