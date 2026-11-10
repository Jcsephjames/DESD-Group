"""Send a certificate ID to the certification service."""

import argparse
from http.client import HTTPException
import json
import os
from pathlib import Path
import sys
from urllib.request import Request, urlopen
from uuid import uuid4

from submit_listing import post


def verification(certificate_id, service_url, timeout=10, *, query_id=None):
    """Send a certificate query and verify that the response matches it."""
    if not isinstance(certificate_id, str) or not certificate_id.strip():
        raise ValueError("A non-empty certificate_id is required.")
    if not service_url:
        raise ValueError("Set CERTIFICATION_SERVICE_URL or pass --service-url.")
    if query_id is None:
        query_id = uuid4().hex
    if not isinstance(query_id, str) or not query_id.strip():
        raise ValueError("A non-empty query_id is required.")

    request = Request(
        service_url,
        data=json.dumps({"certificate_id": certificate_id.strip(), "query_id": query_id}).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=timeout) as response:
        result = json.load(response)
    if (
        not isinstance(result, dict)
        or result.get("query_id") != query_id
        or not isinstance(result.get("valid"), bool)
        or (not result["valid"] and not isinstance(result.get("reason"), str))
    ):
        raise ValueError("Invalid response from the certificate service.")
    return result


def verify_certificate(job, base_url):
    certificate_id = job["variables"]["standardisedProduct"]["certificate_id"]
    query_id = str(job["jobKey"])
    job_path = f"jobs/{query_id}"
    try:
        result = verification(certificate_id, os.environ.get("CERTIFICATION_SERVICE_URL"), query_id=query_id)
    except (HTTPException, OSError, ValueError):
        post(base_url, f"{job_path}/error", {
            "errorCode": "VERIFICATION_UNAVAILABLE",
            "errorMessage": "The certificate service could not complete the check.",
        })
        return

    valid = result["valid"]
    errors = {} if valid else {"certificate_id": result["reason"]}
    post(base_url, f"{job_path}/completion", {"variables": {
        "certificateValid": valid,
        "certificationStatus": "verified" if valid else "failed",
        "verificationPending": False,
        "validationErrors": errors,
    }})


def mark_pending(job, base_url):
    post(base_url, f"jobs/{job['jobKey']}/completion", {"variables": {
        "certificateValid": False,
        "certificationStatus": "unavailable",
        "verificationPending": True,
    }})


def notify_verification_unavailable(job, base_url):
    message = {
        "name": "verification-pending",
        "correlationKey": job["variables"]["submissionKey"],
        "messageId": f"verification-pending-{job['jobKey']}",
        "timeToLive": 3600000,
        "variables": {
            "verificationPending": True,
            "verificationMessage": "The certificate service is unavailable. Your listing is pending verification.",
        },
    }
    if job.get("tenantId"):
        message["tenantId"] = job["tenantId"]
    post(base_url, "messages/publication", message)
    post(base_url, f"jobs/{job['jobKey']}/completion", {})


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
        result = verification(payload.get("certificate_id"), args.service_url, query_id=payload.get("query_id"))
    except (HTTPException, OSError, ValueError) as error:
        parser.exit(2, f"Cannot send certificate: {error}\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
