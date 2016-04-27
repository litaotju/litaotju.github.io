---
layout: post
title: "Python判断文件是否存在的方法"
description: ""
category: python
tags: 
   - python
---
{% include JB/setup %}

#假定在当前目下下存在这样的结构

    #1 -rwxrwxrwx  file
    #2 lrwxrwxrwx  link ->file
    #3 drwxrwxrwx  dir
    #4 lrwxrwxrwx  sym ->dir

在Python里，判断文件是否存在的方法有如下几种：

## os.path.exists(filename)
不论filename是文件夹或者文件或者链接，只要ls能够列出来的， 执行os.path.exists()测试，结果都为真。

## os.path.isfile(filename)
filename为 已经存在的(exists测试为真)文件名或者指向文件的链接时， os.path.isfile()返回真，否则返回false
所以对上述四个文件或者目录执行 isfile测试的结果是， #1 #2返回真，#3#4返回假

## os.path.isdir(filename)
当filename为已经存在的(exists测试为真)文件夹或者指向文件的链接是，os.path.isdir()返回真。
所以对上述四个文件或者目录执行 isdir测试的结果是， #3#4返回真， #1#2返回假





