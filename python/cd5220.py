#!/usr/bin/env python
## Evan Widloski - 2016-12-21
## Writing patterns to a CD5220 display


import serial
import time

move_left = '08'
move_right = '09'
move_pos = '1B6C%02x%02x'
reset = '0C'
full_bar = 'DB'
half_bar_l = 'DD'
half_bar_r = 'DE'
blank = '00'

tick_time = .01

arduino = serial.Serial('/dev/ttyUSB0', 9600)

# write hex string
def write(hex):
    arduino.write(bytearray.fromhex(hex))


def build():
    for x in range(1, 21):
        write(move_pos % (x, 1))
        write(half_bar_l)
        write(move_pos % (x, 2))
        write(half_bar_l)

        time.sleep(tick_time)

        write(move_pos % (x, 1))
        write(full_bar)
        write(move_pos % (x, 2))
        write(full_bar)

        time.sleep(tick_time)

    for x in reversed(range(1, 21)):
        write(move_pos % (x, 1))
        write(half_bar_l)
        write(move_pos % (x, 2))
        write(half_bar_l)

        time.sleep(tick_time)

        write(move_pos % (x, 1))
        write(blank)
        write(move_pos % (x, 2))
        write(blank)

        time.sleep(tick_time)


def knight_rider():
    for x in range(1, 21):

        write(move_pos % (x - 1, 1))
        write(blank)
        write(move_pos % (x - 1, 2))
        write(blank)

        write(move_pos % (x, 1))
        write(half_bar_l)
        write(move_pos % (x, 2))
        write(half_bar_l)

        time.sleep(tick_time)

        write(move_pos % (x, 1))
        write(full_bar)
        write(move_pos % (x, 2))
        write(full_bar)

        time.sleep(tick_time)

        write(move_pos % (x, 1))
        write(half_bar_r)
        write(move_pos % (x, 2))
        write(half_bar_r)

        time.sleep(tick_time)

    for x in reversed(range(1, 21)):
        write(move_pos % (x + 1, 1))
        write(blank)
        write(move_pos % (x + 1, 2))
        write(blank)

        write(move_pos % (x, 1))
        write(half_bar_r)
        write(move_pos % (x, 2))
        write(half_bar_r)

        time.sleep(tick_time)

        write(move_pos % (x, 1))
        write(full_bar)
        write(move_pos % (x, 2))
        write(full_bar)

        time.sleep(tick_time)

        write(move_pos % (x, 1))
        write(half_bar_l)
        write(move_pos % (x, 2))
        write(half_bar_l)

        time.sleep(tick_time)

write(reset)


while True:
    knight_rider()
    # build()
