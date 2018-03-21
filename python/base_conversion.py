#!/bin/env python
## Convert from base10 to another
from math import log

def convert_base(num, base):
    if num == 0:
        return '0'
    elif num < 0:
        raise "Negative input"
    result = ''
    for exp in range(0, int(log(num)/log(base)) + 1):
        result = str(int((num % base**(exp + 1)) / base**exp)) + result

    return result
