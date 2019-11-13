#!/bin/python

def fibonacci(start=0):
    a = 0
    b = 1
    c = 0
    iteration = 0

    while iteration <= 5:
        if iteration >= start:
            yield c

        a = b
        b = c
        c = a + b

        iteration += 1

# get the 20th fibonacci number
# print(fibonacci(20).next())

# fib = fibonacci(10)

# # get the 10th fibonacci number
# print(fib.next())

# # get the 11th fibonacci number
# print(fib.next())

# # get the 12th - 15th number as list
# print([fib.next() for _ in range(4)])

