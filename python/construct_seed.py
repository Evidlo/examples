# test random seed generation in construct

from construct import Struct, Bytes, Computed, this, Transformed
from Crypto.Cipher import AES

# simple encryption/decryption
def encrypt(key):
    # cipher = AES.new(key, AES.MODE_ECB)
    # return lambda data: cipher.encrypt(data)
    print(data)
    return b'\x00' * 16

def decrypt(data):
    # cipher = AES.new(key, AES.MODE_ECB)
    # return lambda data: cipher.decrypt(data)
    print(data)
    return b'\x00' * 16

s = Struct(
    "seed" / Bytes(16),
    "data" / Transformed(
        Bytes(16),
        encrypt,
        16,
        decrypt,
        16
    )
)

seed = b'0x00' * 16
data = b'\x17*\xfe\xcbP\xb5\xf1#x\x14\xb2\xf7\xcbQ\xd0\xf7'

result = s.parse(seed + data)
assert result.data == b'hello world!!!!!'
