def A(func):
    def __call(*args, **kwds):
        print "This is a decorator call with paras"
        return func(*args, **kwds)
    return __call

@A
def x(a, b):
   print "Sum of %d and %d is: %d" %(a, b, a+b)

x(1,2)

