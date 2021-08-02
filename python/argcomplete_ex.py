#!/bin/env python3

from getpass import getpass
import argcomplete, argparse

def path_completer(prefix, parsed_args, **kwargs):
    password = getpass('\nInput Password:')

    if password == 'password':
        return ['helloworld', 'foobar']

parser = argparse.ArgumentParser()

patharg = parser.add_argument('path', metavar='PATH', type=str, help='item path')
patharg.completer = path_completer

argcomplete.autocomplete(parser)
args = parser.parse_args()
print(f'selected item: {args.path}')
