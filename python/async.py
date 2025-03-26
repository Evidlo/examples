#!/usr/bin/env python3
# incomplete

import asyncio

async def looping(duration=.5):
    while True:
        # asyncio.sleep() returns a coroutine
        # we want to start and wait for this coroutine to complete
        await asyncio.sleep(duration)
        print('Looper!')

async def count_up(n=10, duration=1):
    result = 0
    for x in range(n):
        result += x
        await asyncio.sleep(duration)
    # return when done
    return result

async def main():
    loop_task = asyncio.create_task(looping())

    # count_up() returns a coroutine
    # the coroutine does nothing unless we await it or create a separate task
    computed = await count_up()
    print('computed result:', computed)

    await loop_task


if __name__ == '__main__':
    asyncio.run(main())
