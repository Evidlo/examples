#/bin/env python3
## Evan Widloski - 2017-01-06
## Asynchronous magstripe reader example
## Requires root and >= python 3.5

# Much taken from: http://python-evdev.readthedocs.io/en/latest/tutorial.html#reading-events-from-multiple-devices-using-asyncio

import asyncio, evdev

# MSR100 reader vendor/product ids
vendor = 0xc216
product = 0x0180

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

# handle device events asynchronously
async def process_events(device):
    try:
        async for event in device.async_read_loop():
            # only get keypress events
            if event.type == evdev.ecodes.EV_KEY:
                decoded_key = evdev.categorize(event)
                # only get downpress
                if decoded_key.keystate == decoded_key.key_down:
                    print(decoded_key.keycode)
    except OSError as e:
        print('Connection to reader lost.')
        for device in devices:
            device.close()
        loop.stop()

asyncio.ensure_future(process_events(card_reader))
loop = asyncio.get_event_loop()
try:
    loop.run_forever()
except KeyboardInterrupt as e:
    print('Caught keyboard interrupt.  Freeing reader...')
    card_reader.ungrab()
