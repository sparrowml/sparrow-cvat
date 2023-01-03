"""Authentication methods."""
import os
from getpass import getpass

from cvat_sdk import Client


def get_host() -> str:
    """Get the CVAT backend host."""
    return os.getenv("CVAT_HOST", "https://backend.sparrowml.net")


def get_ui_host() -> str:
    """Get the CVAT UI host."""
    return os.getenv("CVAT_UI_HOST", "https://sparrowml.net")


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
    url = get_host().rstrip("/")
    client = Client(url=url, check_server_version=False)
    credentials = (get_username(), get_password())
    client.login(credentials)
    return client
