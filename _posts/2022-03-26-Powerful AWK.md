---
layout: post
title: Powerful AWK
description: 
category: 
tags: 
---
{% include JB/setup %}

AWK is a useful tools to process the text files, and it use a AWK language program to compose complex and useful actions on the text.

These actions may be able to be complished by other gnu tools too, but by learning one tool and the language, it gives you more flexiable ability by learning and knowing little about the cmd line options.

# Some examples
## Slice a file

* Print all the lines after a match

    `$ awk '/pattern/,0' file`

* Print all the lines between two matches (inclusive)

    `$ awk '/patternA/,/patternB/' file`

* Print all the lines before a match

    `$ awk '{print};/pattern/{exit}' file`

* Print all the lines between line number M, and N

    `$ awk 'NR > 5 && NR < 10 {print}' file `

* Print all lines w/o a pattern

    `$ awk '!/pattern/' file `

* Print lines w/h fields more than X

    `$ awk 'NF > 10' file`j

* Delete all non empty lines

    `$ awk NF file`

## Print more information

* print line with a number prefix

    `$ awk '{print NR ":" $0}' `


* Double spacing

    `$ awk '{print $0 ORS}'`


## Statistics

* count all the lines with a pattern

    `$ awk 'BEGIN{x=0};/pattern/{x++}; END{print x}`

# Reference

1. awk oneliners: https://catonmat.net/wp-content/uploads/2008/09/awk1line.txt
2. awesome awk: https://github.com/freznicek/awesome-awk
