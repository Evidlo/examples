#!/bin/env python
## Evan Widloski - 2017-04-19
## Crappy CAS

# example
# >>> x = symbol('x')
# >>> y = symbol('y')
# >>> ans = x + 2*y - 3*x
# >>> ans
# x + (y * 2) + (-1 * (x * 3))
# >>> ans.eval(x=3, y=4)
# 2


class symbol(object):

    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return str(self.val)

    def __add__(self, other):
        return add(self, other)
    __radd__ = __add__

    def __mul__(self, other):
        return mul(self, other)
    __rmul__ = __mul__

    def __sub__(self, other):
        return add(self, mul(-1, other))
    __rsub__ = __sub__

    def eval(self, **kwargs):
        # return int, evaluated symbol, unevaluated symbol
        if type(self.val) is int:
            return self.val
        elif self.val in kwargs:
            return kwargs[self.val]
        else:
            return self

class operation(symbol):

    def __init__(self, a, b):
        if type(a) is int:
            self.a = symbol(a)
        else:
            self.a = a
        if type(b) is int:
            self.b = symbol(b)
        else:
            self.b = b

class add(operation):

    def __repr__(self):
        return "{} + {}".format(self.a, self.b)

    def eval(self, **kwargs):
        return self.a.eval(**kwargs) + self.b.eval(**kwargs)

class mul(operation):

    def __repr__(self):
        return "({} * {})".format(self.a, self.b)

    def eval(self, **kwargs):
        return self.a.eval(**kwargs) * self.b.eval(**kwargs)
