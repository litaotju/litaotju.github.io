---
layout: post
title: "Android Activity"
description: 
category:  
tags: 
---
{% include JB/setup %}

## 关于屏幕方向
一定要写在 
<activity>标签里面啊。。。整死爹了。
不要写在  <application>标签
不要写在  <application>标签！
不要写在  <application>标签！！
不要写在  <application>标签！！！
不要写在  <application>标签！！！！


就像这样


 <activity
            android:name=".CameraActivity"
            android:label="@string/app_name"
            android:screenOrientation="landscape" 
            android:configChanges="keyboardHidden|orientation">
			
千万不要写成这样


    <application
        android:allowBackup="false"
        android:icon="@drawable/ic_launcher"
        android:label="@string/app_name"
        android:theme="@android:style/Theme.NoTitleBar.Fullscreen" 
		android:screenOrientation="landscape" 
		android:configChanges="keyboardHidden|orientation"		>