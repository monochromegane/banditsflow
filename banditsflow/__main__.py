import os

import click

from . import scaffold as s


@click.group()
def cli() -> None:
    pass


@click.command()
@click.argument("name")
def scaffold(name: str) -> None:
    s.Builder().build(
        name, os.path.join(os.path.dirname(__file__), "templates"), os.getcwd()
    )


cli.add_command(scaffold)

if __name__ == "__main__":
    cli()
