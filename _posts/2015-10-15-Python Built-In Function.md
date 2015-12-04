---
layout: post
title: "Python Built-In Function"
description: 
category:  python
tags: 
---
{% include JB/setup %}
## Python的内建模块 %Python_Home%/lib
>getopt.py   

getopt.getopt(sys.argv[1:], shortopt, longopt = '')  
主要用来处理命令行参数，以下是这个函数的说明和用法

	```
	getopt(args, options[, long_options]) -> opts, args
    Parses command line options and parameter list.  args is the
    argument list to be parsed, without the leading reference to the
    running program.  Typically, this means "sys.argv[1:]".  shortopts
    is the string of option letters that the script wants to
    recognize, with options that require an argument followed by a
    colon (i.e., the same format that Unix getopt() uses).  If
    specified, longopts is a list of strings with the names of the
    long options which should be supported.  The leading '--'
    characters should not be included in the option name.  Options
    which require an argument should be followed by an equal sign
    ('=').
    The return value consists of two elements: the first is a list of
    (option, value) pairs; the second is the list of program arguments
    left after the option list was stripped (this is a trailing slice
    of the first argument).  Each option-and-value pair returned has
    the option as its first element, prefixed with a hyphen (e.g.,
    '-x'), and the option argument as its second element, or an empty
    string if the option has no argument.  The options occur in the
    list in the same order in which they were found, thus allowing
    multiple occurrences.  Long and short options may be mixed.

    ```
	
函数的主要内容如下所示。
<pre><code>
def getopt(args, shortopts, longopts = []):


    opts = []
    if type(longopts) == type(""):
        longopts = [longopts]
    else:
        longopts = list(longopts)
    while args and args[0].startswith('-') and args[0] != '-':
        if args[0] == '--':
            args = args[1:]
            break
        if args[0].startswith('--'):
            opts, args = do_longs(opts, args[0][2:], longopts, args[1:])
        else:
            opts, args = do_shorts(opts, args[0][1:], shortopts, args[1:])

    return opts, args
	
if __name__ == '__main__':
    import sys
    print getopt(sys.argv[1:], "a:b", ["alpha=", "beta"])
	# 上面代码的意思是，指定命令行的参数有['a','b','alpha','beta']
	# 如果说sys.argv中出现了 -a -b --alpha --beta等选项，这个函数会分别解析每一个选项
	# 对于短选项，如果后面加“：”表明在使用这个选项时后面必须加参数，
	# 对于长选项，如果后面加“=”，表明在使用这个选项时后面必须加参数。
	# 例如当命令行sys.argv[1:]的输入为 "-a arga -b --alpha argAlpha --beta"时能够正确的识别每一个选项，参数对
	# 返回 [('a','arga'),('b',),('alpha','argAlpha'),('beta',)], []
</code></pre>
