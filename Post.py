# -*-coding:utf8 -*- #
'''本模块只支持Python3K
'''
import os
import sys
import codecs
import getopt
import datetime

def post(title, desc = '', cate = '',  tags = '', override = False):
    "博客头的模板"
    standard_head = ('---',
                     'layout: post' ,
                     'title: %s' % title,
                     'description: %s' % desc,
                     'category: %s' % cate,
                     'tags: %s' % tags,
                     '---',
                     '{% include JB/setup %}'
                     )
    cate = os.path.join("_posts", cate)
    if not os.path.exists(cate):
        os.mkdir(cate)
        
    format_time = datetime.datetime.now().strftime("%Y-%m-%d-")
    whole_title = format_time + title + ".md"
    filename = os.path.join(cate, whole_title)
    if os.path.exists(filename):
        print("Warning:Has same blog already")
        if not override:
            return None
    if filename:
        fobj = codecs.open(filename, 'w','utf8')
        print("Post: %s created successfully" % filename)
        fobj.write(os.linesep.join(standard_head))
        fobj.close()
        return filename
    
if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], 'hwt:c:', ['title=','desc=', 'category=', 'tags=', 'override'])
    title = ''
    desc = ''
    category =''
    tags = ''
    override = False
    for opt, value in opts:
        if opt =='-h':
            sys.stderr.write("\nUsage: Post.[py] [--title='your title'][--dese='ur '][--category='ur'][--tags='ur'][--override]\n\n")
            sys.exit(0)
        if opt =='--title' or opt=='-t':
            title = value
        if opt =='--desc':
            desc = value
        if opt =='--category' or opt == "-c":
            category = value
        if opt == '--tags':
            tags = [ tag.strip() for tag in value.strip().split() ]
        if opt == '--override' or opt == '-w':
            override = True
    if title == '':
        sys.exit(0)
    filename = post(title, desc, category, tags, override)
    if filename:
        os.system("code \"%s\"" % filename)
        sys.exit(0)
