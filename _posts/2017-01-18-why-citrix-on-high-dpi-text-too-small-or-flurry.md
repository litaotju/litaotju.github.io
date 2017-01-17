---
layout: post
title: "Why Citrix on High DPI text too small or Flurry"
description: ""
category: 
tags: []
---
{% include JB/setup %}


Citrix Reciewer在我的新电脑上面的显示时。如果disable掉本地windows系\_的 dpi scaling，则打开之后服务器里面的文字特别小。如果不disable windows系统的 dpi scaling，则显示的客户端界面太模糊。
调研之后在citrix的官方论坛上，发现如下的帖子：

    https://support.citrix.com/article/CTX201696

该帖子的最后一段，解释了这个问题，对于DPI scale的工作原理给了一定的解释：

System to scale the application as appropriate to the client’s DPI settings. This means that the receiver can behave differently on different versions of Windows. In general, what happens when the DPI is increased windows will report a lower resolution than the actual resolution to the receiver, when this occurs this will result in text and other items in the session to be appropriately sized but that text and graphics can appear fuzzy due to the scaling of the graphics. The alternative would be to ignore client DPI settings and send the full resolution which would result in extremely small text and items.

同时，解释DPI的另外两篇文章链接如下，可供参考：

 https://blogs.msdn.microsoft.com/patricka/2010/04/15/why-does-a-high-dpi-setting-make-my-application-look-fuzzy-and-have-clipped-text/

 https://discussions.citrix.com/topic/383853-citrix-windows-dpi-bad-user-experience/

