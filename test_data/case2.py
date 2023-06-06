class B():
    def __init__(self) -> None:
        pass

class A(B):
    def __init__(self) -> None:
        pass
    
    def method(a,b):
        c = a + b
        return c
    
    def method2(self,g,cb):
        o = self.method(g,cb)
        return o

o = A()


def func2():
    def func1():
        a = 3
        b = 4
        c =4
        g = a+ 3
        d = b +c + a+ 5
        f =11
        o = g+d
        return 0
    a = 3
    b = 4
    c =4
    g = a+ 3
    d = b +c + a+ 5
    f =11
    o = g+d
    return 0

    
def func2():
    def func1():
        a = 3
        b = 4
        c =4
        g = a+ 3
        d = b +c + a+ 5
        f =11
        o = g+d
        return 0
    a = 3
    b = 4
    c =4
    g = a+ 3
    d = b +c + a+ 5
    f =11
    o = g+d
    return 0


t = a *3
gaba = a+4
for i in range(1):
    for j in range( a + b ):
        print(gaba)