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
while True:
    # read item id (1 byte)
    item_id = header_item_ids[b[offset]]
    offset += 1
    # read size of item (4 bytes)
    size, = struct.unpack('<I', b[offset:offset + 4])
    offset += 4
    if item_id == 'end':
        offset += size
        break
    else:
        # insert item into header dict
        header[item_id] = b[offset:offset + size]
        offset += size

header_end = offset

header_sha256_hash = b[offset:offset + 32]
assert header_sha256_hash == hashlib.sha256(b[:header_end]).digest(), "Header verification failed"
offset += 32

header_hmac_hash = b[offset:offset + 32]
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

    # read type of item (1 bytes)
    value_type = header['kdf_parameters'][kdf_offset]
    kdf_offset += 1
    # read size of item key
    key_size, = struct.unpack('<I', header['kdf_parameters'][kdf_offset:kdf_offset + 4])
    kdf_offset += 4
    # read item key (`key_size` bytes)
    key = header['kdf_parameters'][kdf_offset:kdf_offset + key_size]
    kdf_offset += key_size
    # read item value size (4 bytes)
    value_size, = struct.unpack('<I', header['kdf_parameters'][kdf_offset:kdf_offset + 4])
    kdf_offset += 4
    value, = struct.unpack('<' + value_types[value_type].format(length=value_size),
                          header['kdf_parameters'][kdf_offset:kdf_offset + value_size])
    kdf_offset += value_size

    kdf_parameters[key.decode('utf-8')] = value

kdf_uuids = {
    'argon2': b'\xefcm\xdf\x8c)DK\x91\xf7\xa9\xa4\x03\xe3\n\x0c',
    'aes': b'\xc9\xd9\xf3\x9ab\x8aD`\xbft\r\x08\xc1\x8aO\xea',
}


# ---------- Key Derivation ----------

from pygcrypt.ciphers import Cipher
from pygcrypt.context import Context
import hmac
import argon2

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
    transformed_key = argon2.low_level.hash_secret_raw(secret=key_composite,
                                                       salt=kdf_parameters['S'],
                                                       hash_len=32,
                                                       type=argon2.low_level.Type.D,
                                                       time_cost=kdf_parameters['I'],
                                                       memory_cost=kdf_parameters['M'] // 1024,
                                                       parallelism=kdf_parameters['P'],
                                                       version=kdf_parameters['V']
    )
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

    transformed_key = hashlib.sha256(transformed_key).digest()
else:
    raise Exception('Unsupported key derivation method')

# combine the transformed key with the header master seed to find the master_key
master_key = hashlib.sha256(header['master_seed'] + transformed_key).digest()

# validate second header hash
hmac_key = hashlib.sha512(b'\xff' * 8 + hashlib.sha512(header['master_seed'] + transformed_key + b'\x01').digest()).digest()
assert header_hmac_hash == hmac.new(hmac_key, b[:header_end], hashlib.sha256).digest(), "Header validation failed"

# ---------- Process and verify payload blocks ----------

payload_data = b''

# read payload block data, block by block
while True:
    # read hmac hash of payload data block (32 bytes)
    block_hmac_hash = b[offset:offset + 32]
    # read block size (4 bytes)
    block_size, = struct.unpack('<I', b[offset + 32:offset + 36])
    if block_size == 0:
        break
    # read block data (`block_size` bytes)
    block_data = b[offset + 36:offset + 36 + block_size]
    payload_data += block_data

    offset += 36 + block_size

payload_ciphers = {
    'aes256': b'1\xc1\xf2\xe6\xbfqCP\xbeX\x05!j\xfcZ\xff',
    # 'twofish': b'\xadh\xf2\x9fWoK\xb9\xa3j\xd4z\xf9e4l',
    # 'chacha20': b'\xd6\x03\x8a+\x8boL\xb5\xa5$3\x9a1\xdb\xb5\x9a'
}

# ---------- Decrypt payload ----------

if header['cipher_id'] == payload_ciphers['aes256']:
    # set up a context for AES128-CBC decryption to find the decrypted payload
    context = Context()
    cipher = Cipher(b'AES', u'CBC')
    context.cipher = cipher
    context.key = master_key
    context.iv = header['encryption_iv']
    payload_data = context.cipher.decrypt(payload_data)
else:
    raise Exception('Unsupported payload cipher')

import zlib

# check if payload_data is compressed
if struct.unpack('<I', header['compression_flags']):
    # decompress using gzip
    payload_data = zlib.decompress(payload_data, 16 + 15)
else:
    payload_data = payload_data

# ---------- Inner header ----------

# dict containing inner header items
inner_header = {}

# inner header item lookup table
inner_header_item_ids = {
    0x00: 'end',
    0x01: 'inner_random_stream_id',
    0x02: 'inner_random_stream_key',
    0x03: 'flags'
}

inner_offset = 0

# read inner header
while True:
    # read item id (1 byte)
    item_id = inner_header_item_ids[payload_data[inner_offset]]
    inner_offset += 1
    # read size of item (4 bytes)
    size, = struct.unpack('<I', payload_data[inner_offset:inner_offset + 4])
    inner_offset += 4
    if item_id == 'end':
        inner_offset += size
        break
    else:
        inner_header[item_id] = b[inner_offset:inner_offset + size]
        inner_offset += size

# xml_data immediately follows inner header
xml_data = payload_data[inner_offset:]

print(xml_data)
