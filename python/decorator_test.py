#!/bin/python
#Evan Widloski - 2015-09-16
#Example code demonstrating how decorators are used


#this is a function which changes a variable 'pos' by an amount 'delta'
def move(pos,delta):
    pos+=delta
    return pos

pos = 5
delta = 10

print move(pos,delta)
#the result is 15



#however, lets assume that we want this function to reject pos > 10
#we can use a wrapper function to modify the returned value of the move function
    

#wrapper to prevent pos from going above 10 - returns function bounds_check
def wrapper(func):
    def bounds_check(pos,delta):
        if pos + delta < 10:
            return func(pos,delta)
        else:
            return pos
    return bounds_check

#redefine 'move' as the wrapped version and call it
move = wrapper(move)
print move(pos,delta)
#the result is 5
    


#we can use a decorator - same thing as move=wrapper(move)
@wrapper
def move(pos,delta):
    pos+=delta
    return pos

print move(pos,delta)
#the result is 5




def decorator(test):
    print test
    def wrapper(func):
        def bounds_check(pos,delta):
            print test
            if pos + delta < 10:
                return func(pos,delta)
            else:
                return pos
        return bounds_check
    return wrapper


@decorator('doop')
def move(pos,delta):
    pos+=delta
    return pos

