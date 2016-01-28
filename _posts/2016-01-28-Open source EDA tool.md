---
layout: post
title: "Open source EDA tool"
description: 
category:  
tags: 
---
{% include JB/setup %}

#EDA工具的开发是一个有挑战性的工作
数字设计越来越需要团队的合作和先进的EDA工具，然而EDA工具的开发是一个有挑战的工作。学术界对于EDA的前沿研究与商业工具不同
学术上需要有前瞻性，点子要新，方法要好。不需要追求产品的实用和可靠，也不追求软件的易用性。

#现有的数字电路开源工具

* [VTR](http://code.google.com/p/vtr-verilog-to-routing)
* Yosys
* rapidSmith

#VTR框架
VTR(Verilog-to-Routing)是一个用于 FPGA架构设计和新型布局布线算法研究的框架，其中包含 ODIN II, ABC, VPR三个工具。

VTR Readme文件中的介绍：

This archive contains a free academic framework, called Verilog-to-Routing 
(VTR), that you can use to explore future FPGAs and CAD algorithms for FPGAs.  
This framework includes benchmark circuits (in Verilog), example FPGA 
architectures, and a flow that maps a set of benchmark circuits to the FPGA 
architecture of your choosing.

==============================================================================
Contents of the archive:

Tools: 

	ODIN II: An open-source Verilog elaborator

	ABC: An open-source logic synthesis tool modified to: 1) use the new 
	FPGA wiremap algorithm 2) not use the readline libraries

	VPR: An academic FPGA packing, placement, and routing tool

Libraries:

	libarchfpga: Library used by ODIN II and VPR.  This library reads an FPGA 
	architecture description file

Other:

	vtr_flow: Run the vtr flow on a set of Verilog benchmarks to a set of 
	FPGA architectures. Measures quality metrics from the output of those 
	experiments. [Optional] For regression tests, also compares with golden 
	results (with an error tolerance for algorithmic noise).

	run_quick_test.pl: Script that checks if the tools in this archive were 
	properly built.

	quick_test: Used by run_quick_test.pl to check build

===============================================================================

ODIN II 是一个Verilog前端工具， 可以解析verilog，输出blif网表。可以选择输出中间信息，比如dot格式的AST(抽象语法树)， 以及网表的 Graph。

ABC 是 伯克利大学开发的一款综合工具。

VPR 是一款FPGA布局布线工具。


#Yosys
Yosys使用C++语言开发。

yosys -- Yosys Open SYnthesis Suite
===================================

This is a framework for RTL synthesis tools. It currently has
extensive Verilog-2005 support and provides a basic set of
synthesis algorithms for various application domains.

Yosys can be adapted to perform any synthesis job by combining
the existing passes (algorithms) using synthesis scripts and
adding additional passes as needed by extending the yosys C++
code base.

Yosys is free software licensed under the ISC license (a GPL
compatible license that is similar in terms to the MIT license
or the 2-clause BSD license).


Web Site
========

More information and documentation can be found on the Yosys web site:

	http://www.clifford.at/yosys/

#rapidSmith

一款Java所写的针对Xilinx FPGA的，基于 xdl语言的 FPGA CAD工具。

RapidSmith is a research-based FPGA CAD tool written in Java for modern Xilinx
FPGAs. Based on XDL, its objective is to serve as a rapid prototyping platform
for research ideas and algorithms relating to low level FPGA CAD tools.



