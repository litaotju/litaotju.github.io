---
layout: post
title: "Python2 str and unicode err"
description: 
category:  python
tags: 
---
{% include JB/setup %}

使用Py2最大的不爽的一点就是，在文件写入带有非asii码字符时总是容易出错。一会儿又需要调用codecs模块啦，
一会儿又是 str.decode() 着的 unicode.encode()方法了。 什么时候调用 decode 什么时候调用 encode总是搞混。
而且一个最大的麻烦就是，怎么知道一个对象是str还是unicode对象呢？

设想一个场景，从命令行传递 参数给 python script.py arg0 arg1 这种格式，传递给脚本的内部的 sys.argv list
里面的对象到底是 str还是unicode? 每一个需不需要编解码？ 是否要先判断类型再进行确定编解码操作？
这样完全违背了Python的精神啊。。。

妈蛋，为了让自动生成的博客标题中 也就是上面的 title field能够支持中文。也是折腾了半天，最后终于在被 str和unicode烦够了之后走向了
Python3K的怀抱。。以后写 print 都需要加括号了！！
