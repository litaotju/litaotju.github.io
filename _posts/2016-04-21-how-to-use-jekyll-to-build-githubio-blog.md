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

## 已知的问题和Jekyll的约束
在 _post文件文件夹下新建博客的.md文件时：文件名的形式必须是：

    %Y-%m-%d-Ascii codenames.md

注意，这里的文件可以和文件内部的标题不一致，但是一定要是可以用 ascii字符集标识的字符，
如果含有中文，在最后生成的博客网站中。**这一页将不能访问**。所以想要生成中文的博客的方法是：**即使title是中文的，文件名仍然需要变成英文。**

## 参考链接
>[jekyll介绍](http://jekyll.bootcss.com/)  
>[git远程操作详解-阮一峰的git教程](http://www.ruanyifeng.com/blog/2014/06/git_remote.html)

    
