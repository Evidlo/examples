#!/usr/bin/env python
"""
(Python >3.3)

This is an example of how we can embed a Python REPL into an asyncio
application. In this example, we have one coroutine that runs in the
background, prints some output and alters a global state. The REPL, which runs
inside another coroutine can access and change this global state, interacting
with the running asyncio application.
The ``patch_stdout`` option makes sure that when another coroutine is writing
to stdout, it won't break the input line, but instead writes nicely above the
prompt.
"""
import asyncio

from ptpython.repl import embed
from prompt_toolkit.enums import EditingMode

loop = asyncio.get_event_loop()
counter = [0]

async def print_counter(q):
    """
    Example coroutine which waits for data in the queue
    """
    counter = 0
    while True:
        print('!!!', await q.get())
        print(f'{counter=}')
        counter += 1
        await asyncio.sleep(3)
        print('delayed print')


async def interactive_shell(q):
    """
    Shell coroutine which has access to the queue
    """
    def repl_config(repl):
        repl.show_status_bar = False
        repl.confirm_exit = False
        repl.editing_mode = EditingMode.VI

    def send(msg):
        q.put_nowait(msg)

    print('Use send(...) to stick things in the queue')
    await embed(
        globals=globals(),
        locals=locals(),
        return_asyncio_coroutine=True,
        patch_stdout=True,
        configure=repl_config
    )
    loop.stop()


def main():
    q = asyncio.Queue()
    # asyncio.ensure_future(print_counter(q))
    asyncio.ensure_future(interactive_shell(q))

    loop.run_forever()
    loop.close()


if __name__ == "__main__":
    main()
