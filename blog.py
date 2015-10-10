# -*-coding:utf8 -*- #
import os
import sys
import datetime
import traceback
def blog(title):
    '给一个title的字符串，生成一个markdown文件表示'
    #获得当前时间,并转化成正确的格式
    format_time = datetime.datetime.now().strftime("%Y-%m-%d-")
    whole_title = format_time + title
    filename = "_posts\\%s.md" % whole_title 
    if os.path.exists(filename):
        print "Warning:Has same blog already"
##        override = True if raw_input("Override old one(y/n)?:")in 'yY' else False
##        if not override:
##            print "No file been created"
##            sys.exit()
        sys.exit()
    try:
        blog_file = open(filename, 'w')
    except Exception,e:
        print e
        traceback.print_exc()
    blog_file.write('''---
layout: post
title: "%s"
description: 
category:
tags: 
---
{%% include JB/setup %%}
''' % title)
    print "%s created successfully" % filename
    blog_file.close()
    return filename

if __name__ == "__main__":
    title = raw_input("plz enter blog_title:")
    filename = blog(title)
    os.system("code \"%s\"" % filename)
    sys.exit()
