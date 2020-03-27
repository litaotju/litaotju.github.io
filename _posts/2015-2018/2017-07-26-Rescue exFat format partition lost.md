---
layout: post
title: Rescue exFat format partition lost
description: 
category: 
tags: 
---
{% include JB/setup %}

After tried a lot of methods, the simplest and most powerful way for me is just the
windows native command.

<pre>
    chkdsk :x /f
</pre>

Here "x" is the label for your partition, for example, "c" or "d" or "e"... 
