---
layout: page
title: 不断进步的Blog
tagline: 我们的宗旨是，生命不息，折腾不止
---
{% include JB/setup %}

## 博文目录
<ul class="posts">
  {% for post in site.posts %}
    <li>
    <span>{{ post.date | date_to_string }}</span> &raquo; 
    <a href="{{ BASE_PATH }}{{ post.url }}">{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>
<br>
<br>
<br> 

 
***
>两个帮助的网页  

1. Read [Jekyll Quick Start](http://jekyllbootstrap.com/usage/jekyll-quick-start.html)

2. Complete usage and documentation available at: [Jekyll Bootstrap](http://jekyllbootstrap.com)
