import os
import sys
import click

from commands import init, watch, build


@click.group()
def cli():
    pass


cli.add_command(init, name="init")
cli.add_command(watch, name="watch")
cli.add_command(build, name="build")

if __name__ == "__main__":
    cli()
