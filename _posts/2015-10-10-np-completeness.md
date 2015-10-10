---
layout: post
title: "关于NP完整性问题"
description: 
category:  
tags: 
---
{% include JB/setup %}

## 证明问题Q的NP完整性的两个条件  
  NP的问题都针对性的是判定性问题。
    
* Q是NP问题，Nodeterministic Polynomial Decisionable
* Q与一个一直的NPC问题一样难，关键是找到一个多项式规约函数。

## 库克定理的内容  
SAT问题属于NP-Complete问题。SAT是第一个被证明的NP完整性问题。往后的NPC问题都是在其
基础上证明出来的。下图是NPC问题的证明历史脉络（存在不同的版本）。  

<img src ="/assets/pic/npc.jpg" align="center" alt="NPC问题的证明历史" style="max-width:100%;" />

## 与我们的联系
如果能证明一个问题是NPC问题，那么就能说明他很难解，基本上不存在着多项式时间解法，只能靠暴力破解的方式等来进行解决。
所以不用费力的去找快速的准确解，只能进行近似求解，*Approximation Algorithm*，然后使得解的精度尽可能近似于最优解。

## 近似解法的几个衡量标准
* 求解的时间要尽可能快，线性或者多项式时间。
* 近似程度 Approximation Ratio要小。

## 参考网址
[库克其人](http://blog.sciencenet.cn/blog-1225851-840719.html)