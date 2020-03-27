---
layout: post
title: Fix ubuntu touch pad too sensitive
description: 
category: 
tags: 
---
{% include JB/setup %}

Actions Taken:

Backup the original:
/usr/share/X11/xorg.conf.d/50-synaptics.conf

<pre>
sudo vi /usr/share/X11/xorg.conf.d/50-synaptics.conf
</pre>

Add the sections to:

<pre>
Section "InputClass"
  Identifier "touchpad catchall"
  Driver "synaptics"
  MatchIsTouchpad "on"
  MatchDevicePath "/dev/input/event*"
  Option "FingerLow" "32"
  Option "FingerHigh" "35" 
EndSection
</pre>

Ref links:
>https://blog.laimbock.com/2014/11/23/howto-fix-a-too-sensitive-touchpad-on-linux/
>https://help.ubuntu.com/community/SynapticsTouchpad
