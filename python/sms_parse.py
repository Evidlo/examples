#!/usr/bin/env python3
#
# parse XML from SMS backup and restore

from lxml import etree
from tqdm import tqdm
import json

f_input = '/tmp/sms.xml'
f_output = '/tmp/sms.json'

# message type meanings
typemap = {
    '1': 'user',
    '2': 'assistant'
}

print(f'Read from {f_input}')

# enumerate conversations
conversations = {}
for line in tqdm(open(f_input, 'r').readlines(), desc="Enumerating conversations..."):
    if line.lstrip().startswith('<sms '):
        try:
            msg = etree.fromstring(line).attrib
        except etree.XMLSyntaxError as e:
            print("offending line:", line)
            raise e

        number, content, kind = msg['address'][-10:], msg['body'], typemap[msg['type']]

        if number not in conversations:
            conversations[number] = []

        conversations[number].append({'role': kind, 'content': content})

print('Writing...')
with open(f_output, 'w') as f:
    json.dump(conversations, f, indent=2)
print(f'Wrote to {f_output}')
