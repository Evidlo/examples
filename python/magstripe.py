#!/bin/env python3
## Evan Widloski - 2017-01-06
## Asynchronous magstripe reader example
## Requires root and >= python 3.5

# Much taken from: http://python-evdev.readthedocs.io/en/latest/tutorial.html#reading-events-from-multiple-devices-using-asyncio

import asyncio, evdev, json, os

# MSR100 reader vendor/product ids
vendor = 0xc216
product = 0x0180

card_record = './cards.json'

# find card reader from vendor and product ids
try:
    devices = [evdev.InputDevice(device) for device in evdev.list_devices()]
    card_reader = next(device for device in devices
                if device.info.vendor == vendor and device.info.product == product)
except StopIteration:
    print('Device not found: productID: {0}, vendorID: {1}'.format(hex(vendor), hex(product)))
    for device in devices:
        device.close()
    quit()

# take full control of reader (requires root)
card_reader.grab()

print('Connected to device: productID: {0}, vendorID: {1}'.format(hex(vendor), hex(product)))

swiped_card = []
# handle device events asynchronously
async def listen_cards(device, recording = False, dump = False):
    listening = False
    try:
        async for event in device.async_read_loop():
            # only get keypress events
            if event.type == evdev.ecodes.EV_KEY:
                decoded_key = evdev.categorize(event)
                # only get downpress
                if decoded_key.keystate == decoded_key.key_down:
                    # dump data
                    if dump:
                        print(decoded_key.keycode)
                    # new card reading has begun
                    if decoded_key.keycode == 'KEY_SEMICOLON':
                        swiped_card = []
                        listening = True
                    if listening:
                        swiped_card.append(decoded_key.keycode)
                    # card is finished reading
                    if decoded_key.keycode == 'KEY_ENTER':
                        if recording:
                            cards.append(swiped_card)
                            print('Added new card')
                        else:
                            if swiped_card in cards:
                                print('Access granted.')
                            else:
                                print('Access denied.')

                        listening = False

    except OSError as e:
        print('Connection to reader lost.')
        for device in devices:
            device.close()
        loop.stop()

if __name__ == '__main__': 
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-r",action="store_true",help="Record new cards")
    parser.add_argument("-d",action="store_true",help="Print swipe data to console")
    args = parser.parse_args()

    # record mode
    if args.r:
        recording = True
        if not os.path.exists(card_record):
            print('{0} not found.  Creating...'.format(card_record))
            cards = []
        else:
            # try to load cards from card_record
            with open(card_record, 'r') as f:
                try:
                    cards = json.loads(f.read())
                except ValueError:
                    print('{0} seems to be corrupt.  Exiting...'.format(card_record))
                    quit()


    # listen mode
    else:
        recording = False
        if not os.path.exists(card_record):
            print('{0} not found.  Run record script to add new cards.'.format(card_record))
            quit()

        f = open(card_record, 'r')
        cards = json.loads(f.read())

    # dump cards
    if args.d:
        dump = True
    else:
        dump = False

    # set up asynchronous bits
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(listen_cards(card_reader, recording, dump))
    except KeyboardInterrupt as e:
        print('Caught keyboard interrupt.  Freeing reader...')
        if args.r:
            print('Saving recorded cards to {0}...'.format(card_record))
            with open(card_record, 'w') as f:
                f.write(json.dumps(cards))
        card_reader.ungrab()
        for task in asyncio.Task.all_tasks():
            task.cancel()
