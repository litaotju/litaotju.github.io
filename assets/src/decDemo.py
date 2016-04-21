def A(func):
    def __call():
        print "This is a decorator call"
        return func()
    return __call()
@A
def x():
    print "This is a X func()"

@A
def y():
    print "This is a Y func()"
    
x()
y()

