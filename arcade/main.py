import os
import sys
import click

from commands import init, watch

@click.group()
def cli():
    pass


@cli.add_command(init)
@cli.add_command(wath)
    
if __name__ == '__main__':
    cli()
