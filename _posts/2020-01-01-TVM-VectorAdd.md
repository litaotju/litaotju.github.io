---
layout: post
title: TVM-VectorAdd
description: 
category: TVM
tags: TVM AI Compiler DL Introduction
---
{% include JB/setup %}# TVM VectorAdd - Hello World of TVM

This doc is trying to decode what is happening when the tvm python api demoed by the following tutorial [tutorials/tensor_expr_get_started.py](https://github.com/litaotju/incubator-tvm/blob/master/tutorials/tensor_expr_get_started.py)

```python
import tvm
import numpy as np

tgt_host="llvm"
tgt="cuda"

# define the graph
n = tvm.var("n")
A = tvm.placeholder((n,), name='A')
B = tvm.placeholder((n,), name='B')
C = tvm.compute(A.shape, lambda i: A[i] + B[i], name="C")
print(type(C))

# compile the graph
s = tvm.create_schedule(C.op)
fadd = tvm.build(s, [A, B, C], tgt, target_host=tgt_host, name="myadd")

# Run the graph/function
ctx = tvm.context(tgt, 0)
n = 1024
a = tvm.nd.array(np.random.uniform(size=n).astype(A.dtype), ctx)
b = tvm.nd.array(np.random.uniform(size=n).astype(B.dtype), ctx)
c = tvm.nd.array(np.zeros(n, dtype=C.dtype), ctx)
fadd(a, b, c)

# check result with numpy computation  

tvm.testing.assert_allclose(c.asnumpy(), a.asnumpy() + b.asnumpy())

```

The tvm python API are exported from the [`python/tvm/__init__.py`](https://github.com/litaotju/incubator-tvm/blob/master/python/tvm/__init__.py), and you can see from there that, many of the APIs are defined in [pyhton/tvm/api.py](https://github.com/litaotju/incubator-tvm/blob/master/python/tvm/api.py),which is then lead to [python/tvm/_api_internal.py](https://github.com/litaotju/incubator-tvm/blob/master/python/tvm/_api_internal.py)

## 1. tvm.var

```
import tvm
n = tvm.var("n")
```
-> 
``` python
    #pythom/tvm/api.py
    ...
   return _api_internal._Var(name, dtype
```
-> 
```cpp
   //src/src/api_ir.cc
   TVM_REGISTER_API("_Var")
    .set_body_typed<VarExpr(std::string, Type)>([](std::string s, Type t) {
        return Variable::make(t, s);
    });
```
->
```
//tvm/runtime/registry.h

#define TVM_REGISTER_GLOBAL(OpName)                              \
  TVM_STR_CONCAT(TVM_FUNC_REG_VAR_DEF, __COUNTER__) =            \
  ::tvm::runtime::Registry::Register(OpName)

//include/tvm/api_registry.h
#define TVM_REGISTER_API(OpName) TVM_REGISTER_GLOBAL(OpName)
```

The registry is like the registry tech we mentioned in [last blog](http://litaotju.github.io/2019/12/29/Registry-tech/), can associate any function with any string name. And can get the function in from the string.

## 2. tvm.placeholder

```python
A = tvm.placeholder((n,), name='A')
```

```cpp
namespace tvm{
Tensor placeholder(Array<Expr> shape, Type dtype, std::string name) {
  return PlaceholderOpNode::make(name, shape, dtype).output(0);
}
}

TVM_REGISTER_API("_Placeholder")
.set_body_typed<Tensor(Array<Expr>, Type, std::string)>([](
  Array<Expr> shape, Type dtype, std::string name
) {
  return placeholder(shape, dtype, name);
});
```

## 3. tvm.compute

```python
C = tvm.compute(A.shape, lambda i: A[i] + B[i], name="C"
```
The following function is the defination of the `tvm.compute`, it accept shape, and python lambda, while returns a `tvm.Tensor`.


``` python
#python/tvm/api.py

def compute(shape, fcompute, name="compute", tag="", attrs=None):
    # Construct a new tensor by computing over the shape domain.  

    # The compute rule is result[axis] = fcompute(axis)  

    # Parameters  

    # ----------  

    # shape: Tuple of Expr  

    #     The shape of the tensor  

    # fcompute: lambda function of indices-> value  

    #     Specifies the input source expression  

    # name: str, optional  

    #     The name hint of the tensor  

    # tag: str, optional  

    #     Additional tag information about the compute.  

    # attrs: dict, optional  

    #     The additional auxiliary attributes about the compute.  

    # Returns  

    # -------  

    # tensor: Tensor  

    #     The created tensor  
    

    if _tag.TagScope.get_current() is not None:
        if tag != "":
            raise ValueError("nested tag is not allowed for now")
        tag = _tag.TagScope.get_current().tag
    shape = (shape,) if isinstance(shape, _expr.Expr) else shape
    # for python3

    shape = tuple([int(s) if isinstance(s, float) else s for s in shape])
    ndim = len(shape)
    code = fcompute.__code__

    out_ndim = ndim
    if code.co_argcount == 0:
        arg_names = ["i%d" % i for i in range(ndim)]
    else:
        arg_names = code.co_varnames[:code.co_argcount]
        out_ndim = code.co_argcount

    if out_ndim != len(arg_names):
        raise ValueError("fcompute do not match dimension, ndim=%d" % ndim)

    dim_var = [_IterVar((0, s), x, 0) for x, s in zip(arg_names, shape[:out_ndim])]
    body = fcompute(*[v.var for v in dim_var])

    if isinstance(body, _tensor.TensorIntrinCall):
        for i, s in enumerate(shape[out_ndim:]):
            var_name = "ax" + str(i)
            dim_var.append(_IterVar((0, s), var_name, 4))
        op_node = _api_internal._TensorComputeOp(name,
                                                 tag,
                                                 dim_var,
                                                 body.reduce_axis,
                                                 out_ndim,
                                                 body.intrin,
                                                 body.tensors,
                                                 body.regions,
                                                 body.scalar_inputs)
    else:
        if not isinstance(body, (list, tuple)):
            body = [body]
        body = convert(body)
        op_node = _api_internal._ComputeOp(
            name, tag, attrs, dim_var, body)

    num = op_node.num_outputs
    outputs = tuple(op_node.output(i) for i in range(num))
    return outputs[0] if num == 1 else outputs
```

Some keypoint observations:

1. The lambda input args are the index of output Tensor.
2. The lambda function is specifying how to compute value in each element specified by the `index`.

Here is how to specify convolution in this way, the complete code, see [tutorials/optimize/opt_conv_cuda.py](https://github.com/litaotju/incubator-tvm/blob/master/tutorials/optimize/opt_conv_cuda.py)

```python
# Create reduction variables
rc = tvm.reduce_axis((0, in_channel), name='rc')
ry = tvm.reduce_axis((0, kernel), name='ry')
rx = tvm.reduce_axis((0, kernel), name='rx')
# Compute the convolution
B = tvm.compute(
    (out_size, out_size, out_channel, batch),
    lambda yy, xx, ff, nn: tvm.sum(
        Apad[yy * stride + ry, xx * stride + rx, rc, nn] * W[ry, rx, rc, ff],
        axis=[ry, rx, rc]),
    name='B')
```

## 4. tvm.create_schedule

``` python
s = tvm.create_schedule(C.op)
```

```
TVM_REGISTER_API("_CreateSchedule")
.set_body_typed(create_schedule);

inline Schedule create_schedule(Array<Operation> ops) {
  return ScheduleNode::make(ops);
}
```

## 5. tvm.build
```
fadd = tvm.build(s, [A, B, C], tgt, target_host=tgt_host, name="myadd")
```
Source code, see [python/tvm/build_module.py:build](https://github.com/litaotju/incubator-tvm/blob/master/python/tvm/build_module.py), the function has be well documented.

The core api called by the `tvm.build` are 
1. `tvm.lower` 
2. `tvm._build_for_device` 
3. `tvm.codegen.build_module`
4. `tvm.import_module`

### 5.1 tvm.lower

Lower is transforming from the schedule node to lowering IRs, and performing optimiations.

```python

def lower(sch,
          args,
          name="default_function",
          binds=None,
          simple_mode=False):
    """Lowering step before build into target.

    Parameters
    ----------
    sch : tvm.schedule.Schedule
        The schedule to be built

    args : list of Buffer or Tensor or Var
        The argument lists to the function.

    name : str, optional
        The name of result function.

    binds : dict of :any:`Tensor` to :any:`Buffer`, optional
        Dictionary that maps the Tensor to Buffer which specified the data layout
        requirement of the function. By default, a new compact buffer is created
        for each tensor in the argument.

    simple_mode : bool, optional
        Whether only output simple and compact statement, this will skip
        LoopPartition, api wrapper generation and Unrolling.

    Returns
    -------
    f : LoweredFunc or Stmt
       The result function, if with_api_wrapper=False
       Then the Stmt before make api is returned.
    """
    cfg = current_build_config()
    add_lower_pass = cfg.add_lower_pass if cfg.add_lower_pass else []
    if cfg.dump_pass_ir:
        add_lower_pass = BuildConfig._dump_ir.decorate_custompass(add_lower_pass)
    lower_phase0 = [x[1] for x in add_lower_pass if x[0] == 0]
    lower_phase1 = [x[1] for x in add_lower_pass if x[0] == 1]
    lower_phase2 = [x[1] for x in add_lower_pass if x[0] == 2]
    lower_phase3 = [x[1] for x in add_lower_pass if x[0] > 2]

    # Phase 0

    if isinstance(sch, schedule.Schedule):
        stmt = form_body(sch)

    for f in lower_phase0:
        stmt = f(stmt)

    compact = ir_pass.VerifyCompactBuffer(stmt)
    binds, arg_list = get_binds(args, compact, binds)

    # Phase 1  

    stmt = ir_pass.RewriteForTensorCore(stmt, sch, binds)
    stmt = ir_pass.StorageFlatten(stmt, binds, 64, cfg.instrument_bound_checkers)
    stmt = ir_pass.CanonicalSimplify(stmt)
    for f in lower_phase1:
        stmt = f(stmt)

    # Phase 2  

    if not simple_mode:
        stmt = ir_pass.LoopPartition(stmt, cfg.partition_const_loop)
    if cfg.disable_vectorize:
        stmt = ir_pass.SkipVectorize(stmt)
    else:
        stmt = ir_pass.VectorizeLoop(stmt)
    stmt = ir_pass.InjectVirtualThread(stmt)
    stmt = ir_pass.InjectDoubleBuffer(stmt, cfg.double_buffer_split_loop)
    stmt = ir_pass.StorageRewrite(stmt)
    stmt = ir_pass.UnrollLoop(
        stmt,
        cfg.auto_unroll_max_step,
        cfg.auto_unroll_max_depth,
        cfg.auto_unroll_max_extent,
        cfg.unroll_explicit)
    for f in lower_phase2:
        stmt = f(stmt)

    # Phase 3

    stmt = ir_pass.Simplify(stmt)
    stmt = ir_pass.RemoveNoOp(stmt)
    if not cfg.disable_select_rewriting:
        stmt = ir_pass.RewriteUnsafeSelect(stmt)
    for f in lower_phase3:
        stmt = f(stmt)

    # Instrument BoundCheckers

    if cfg.instrument_bound_checkers:
        stmt = ir_pass.InstrumentBoundCheckers(stmt)
    if simple_mode:
        return stmt

    return ir_pass.MakeAPI(stmt, name, arg_list, 0, cfg.restricted_func)
```

### 5.2 tvm._build_for_device

See python/tvm/build_module.py:_build_for_device
Performinig some IR pass for device code.

### 5.3 tvm.codegen.build_module

See cpp source code `src/codegen/codegen.cc`.
The function signature is following.
```
runtime::Module Build(const Array<LoweredFunc>& funcs,
                      const std::string& target);
```

Different target has different build functions, for cuda, it's `cudagen.build_cuda`.

```
TVM_REGISTER_API("codegen.build_cuda")
.set_body_typed(BuildCUDA)
```
There are also `codegen.build_llvm`, `codegen.build_opengl`...

The `cudagen.build_cuda` relies on the `CodeGenCUDA` class to generate `cuda` code.
Then, if there is a registered function named `tvm_callback_cuda_compile`, use this registered callback, normally, use just use this callback to to
call nvcc from command line to compile.
If there is no registered function using this name, just use the `nvrtc` c++ APIs.

```
  if (const auto* f = Registry::Get("tvm_callback_cuda_compile")) {
    ptx = (*f)(code).operator std::string();
    // Dirty matching to check PTX vs cubin.
    // TODO(tqchen) more reliable checks
    if (ptx[0] != '/') fmt = "cubin";
  } else {
    ptx = NVRTCCompile(code, cg.need_include_path());
  }
  return CUDAModuleCreate(ptx, fmt, ExtractFuncInfo(funcs), code);
```

## TODO

- [P1] Why the Api function defined or registered by `TVM_REGISTER_API` can be automatically exported to `_api_internal.py`?
- [P1] How the python lambda function converted into a c++ function can be called by tvm ?
- [P0] What's the exact meanting and motivation for each IR pass in `tvm.lower`?

## Reference
- [https://docs.tvm.ai/dev/codebase_walkthrough.html#vector-add-example](https://docs.tvm.ai/dev/codebase_walkthrough.html#vector-add-example)
- [https://docs.tvm.ai/dev/runtime.html](https://docs.tvm.ai/dev/runtime.html)