"""Authentication methods."""
import os
from getpass import getpass

from cvat_sdk.api_client import ApiClient, Configuration


def get_host() -> str:
    """Get the CVAT backend host."""
    return os.getenv("CVAT_HOST", "https://backend.sparrowml.net")


def get_username() -> str:
    """Get the CVAT user."""
    username = os.getenv("CVAT_USERNAME")
    if username is None:
        username = input("Username: ")
    return username


def get_org() -> str:
    """Get the CVAT org."""
    return os.getenv("CVAT_ORG")


def get_password() -> str:
    """Get the CVAT password."""
    password = os.getenv("CVAT_PASSWORD")
    if password is None:
        password = getpass()
    return password


def get_token() -> str:
    """Get the CVAT auth token."""
    token = os.getenv("CVAT_TOKEN")
    if token is not None:
        return token
    config = Configuration(get_host())
    auth, _ = ApiClient(config).auth_api.create_login(
        {"username": get_username(), "password": get_password()}
    )
    return auth.key


def get_api() -> ApiClient:
    """Get the CVAT API client object."""
    config = Configuration(get_host(), api_key={"tokenAuth": f"Token {get_token()}"})
    return ApiClient(config)
