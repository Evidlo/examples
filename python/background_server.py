# Evan Widloski - 2019-04-30
# Simple Client-Server example
# Forks a long-running background process which listens on a socket at /tmp/socket.

from multiprocessing.connection import Listener, Client
from socket import timeout as TimeoutError
import sys
import os
import time
import daemon
import traceback

socket_file = '/tmp/socket'

# a Traceback object is returned if the server has an exception
class Traceback:
    def __init__(self, traceback):
        self.traceback = traceback
    def __repr__(self):
        return self.traceback

def server():
    """listen on socket and respond to messages from client"""
    # automatically close server after N seconds
    timeout = 5
    listener = Listener(socket_file)
    listener._listener._socket.settimeout(timeout)

    try:
        # simulate a slow server startup
        time.sleep(2)
        # raise Exception

    except Exception as e:
        # wait up to 1s for client to connect to send back exception info
        listener._listener._socket.settimeout(1)
        conn = listener.accept()
        conn.send(Traceback(traceback.format_exc()))
        sys.exit()

    try:
        while True:
            try:
                conn = listener.accept()
            # timeout if no client connects
            except TimeoutError:
                sys.exit()

            # server response
            conn.send([2.25, None, 'junk', float])
            # raise Exception

            # tell client we are done sending
            conn.send(False)

            # reset timeout
            listener._listener._socket.settimeout(timeout)

    except Exception as e:
        # wait up to 1s for client to connect to send back exception info
        listener._listener._socket.settimeout(1)
        conn.send(Traceback(traceback.format_exc()))
        sys.exit()


def client():
    """connect to server over socket"""
    conn = Client(socket_file)

    conn.send('command1')

    # get results from server
    while True:
        try:
            result = conn.recv()

        # handle response timeout
        except EOFError:
            print('server exited unexpectedly')
            sys.exit()

        # handle server exception
        if type(result) is Traceback:
            print('error on server')
            print(result)
            sys.exit()

        # server is done sending
        elif result == False:
            break

        # print server results
        else:
            print(result)

    conn.close()
    sys.exit()


def main():

    # if server is running, connect to it
    if os.path.exists(socket_file):
        client()

    # otherwise, fork server, then connect to it
    else:
        pid = os.fork()

        # parent process, run server() as unix daemon
        if pid == 0:
            with daemon.DaemonContext():
                server()
        # child process
        else:
            time.sleep(.1)
            client()


if __name__ == '__main__':
    main()
