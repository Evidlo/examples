#!/bin/env python3
# Evan Widloski - 2017-11-27
# Read Agilent 34405A

import time

with open('/dev/usbtmc0', 'wb+') as dev:
    while True:
        dev.write('READ?')
        print(dev.read(16))
        time.sleep(.1)
