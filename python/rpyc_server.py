import rpyc
from rpyc.utils.server import ThreadedServer
from pykeepass.exceptions import CredentialsError


class HelloService(rpyc.Service):
    def exposed_foobar(self, remote_str):
        self.close()


class MyServer(ThreadedServer):

    def __init__(self, *args, **kwargs):
        args[0].close = self.close
        super().__init__(*args, **kwargs)

if __name__ == "__main__":
    rpyc.lib.setup_logger()
    server = MyServer(
        HelloService,
        port=12345,
    )
    server.start()
