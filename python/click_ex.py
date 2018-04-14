#!/bin/env python3
# Evan Widloski - 2018-03-26
# Example usage of Click library

import click
import logging

logging.basicConfig()
log = logging.getLogger(__name__)

@click.group()
@click.option('--verbose', is_flag=True, help="Will print verbose messages.")
def cli(verbose):
    """This is an example script to learn Click."""
    if verbose:
        click.echo("verbose mode.")
        log.setLevel(logging.DEBUG)
    click.echo("Hello World")

@click.command(short_help="add two numbers", help="add NUM1 and NUM2")
@click.argument('num1')
@click.argument('num2')
def add(num1, num2):
    log.debug("Adding {} to {}".format(num1, num2))
    click.echo("Result: {}".format(int(num1) + int(num2)))


cli.add_command(add)
if __name__ == '__main__':
    cli()
