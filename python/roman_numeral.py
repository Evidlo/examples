#!/usr/bin/env python

numerals = [
    ('M', 1000)
    ('D', 500)
    ('C', 100)
    ('L', 50)
    ('X', 10)
    ('V', 5)
    ('I', 1)
]

def parse(r: str):
    i = 0
    total = 0

    for n, val in numerals:
        while r[i] == n:
            total += val
            i += 1
            if i == len(r):
                break
