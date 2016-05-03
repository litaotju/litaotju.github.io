---
layout: post
title: multi python version on windows
description: 
category: python 
tags: 
    - python setup
---
{% include JB/setup %}

在windows上需要存在多个python版本时，比如python2和python3同时存在，假定python2和3的安装目录分别为：
C:\Python27和 C:\Python35。设置windows的步骤如下：

## 设置path环境变量：
假定你想要的默认的python版本为python27，将```C:\Python27;C:\Python27\Scripts; C:\Python35;C:\Python35\Scripts;```加入环境变量。如果要python3设为默认版本，则
将Python35开头的路径加在前面；
将python35路径下的 python.exe 和pythonw.exe**复制**并改名为 python3.exe和pythonw3.exe，注意使用复制是为了，防止有的模块需要直接调用 python.exe文件名，防止出错。 

## pip和virtual
将C:\Python35\Script文件夹下的 pip 和virtualenv直接改名为 pip3和 virtualenv3，并不好使，直接改名会报错 "Fatal error in launcher: Unable to create process using “”"。
参考网址[stackoverflow上的问答](http://stackoverflow.com/questions/24627525/fatal-error-in-launcher-unable-to-create-process-using-c-program-files-x86)
可以采用 python3 -m pip install 和 python3 -m virtualenv XXXX 来代替直接执行 pip和virutal 不会出错。
所以在 C:\Python35\Script 下新建两个python脚本，将 pip3 XXX 转义成 python3 -m pip XXX,  将 virtualenv3 xxx转义成 python -m virtualenv xxx.两个文件的代码如下：

pip3.py

    import sys
    import subprocess
    print(" ".join(sys.argv))
    cmd = "python3 -m pip " + " ".join(sys.argv[1:])
    obj = subprocess.Popen(cmd)
    obj.wait()

virtualenv3.py

    import sys
    import subprocess
    print(" ".join(sys.argv))
    cmd = "python3 -m pip " + " ".join(sys.argv[1:])
    obj = subprocess.Popen(cmd)
    obj.wait()

利用 subprocess模块的 Popen对象来执行子进程，同时默认将stdin和stdout等定位在当前是的窗口中。