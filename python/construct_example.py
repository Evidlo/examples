#!/bin/env python
# Evan Widloski - 2018-05-24
# Example python-construct adapter.  Maps ListContainer to Container and vice-versa

from construct import Struct, Enum, Byte, Prefixed, GreedyBytes, RepeatUntil, Int8ul, Adapter, Container, ListContainer

class DynamicDict(Adapter):
    def __init__(self, key, subcon):
        super().__init__(subcon)
        self.key = key

    # map ListContainer to Container
    def _decode(self, obj, context, path):
        d = {item[self.key]:item for item in obj}
        return Container(d)

    # map Container to ListContainer
    def _encode(self, obj, context, path):
        return ListContainer(obj.values())

DictItem = Struct("id"   / Enum(Byte, comment=0x08, another_field=0x09, dict_end=0x00),
                  "data" / Prefixed(Int8ul, GreedyBytes))

header = RepeatUntil(lambda item, a, b: item.id == 'dict_end', DictItem)

data = b'\x08\x01\x01' + b'\x09\x01\x01' + b'\x00\x00'

print(header.parse(data))

print(DynamicDict('id', header).parse(data))
