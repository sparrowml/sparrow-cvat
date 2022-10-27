"""Interact with CVAT API."""
import os
import sys
import traceback
from typing import Any, Optional

import requests


def get_host() -> str:
    """Get the CVAT backend host."""
    return os.getenv("CVAT_HOST", "https://backend.sparrowml.net")


def get_url(route: str) -> str:
    """Create a route with the host."""
    return os.path.join(get_host(), route.removeprefix("/"))


def post(
    route: str, data: dict[str, Any], headers: Optional[dict[str, str]] = None
) -> dict[str, Any]:
    """Send a POST request."""
    response = requests.post(get_url(route), json=data, headers=headers)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        traceback.print_exc()
        print(f"\n{response.content.decode()}\n")
        sys.exit(1)
    return response.json()
