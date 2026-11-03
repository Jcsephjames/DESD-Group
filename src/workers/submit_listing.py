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
    request = Request(
        f"{base_url.rstrip('/')}/{path}",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=30) as response:
            body = response.read()
            return json.loads(body) if body else None
    except HTTPError as error:
        detail = error.read().decode(errors="replace")
        raise RuntimeError(f"Camunda {path} returned HTTP {error.code}: {detail}") from error


def submit_listing(job, base_url, *, send=post):
    """Publish before completing; preserve the form's original variable names.

    The job key stays the same on retries and is used as the message ID. Camunda
    deduplicates matching messages while their one-hour TTL remains active; this
    is not permanent exactly-once delivery. The receiving process must also handle
    duplicate submissions when persistence is connected.
    """
    variables = dict(job["variables"])
    correction = variables.get("isCorrection") is True
    if correction:
        variables["submissionKey"] = variables["originalSubmissionKey"]
    submission_key = variables.get("submissionKey")
    if not isinstance(submission_key, str) or not submission_key.strip():
        raise ValueError("The form must supply a non-empty submissionKey string.")
    payload = {
        "name": "product-resubmitted" if correction else "product-submitted",
        "correlationKey": submission_key,
        "messageId": f"submit-listing-{job['jobKey']}",
        "timeToLive": 3600000,
        "variables": variables,
    }
    if job.get("tenantId"):
        payload["tenantId"] = job["tenantId"]
    send(base_url, "messages/publication", payload)
    send(base_url, f"jobs/{job['jobKey']}/completion", {"variables": {"originalSubmissionKey": submission_key, "submissionKey": submission_key}})
    LOGGER.info("Submitted listing for job %s", job["jobKey"])


def run(base_url, once=False):
    while True:
        try:
            response = post(base_url, "jobs/activation", {
                "type": "submit-listing", "worker": "submit-listing-worker",
                "timeout": 120000, "maxJobsToActivate": 1, "requestTimeout": 10000,
            })
            for job in response.get("jobs", []):
                try:
                    submit_listing(job, base_url)
                except (ValueError, RuntimeError, OSError) as error:
                    LOGGER.error("Job %s failed: %s", job["jobKey"], error)
                    post(base_url, f"jobs/{job['jobKey']}/failure", {
                        "retries": max(job["retries"] - 1, 0),
                        "retryBackOff": 10000, "errorMessage": str(error)[:2000],
                    })
            if once:
                return
            if not response.get("jobs"):
                time.sleep(1)
        except (RuntimeError, URLError, OSError):
            if once:
                raise
            LOGGER.exception("Camunda request failed; retrying in five seconds")
            time.sleep(5)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--camunda-url", default=os.environ.get(
        "CAMUNDA_REST_URL", "http://camunda:8080/v2"))
    parser.add_argument("--once", action="store_true", help="Poll once, process any job, then exit")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    try:
        run(args.camunda_url, args.once)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
