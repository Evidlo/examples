#!/bin/env python3
# Evan Widloski - 2018-04-11
# pygcrypt/pykeepass experimentation

# Useful reference: https://gist.github.com/msmuenchen/9318327
#                   https://framagit.org/okhin/pygcrypt/#use

import struct

database = 'test.kdbx'
password = b'shatpass'

b = []
with open('test.kdbx', 'rb') as f:
    b = bytearray(f.read())

# ---------- Header Stuff ----------

# file magic number (4 bytes)
magic = b[0:4]
# keepass version (2 bytes)
version = b[4:8]
# database minor version (2 bytes)
minor_version = b[8:10]
# database major version (2 bytes)
major_version = b[10:12]

# header item lookup table
header_item_ids = {0: 'end',
                   1: 'comment',
                   2: 'cipher_id',
                   3: 'compression_flags',
                   4: 'master_seed',
                   5: 'transform_seed',
                   6: 'transform_rounds',
                   7: 'encryption_iv',
                   8: 'protected_stream_key',
                   9: 'stream_start_bytes',
                   10: 'inner_random_stream_id'
}

# read dynamic header

# offset of first header byte
offset = 12
# dict containing header items
header = {}

# loop until end of header
while b[offset] != 0:
    # read size of item (2 bytes)
    size = struct.unpack('<H', b[offset + 1:offset + 3])[0]
    # insert item into header dict
    header[header_item_ids[b[offset]]] = b[offset + 3:offset + 3 + size]
    # move to next header item
    # (1 byte for header item id, 2 bytes for item size, `size` bytes for data)
    offset += 1 + 2 + size

# move from `end` to start of payload
size = struct.unpack('<H', b[offset + 1:offset + 3])[0]
offset += 1 + 2 + size

# ---------- Payload Stuff ----------

from pygcrypt.ciphers import Cipher
from pygcrypt.context import Context
import hashlib

encrypted_payload = b[offset:]

# hash the password into a composite key
sha256 = hashlib.sha256()
sha256.update(password)
composite_password = sha256.digest()
sha256 = hashlib.sha256()
sha256.update(composite_password)
composite_key = sha256.digest()

# set up a context for AES128-ECB encryption to find transformed_key
context = Context()
cipher = Cipher(b'AES', u'ECB')
context.cipher = cipher
context.key = bytes(header['transform_seed'])
context.iv = b'\x00' * 16

# get the number of rounds from the header and transform the composite_key
rounds = struct.unpack('<Q', header['transform_rounds'])[0]
transformed_key = composite_key
for _ in range(0, rounds):
    transformed_key = context.cipher.encrypt(transformed_key)

# combine the transformed key with the header master seed to find the master_key
sha256 = hashlib.sha256()
sha256.update(transformed_key)
transformed_key = sha256.digest()
sha256 = hashlib.sha256()
sha256.update(bytes(header['master_seed']) + transformed_key)
master_key = sha256.digest()

# set up a context for AES128-CBC decryption to find the decrypted payload
context = Context()
cipher = Cipher(b'AES', u'CBC')
context.cipher = cipher
context.key = master_key
context.iv = bytes(header['encryption_iv'])
raw_payload_area = context.cipher.decrypt(bytes(encrypted_payload))
