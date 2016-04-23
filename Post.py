# -*-coding:utf8 -*- #
'''本模块只支持Python3K
'''
import os
import sys
import codecs
import getopt
import datetime

def mkpost(title, override = False):
    '给一个title的字符串，生成一个markdown文件表示'
    #获得当前时间,并转化成正确的格式
    format_time = datetime.datetime.now().strftime("%Y-%m-%d-")
    whole_title = format_time + title
    filename = "_posts\\%s.md" % whole_title 
    if os.path.exists(filename):
        print("Warning:Has same blog already")
        if not override:
            return None
    return filename

def post(title, desc = '', cate = '',  tags = '', override = False):
    "博客头的模板"
    standard_head = '''---\nlayout: %s\ntitle: "%s"\ndescription: %s\ncategory: %s \ntags: %s\n---\n{%% include JB/setup %%}'''\
                    % ('post', title, desc, cate, tags)
    filename = mkpost(title, override)
    if filename:
        fobj = codecs.open(filename, 'w','utf8')
        print("Post: %s created successfully" % filename)
        fobj.write(standard_head)
        fobj.close()
        return filename
    
if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], 'h', ['title=','desc=', 'category=', 'tags=', 'override'])
    title = ''
    desc = ''
    category =''
    tags = ''
    override = False
    for opt, value in opts:
        if opt =='-h':
            sys.stderr.write("\nUsage: Post.[py] [--title='your title'][--dese='ur '][--category='ur'][--tags='ur'][--override]\n\n")
            sys.exit(0)
        if opt =='--title':
            title = value
        if opt =='--desc':
            desc = value
        if opt =='--category':
            category = value
        if opt == '--tags':
            tags = [ tag.strip() for tag in value.strip().split() ]
        if opt == '--override':
            override = True
    if title == '':
        sys.exit(0)
    filename = post(title, desc, category, tags, override)
    if filename:
        os.system("code \"%s\"" % filename)
        sys.exit(0)
