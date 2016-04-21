---
layout: post
title: "How to use jekyll to build github.io blog"
description: ""
category: lessons
tags: []
---
{% include JB/setup %}

# Jekyll 是什么
Jekyll是一个渲染引擎，能够将html模板文件，markup文件，渲染成一个静态的网站所需的所有html页面。
Github pages使用了 Jekyll3.0进行渲染，只要建立相应的github仓库，并且按照Jekyll的要求建立该仓库的内容，github可以自动的将
你的仓库变成一个静态的博客网站。

# 你需要怎么做

## 安装jekyll
jekyll是一个ruby的gem包，所以你首先要做的是安装ruby和gem。请百度具体教程。
安装ruby和gem完成后，请输入如下指令：

    gem install jekyll
    
完成jekyll的安装。

## 下一个jekyll的模板
在github上有现成的jekyll模板，你只需要clone到本地，然后进行修改就可以搭建自己的最简单的博客了。
输入如下指令：

    git clone git@github.com:BlackrockDigital/startbootstrap-clean-blog-jekyll.git
    cd startbootstrap-clean-blog-jekyll

然后你的本地文件夹里面就有了一个 jekyll模板文件夹，运行：

    jekyll serve

打开浏览器，输入:
    
    localhost:4000

预览的你的jekyll网站。
在 "_post"文件夹下按照格式新建markdown文件。完成之后再次运行 <code>"jekyll serve"</code>
可以看到已经新增加了一个博文。


## 在github上新建自己的仓库
假如你的github的名字为"username",则在你自己的github上新建一个名为

    username.github.io
    
的仓库。


## 将本地的jekyll文件夹推送到github
执行以下指令：

    git remote add username git@github.com:username/username.github.io
    git push username master
    
    
## 网页访问博客

在浏览器中输入：username.github.io就可以访问你推送到git的博客了。

## 参考链接
>[jekyll介绍](http://jekyll.bootcss.com/)  
>[git远程操作详解-阮一峰的git教程](http://www.ruanyifeng.com/blog/2014/06/git_remote.html)

    
