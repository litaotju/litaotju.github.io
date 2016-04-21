---
layout: post
title: "Android Activity"
description: 
category:  offer
tags: 
---
{% include JB/setup %}

## 关于屏幕方向
一定要写在 
< activity >标签里面啊。。。

不要写在  < application >标签里面

不要写在  < application >标签里面！

不要写在  < application >标签里面！！

不要写在  < application >标签里面！！！

不要写在  < application >标签里面！！！！


就像这样

 <code>
    < activity <br>
            android:name=".CameraActivity"  <br>
            android:label="@string/app_name"  <br>
            android:screenOrientation="landscape" <br>
            android:configChanges="keyboardHidden|orientation"      ><br>
 </code>
			
千万不要写成这样  

<code>    
    < application <br> 
        android:allowBackup="false"<br>
        android:icon="@drawable/ic_launcher"<br>
        android:label="@string/app_name"  <br>
        android:theme="@android:style/Theme.NoTitleBar.Fullscreen"<br>
		android:screenOrientation="landscape"   <br>
		android:configChanges="keyboardHidden|orientation"		><br>
</code>