"""Authentication methods."""
import os
from getpass import getpass

from .api import post


def get_user() -> str:
    """Get the CVAT user."""
    user = os.getenv("CVAT_USER")
    if user is None:
        raise ValueError("Please set the CVAT_USER environment variable.")
    return user


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
    """Get the auth token for a user."""
    response = post(
        "/api/auth/login",
        data=dict(username=get_user(), password=get_password()),
    )
    return response["key"]


def get_auth_headers() -> dict[str, str]:
    """Get auth headers for a request."""
    return dict(Authorization=f"Token {get_token()}")
