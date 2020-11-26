#!/bin/env python3

from getpass import getpass
import argcomplete, argparse

def path_completer(prefix, parsed_args, **kwargs):
    f = open('/tmp/log', 'w')
    f.write('start\n')

    # x = input('input:')
    x = getpass('input:')

    f.write('got input\n')
    # database = open_databases(**vars(args))
    f.write('db open')
    return ['test', 'foo', 'bar']

def move(args):
    print(args)

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

mv_parser = subparsers.add_parser('mv', help='move a thing')
patharg = mv_parser.add_argument('path', metavar='PATH', type=str, help='entry/group path')
patharg.completer = path_completer
mv_parser.set_defaults(func=move)

print('ran program')
argcomplete.autocomplete(parser)

args = parser.parse_args()
