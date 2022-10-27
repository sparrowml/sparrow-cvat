"""Expose CLI."""
import fire

from .auth import get_token


def main() -> None:
    """Call CLI commands."""
    fire.Fire({"get-token": get_token})
