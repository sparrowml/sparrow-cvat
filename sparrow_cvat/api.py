"""API class for CVAT."""
from __future__ import annotations

import os
import time
import warnings
from getpass import getpass
from typing import Any, Optional
from urllib.parse import parse_qsl, urlencode, urlparse

import requests
from cvat_sdk import Client
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import MaxRetryError


def get_host() -> str:
    """Get the CVAT backend host."""
    return os.getenv("CVAT_HOST", "https://sparrowml.net")


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
    username: Optional[str] = None,
    password: Optional[str] = None,
    org: Optional[str] = None,
) -> Client:
    """Get the CVAT SDK high-level client object."""
    if username is None:
        username = get_username()
    if password is None:
        password = get_password()
    if org is None:
        org = get_org()
    url = get_host().rstrip("/")
    client = Client(url=url, check_server_version=False)
    credentials = (username, password)
    client.login(credentials)
    client.api_client.set_default_header("x-organization", org)
    return client


def raise_for_status(response: requests.Response) -> None:
    """Raise an error if the response status code is not 200."""
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise requests.exceptions.HTTPError(
            f"{error}\nResponse body: {response.text}"
        ) from error


class CVAT:
    """API class for CVAT."""

    base_url: str = get_host()
    api_url: str = os.path.join(base_url, "api")
    basic_auth: HTTPBasicAuth = HTTPBasicAuth(get_username(), get_password())

    @classmethod
    def _org_specific_route(cls, route: str) -> str:
        """Prepend the organization name to a route."""
        url = urlparse(route)
        query_params = dict(parse_qsl(url.query))
        query_params.update({"org": get_org()})
        query = urlencode(query_params)
        return f"{url.path}?{query}"

    @classmethod
    def delete(cls, route: str) -> dict[str, Any]:
        """Make a DELETE request to the CVAT API."""
        route = cls._org_specific_route(route)
        response = requests.delete(
            os.path.join(cls.api_url, route), auth=cls.basic_auth
        )
        raise_for_status(response)
        if response.status_code == 204:
            return {}
        return response.json()

    @classmethod
    def download(cls, route: str) -> bytes:
        """Download a file from the CVAT API."""
        route = cls._org_specific_route(route)
        print("Preparing download...", end="", flush=True)
        response = requests.get(os.path.join(cls.api_url, route), auth=cls.basic_auth)
        raise_for_status(response)
        while len(response.content) == 0:
            print(".", end="", flush=True)
            time.sleep(0.25)
            response = requests.get(
                os.path.join(cls.api_url, route), auth=cls.basic_auth
            )
            raise_for_status(response)
        print(flush=True)
        return response.content

    @classmethod
    def get(cls, route: str) -> dict[str, Any]:
        """Make a GET request to the CVAT API."""
        route = cls._org_specific_route(route)
        response = requests.get(os.path.join(cls.api_url, route), auth=cls.basic_auth)
        raise_for_status(response)
        if response.status_code == 204:
            return {}
        return response.json()

    @classmethod
    def post(cls, route: str, payload: dict[str, Any] = dict()) -> dict[str, Any]:
        """Make a POST request to the CVAT API."""
        route = cls._org_specific_route(route)
        response = requests.post(
            os.path.join(cls.api_url, route), auth=cls.basic_auth, json=payload
        )
        raise_for_status(response)
        if response.status_code == 204:
            return {}
        return response.json()


class SparrowML(CVAT):
    """API class for SparrowML."""

    api_url: str = os.path.join(CVAT.base_url, "sparrowml/api")
