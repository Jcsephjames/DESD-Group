"""Send JSON requests to Camunda from workflow workers."""

import json
from urllib.error import HTTPError
from urllib.request import Request, urlopen


def post(base_url, path, payload):
    """Send a JSON POST request to Camunda and decode the response."""
    # Build an HTTP POST request using the Camunda internal address and the data we want to send.
    # We convert the Python dictionary into JSON because Camunda expects requests in JSON format.
    request = Request(
        f"{base_url.rstrip('/')}/{path}",
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )

    # Send the request to Camunda and read its response.
    try:
        with urlopen(request, timeout=30) as response:
            body = response.read()
        return json.loads(body) if body else None
    except HTTPError as error:
        detail = error.read().decode(errors="replace")
        raise RuntimeError(
            f"Camunda {path} returned HTTP {error.code}: {detail}"
        ) from error
