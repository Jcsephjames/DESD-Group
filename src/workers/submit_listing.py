"""Receive submit-listing jobs and publish product-submitted messages to Camunda."""

import argparse
import json
import logging
import os
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

LOGGER = logging.getLogger(__name__)


def post(base_url, path, payload):
    """Send a JSON POST request to Camunda and decode the response."""
    request = Request(
        f"{base_url.rstrip('/')}/{path}",
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=30) as response:
            body = response.read()
            return json.loads(body) if body else None
    except HTTPError as error:
        detail = error.read().decode(errors="replace")
        raise RuntimeError(
            f"Camunda {path} returned HTTP {error.code}: {detail}"
        ) from error


def _completion_payload(submission_key):
    return {
        "variables": {
            "originalSubmissionKey": submission_key,
            "submissionKey": submission_key,
        }
    }


def submit_listing(job, base_url, *, send=post):
    """Publish before completing; preserve the form's original variable names.

    The job key stays the same on retries and is used as the message ID. Camunda
    deduplicates matching messages while their one-hour TTL remains active; this
    is not permanent exactly-once delivery. The receiving process must also handle
    duplicate submissions when persistence is connected.
    """
    # Keep the original form variables intact while we build the outgoing message.
    job_variables = dict(job.get("variables", {}))
    is_correction = job_variables.get("isCorrection") is True
    custom_headers = job.get("customHeaders") or {}

    # Reject unsupported correction jobs before publishing anything.
    if is_correction and custom_headers.get("correctionLoop") != "enabled":
        raise ValueError(
            "This older process version has no correction form. Start a new "
            "submission using the latest process version."
        )

    # Correction submissions reuse the original key so the message matches the right record.
    if is_correction:
        job_variables["submissionKey"] = job_variables["originalSubmissionKey"]

    submission_key = job_variables.get("submissionKey")
    if not isinstance(submission_key, str) or not submission_key.strip():
        raise ValueError("The form must supply a non-empty submissionKey string.")

    payload = {
        "name": "product-resubmitted" if is_correction else "product-submitted",
        "correlationKey": submission_key,
        "messageId": f"submit-listing-{job['jobKey']}",
        "timeToLive": 3600000,
        "variables": job_variables,
    }
    if job.get("tenantId"):
        payload["tenantId"] = job["tenantId"]

    # Publish the business event before completing the Camunda job.
    send(base_url, "messages/publication", payload)
    send(
        base_url,
        f"jobs/{job['jobKey']}/completion",
        _completion_payload(submission_key),
    )
    LOGGER.info("Submitted listing for job %s", job["jobKey"])


def run(base_url, once=False):
    while True:
        try:
            # Fetch one submit-listing job from Camunda for processing.
            response = post(
                base_url,
                "jobs/activation",
                {
                    "type": "submit-listing",
                    "worker": "submit-listing-worker",
                    "timeout": 120000,
                    "maxJobsToActivate": 1,
                    "requestTimeout": 10000,
                },
            )
            jobs = response.get("jobs", [])

            # Handle each job and report failures back to Camunda.
            for job in jobs:
                try:
                    submit_listing(job, base_url)
                except (ValueError, RuntimeError, OSError) as error:
                    LOGGER.error("Job %s failed: %s", job["jobKey"], error)
                    post(
                        base_url,
                        f"jobs/{job['jobKey']}/failure",
                        {
                            "retries": max(job["retries"] - 1, 0),
                            "retryBackOff": 10000,
                            "errorMessage": str(error)[:2000],
                        },
                    )

            if once:
                return
            if not jobs:
                time.sleep(1)
        except (RuntimeError, URLError, OSError):
            if once:
                raise
            LOGGER.exception("Camunda request failed; retrying in five seconds")
            time.sleep(5)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--camunda-url",
        default=os.environ.get("CAMUNDA_REST_URL", "http://camunda:8080/v2"),
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Poll once, process any job, then exit",
    )
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    try:
        run(args.camunda_url, args.once)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
