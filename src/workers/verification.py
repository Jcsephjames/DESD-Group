"""Send a certificate ID to the certification service."""

import argparse
import json
import os
from pathlib import Path
import sys
from urllib.error import URLError
from urllib.request import Request, urlopen


def verification(certificate_id, service_url, timeout=10):
    """POST the certificate ID and return the service's JSON response.

    Transport errors are raised so the caller can retry verification rather
    than treating an unavailable service as an invalid certificate.
    """
    if not isinstance(certificate_id, str) or not certificate_id.strip():
        raise ValueError("A non-empty certificate_id is required.")
    if not service_url:
        raise ValueError("Set CERTIFICATION_SERVICE_URL or pass --service-url.")

    request = Request(
        service_url,
        data=json.dumps({"certificate_id": certificate_id.strip()}).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=timeout) as response:
        return json.load(response)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", nargs="?", type=Path, help="Product or certificate JSON file; otherwise read stdin")
    parser.add_argument("--service-url", default=os.environ.get("CERTIFICATION_SERVICE_URL"))
    args = parser.parse_args()
    try:
        raw = args.file.read_text(encoding="utf-8") if args.file else sys.stdin.read()
        payload = json.loads(raw)
        if not isinstance(payload, dict):
            raise ValueError("Input must be a JSON object containing certificate_id.")
        result = verification(payload.get("certificate_id"), args.service_url)
    except (OSError, ValueError, URLError) as error:
        parser.exit(2, f"Cannot send certificate: {error}\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
