#!/bin/env python3
# Evan Widloski - 2018-04-11
# keepass decrypt experimentation

import struct
import hashlib

database = 'test4.kdbx'
password = b'shatpass'
# password = None
keyfile = 'test4.key'
# keyfile = None

b = []
with open(database, 'rb') as f:
    b = f.read()

# ---------- Header Stuff ----------

# file magic number (4 bytes)
magic = b[0:4]
# keepass version (4 bytes)
# database minor version (2 bytes)
# database major version (2 bytes)
version, minor_version, major_version = struct.unpack('<IHH', b[4:12])

assert major_version == 4, "Database is not v4"

# header item lookup table
header_item_ids = {0: 'end',
                   1: 'comment',
                   2: 'cipher_id',
                   3: 'compression_flags',
                   4: 'master_seed',
                   7: 'encryption_iv',
                   8: 'protected_stream_key',
                   9: 'stream_start_bytes',
                   10: 'inner_random_stream_id',
                   11: 'kdf_parameters'
}

# read dynamic header

# offset of first header byte
offset = 12
# dict containing header items
header = {}

# loop until end of header
while b[offset] != 0:
    # read size of item (4 bytes)
    size, = struct.unpack('<I', b[offset + 1:offset + 5])
    # insert item into header dict
    header[header_item_ids[b[offset]]] = b[offset + 5:offset + 5 + size]
    # move to next header item
    # (1 byte for header item id, 4 bytes for item size, `size` bytes for data)
    offset += 1 + 4 + size

# move from `end` to start of header hash
size, = struct.unpack('<I', b[offset + 1:offset + 5])
offset += 1 + 4 + size

header_hash = hashlib.sha256(b[:offset]).digest()
offset += 32

# read kdf parameters
# https://github.com/dlech/KeePass2.x/blob/VS2017/KeePassLib/Cryptography/KeyDerivation/Argon2Kdf.cs#L33-39
# https://github.com/dlech/KeePass2.x/blob/VS2017/KeePassLib/Cryptography/KeyDerivation/AesKdf.cs#L45-L46

# loop until end of kdf_parameters
kdf_offset = 0
kdf_parameters = {}
dictionary_version = struct.unpack('<H', header['kdf_parameters'][0:2])
value_types = {
    0x04: 'I',
    0x05: 'Q',
    0x08: '?',
    0x0C: 'i',
    0x0D: 'q',
    0x18: '{length}s',
    0x42: '{length}s'
}

kdf_offset += 2
while header['kdf_parameters'][kdf_offset] != 0:
    value_type = header['kdf_parameters'][kdf_offset]
    key_size, = struct.unpack('<I', header['kdf_parameters'][kdf_offset + 1:kdf_offset + 5])
    key = header['kdf_parameters'][kdf_offset + 5:kdf_offset + 5 + key_size]
    kdf_offset += 1 + 4 + key_size
    value_size, = struct.unpack('<I', header['kdf_parameters'][kdf_offset:kdf_offset + 4])
    value, = struct.unpack('<' + value_types[value_type].format(length=value_size),
                          header['kdf_parameters'][kdf_offset + 4:kdf_offset + 4 + value_size])
    kdf_offset += 4 + value_size

    kdf_parameters[key.decode('utf-8')] = value

kdf_uuids = {
    'argon2': b'\xefcm\xdf\x8c)DK\x91\xf7\xa9\xa4\x03\xe3\n\x0c',
    'aes': b'\xc9\xd9\xf3\x9ab\x8aD`\xbft\r\x08\xc1\x8aO\xea',
}


# ---------- Key Derivation ----------

from pygcrypt.ciphers import Cipher
from pygcrypt.context import Context

# hash the password
if password:
    password_composite = hashlib.sha256(password).digest()
else:
    password_composite = b''
# hash the keyfile
if keyfile:
    try:
        with open(keyfile, 'rb') as f:
            keyfile_composite = hashlib.sha256(f.read()).digest()
    except:
        raise IOError('Could not read keyfile')

else:
    keyfile_composite = b''

# create composite key from password and keyfile composites
key_composite = hashlib.sha256(password_composite + keyfile_composite).digest()

if kdf_parameters['$UUID'] == kdf_uuids['argon2']:
    pass
elif kdf_parameters['$UUID'] == kdf_uuids['aes']:
    # set up a context for AES128-ECB encryption to find transformed_key
    context = Context()
    cipher = Cipher(b'AES', u'ECB')
    context.cipher = cipher
    context.key = kdf_parameters['S']
    context.iv = b'\x00' * 16

    # get the number of rounds from the header and transform the key_composite
    rounds = kdf_parameters['R']
    transformed_key = key_composite
    for _ in range(0, rounds):
        transformed_key = context.cipher.encrypt(transformed_key)

    # combine the transformed key with the header master seed to find the master_key
    transformed_key = hashlib.sha256(transformed_key).digest()
    master_key = hashlib.sha256(bytes(header['master_seed']) + transformed_key).digest()
else:
    raise Exception('Unsupported key derivation method')


# # dict containing inner header items
# inner_header = {}

# # inner heaer item lookup table
# inner_header_item_ids = {0: 'end',
#                          1: 'inner_random_stream_id',
#                          2: 'inner_random_stream_key',
#                          3: 'flags'
#                          }

# while b[offset] != 0:
#     # read size of item (4 bytes)
#     size, = struct.unpack('<I', b[offset + 1:offset + 5])
#     inner_header[inner_header_item_ids[offset]] = b[offset + 5:offset + 5 + size]
#     offset += 1 + 4 + size

