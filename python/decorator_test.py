#!/bin/python
#Evan Widloski - 2015-09-16
#Example code demonstrating how decorators are used


# this is a function which changes a variable 'pos' by an amount 'delta'
def move(pos,delta):
    pos+=delta
    return pos

pos = 5
delta = 10
print move(pos,delta)
# the result is 15

#------------- wrapping functions --------------------

# however, lets assume that we want this function to ignore requests to increase `pos`
# to more than 10
# we can use a wrapper function to add extra logic without modifying `move()`

# wrapper to prevent pos from going above 10
def wrapper(func):
    def bounds_check(pos,delta):
        if pos + delta <= 10:
            return func(pos,delta) #return the function passed to `wrapper` (`move` in this case)
        else:
            return pos
    return bounds_check

# redefine `move` as the wrapped version and call it
move = wrapper(move)
print move(pos,delta)
# the result is 5

#-------------- using decorators -----------------------

# we can use a decorator - same thing as move=wrapper(move)
# the argument to wrapper is the function on the line below it
@wrapper
def move(pos,delta):
    pos+=delta
    return pos

print move(pos,delta)
# the result is 5

#-------------- arguments to decorators -----------------

def bounds_decorator(wrapper):
    def wrapper1(func):
        def bounds_check(pos,delta):
            print test
            if pos + delta < 10:
                return func(pos,delta)
            else:
                return pos
        return bounds_check
    def wrapper2(func):
        def other_action(pos,delta):
            return 'doop'
        return other_action

    if wrapper == 'wrapper1':
        return wrapper1
    if wrapper == 'wrapper2':
        return wrapper2

@decorator('wrapper1')    # <--- this is equivalent to `move = wrapper(move)`
def move(pos,delta):      # you can pass arguments to the decorator
    pos+=delta            # and perform logic before returning `wrapper`
    return pos
# returns 5


@decorator('wrapper2')
def move(pos,delta):
    pos+=delta
    return pos
# returns 'doop'
