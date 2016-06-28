---
layout: post
title: python json dump 输出中文
description: 
category: python
tags: 
    - json
    - 输出中文
---
{% include JB/setup %}

在写爬虫时，使用python自带的json模块将网页中需要的信息输出保存到json文件中，发现json文件中的中文
格式全是类似于"\u5176\u5b83"的形式。可见该模块将输出的中文进行了 编码，将utf-8码直接变成了 ascii字符的形式。所以这些字符无法直接阅读。
要直接输出中文需要使用 json.dump()函数的 ensure_ascii=False选项。同时需要采用 codecs模块的open函数，指定输出文件的编码方式。
完整的代码片段如下。

```python
    # -*-coding:utf-8 -*-
    import json
    import codecs

    fobj = open("gaokao.json",'r')
    wfobj = codecs.open("formarted_gaokao.json", 'w', encoding="utf-8")

    universities = json.load(fobj)
    json.dump(universities, wfobj, indent=4, ensure_ascii=False)

    fobj.close()
    wfobj.close()
```

### 参考网址
> [使用 python 读写中文json](http://www.tuicool.com/articles/YBbAzi)  
> [python输出json时中文处理问题](http://blog.csdn.net/followingturing/article/details/8138365)  
> [python字符串编码详解](http://www.cnblogs.com/huxi/archive/2010/12/05/1897271.html)