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


def get_org() -> str:
    """Get the CVAT organization name."""
    org = os.getenv("CVAT_ORG")
    if org is None:
        org = input("Organization: ")
    return org


def get_client(
    username: str = get_username(),
    password: str = get_password(),
    org: str = get_org(),
) -> Client:
    """Get the CVAT SDK high-level client object."""
    url = get_host().rstrip("/")
    client = Client(url=url, check_server_version=False)
    credentials = (username, password)
    client.login(credentials)
    client.api_client.set_default_header("x-organization", org)
    return client
