# Evan Widloski - 2019-09-15
# Decoding remarkable xochitl.conf

import re

# 3 config variants from different xochitl versions
# someone told me this is CBOR, but I haven't had any success on this front

config = r'glugphone=@Variant(\0\0\0\b\0\0\0\x3\0\0\0\b\0s\0s\0i\0\x64\0\0\0\n\0\0\0\x12\0g\0l\0u\0g\0p\0h\0o\0n\0\x65\0\0\0\x10\0p\0r\0o\0t\0o\0\x63\0o\0l\0\0\0\n\0\0\0\x6\0p\0s\0k\0\0\0\x10\0p\0\x61\0s\0s\0w\0o\0r\0\x64\0\0\0\n\0\0\0\x10\0p\0\x61\0s\0s\0w\0o\0r\0\x64)'
# config = r'Sad%20Wifi=@Variant(\0\0\0\b\0\0\0\x3\0\0\0\b\0s\0s\0i\0\x64\0\0\0\n\0\0\0\x10\0S\0\x61\0\x64\0 \0W\0i\0\x66\0i\0\0\0\x10\0p\0r\0o\0t\0o\0\x63\0o\0l\0\0\0\n\0\0\0\x6\0p\0s\0k\0\0\0\x10\0p\0\x61\0s\0s\0w\0o\0r\0\x64\0\0\0\n\0\0\0\x1c\0\x61\0\x64\0v\0\x65\0n\0t\0u\0r\0\x65\0 \0t\0i\0m\0\x65)'
# config = r'test2=@Variant(\0\0\0\b\0\0\0\x3\0\0\0\b\0s\0s\0i\0\x64\0\0\0\n\0\0\0\n\0t\0\x65\0s\0t\0\x32\0\0\0\x10\0p\0r\0o\0t\0o\0\x63\0o\0l\0\0\0\n\0\0\0\x6\0n\0o\0n\0e\0\0\0\x10\0p\0\x61\0s\0s\0w\0o\0r\0\x64\0\0\0\n\0\0\0\x10\0\x66\0o\0o\0\x62\0\x61\0r\0\x30\0\x30)'

# for some reason byte values less than \x10 have the leading zero removed. fix that
config = re.sub(r'\\x(.)\\0', r'\\x0\g<1>\\0', config)
# remove null bytes between all characters
config = re.sub(r'\\0', r'', config)
config = config.encode('utf8').decode('unicode_escape')

# split into fields
results = re.findall('[^\x08\x03(\n\x10)(\n\x12)(\n\x06)(\n\x1c)]+', config)

ssid = results[2]
protocol = results[4]
password = results[6]

print(results)
print('ssid:', ssid)
print('password:', ssid)
