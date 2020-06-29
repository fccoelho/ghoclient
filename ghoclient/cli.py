"""Console script for ghoclient."""
import sys
import click
from ghoclient import GHOSession


@click.command()
def main(args=None):
    """Console script for ghoclient."""

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
