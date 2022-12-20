"""Authentication methods."""
import os
from getpass import getpass

from cvat_sdk import Client, make_client


def get_host() -> str:
    """Get the CVAT backend host."""
    return os.getenv("CVAT_HOST", "https://backend.sparrowml.net")


def get_username() -> str:
    """Get the CVAT user."""
    username = os.getenv("CVAT_USERNAME")
    if username is None:
        username = input("Username: ")
    return username


def get_password() -> str:
    """Get the CVAT password."""
    password = os.getenv("CVAT_PASSWORD")
    if password is None:
        password = getpass()
    return password


def get_client() -> Client:
    """Get the CVAT SDK high-level client object."""
    return make_client(get_host(), credentials=(get_username(), get_password()))
