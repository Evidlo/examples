import argparse
import logging

logging.basicConfig()
log = logging.getLogger(__name__)

def add(args):
    log.debug("Adding {} to {}".format(args.num1, args.num2))
    print("Result: {}".format(args.num1 + args.num2))

def main():
    parser = argparse.ArgumentParser(description="Calculator program")
    parser._positionals.title = "commands"

    subparsers = parser.add_subparsers()
    subparsers.required = True

    # program arguments
    parser.add_argument('--debug', action='store_true', default=False, help="enable debugging")
    parser.add_argument('file', metavar='FILE', type=str, help="a file")

    # subparser for `add` command
    add_parser = subparsers.add_parser('add', help="add two numbers")
    # these arguments have no default and are required
    add_parser.add_argument('num1', type=int)
    add_parser.add_argument('num2', type=int)
    # `store_true` means just store that this option was used, i.e. this option has no argument
    add_parser.add_argument('--sub', action='store_true', default=False, help="subtract instead of add")
    add_parser.set_defaults(func=add)

    args = parser.parse_args()

    if args.debug:
        log.setLevel(logging.DEBUG)
        log.debug("Debugging enabled")

    args.func(args)

if __name__ == '__main__':
    main()
