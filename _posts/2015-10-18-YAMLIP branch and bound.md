---
layout: post
title: "YAMLIP branch and bound"
description: 
category:  算法
tags: 
---
{% include JB/setup %}
YAMLIP包
matlab>help bnb

 bnb          General branch-and-bound scheme for conic programs
 
  bnb applies a branch-and-bound scheme to solve mixed integer
  conic programs (LP, QP, SOCP, SDP) and mixed integer geometric programs.
 
  bnb is never called by the user directly, but is called by
  YALMIP from SOLVESDP, by choosing the solver tag 'bnb' in sdpsettings.
 
  bnb is used if no other mixed integer solver is found, and
  is only useful for very small problems, due to its simple
  and naive implementation.
 
  The behaviour of bnb can be altered using the fields
  in the field 'bnb' in SDPSETTINGS
 
  bnb.branchrule   Deceides on what variable to branch
                    'max'     : Variable furthest away from being integer
                    'min'     : Variable closest to be being integer
                    'first'   : First variable (lowest variable index in YALMIP)
                    'last'    : Last variable (highest variable index in YALMIP)
                    'weight'  : See manual
 
  bnb.method       Branching strategy
                    'depth'   : Depth first
                    'breadth' : Breadth first
                    'best'    : Expand branch with lowest lower bound
                    'depthX'  : Depth until integer solution found, then X (e.g 'depthbest')
 
  solver           Solver for the relaxed problems (standard solver tag, see SDPSETTINGS)
 
  maxiter          Maximum number of nodes explored
 
  inttol           Tolerance for declaring a variable as integer
 
  feastol          Tolerance for declaring constraints as feasible
 
  gaptol           Exit when (upper bound-lower bound)/(1e-3+abs(lower bound)) < gaptol
 
  round            Round variables smaller than bnb.inttol
 
 
  See also solvesdp, binvar, intvar, binary, integer