---
layout: page
title: Index Page
tagline: 这一一个Tagline，可以写副标题之类的
---
{% include JB/setup %}
## 两个帮助的网页
1. Read [Jekyll Quick Start](http://jekyllbootstrap.com/usage/jekyll-quick-start.html)

2. Complete usage and documentation available at: [Jekyll Bootstrap](http://jekyllbootstrap.com)
  
## 删除Sample Posts的方法

This blog contains sample posts which help stage pages and blog data.
When you don't need the samples anymore just delete the `_posts/core-samples` folder.

    $ rm -rf _posts/core-samples

Here's a sample "posts list".


## 下面的博客的正文了
<ul class="posts">
  {% for post in site.posts %}
    <li><span>{{ post.date | date_to_string }}</span> &raquo; <a href="{{ BASE_PATH }}{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
</ul>


