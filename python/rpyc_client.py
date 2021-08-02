import rpyc
from pykeepass.exceptions import CredentialsError
import pykeepass.exceptions
import pykeepass


if __name__ == "__main__":
    c = rpyc.connect("localhost", 12345)
    print(c.root.foobar('hello'))
    import ipdb
    ipdb.set_trace()
