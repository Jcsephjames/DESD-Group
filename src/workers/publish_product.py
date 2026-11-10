"""Save a validated F1 submission and notify the waiting producer."""

from datetime import date
from decimal import Decimal

import psycopg

from submit_listing import post

PRODUCT_FIELDS = (
    "name", "description", "category", "farm_origin", "price", "quantity",
    "availability_start", "availability_end", "best_before_date",
    "harvest_date", "organic", "certificate_id", "allergens",
)


def publish_listing(job, base_url):
    variables = job["variables"]
    product = variables["standardisedProduct"]
    organic = product["organic"]
    if variables["detailsValid"] is not True or (organic and variables.get("certificateValid") is not True):
        raise ValueError("The listing has not passed validation and certification.")

    producer_id = variables["producerId"]
    submission_key = variables["submissionKey"]
    certification_status = "verified" if organic else "not_required"
    values = tuple(product.get(field) for field in PRODUCT_FIELDS)
    placeholders = ", ".join(["%s"] * len(PRODUCT_FIELDS))
    with psycopg.connect() as connection, connection.cursor() as cursor:
        cursor.execute(
            f"""
            INSERT INTO products (
                producer_id, submission_key, publication_status, certification_status,
                {', '.join(PRODUCT_FIELDS)}
            )
            VALUES (%s, %s, 'published', %s, {placeholders})
            ON CONFLICT (submission_key) DO NOTHING
            RETURNING id
            """,
            (producer_id, submission_key, certification_status, *values),
        )
        inserted = cursor.fetchone()
        if inserted:
            product_id = inserted[0]
            if organic:
                cursor.execute(
                    """
                    INSERT INTO certificate_checks (product_id, certificate_id, outcome)
                    VALUES (%s, %s, 'verified')
                    """,
                    (product_id, product["certificate_id"]),
                )
        else:
            # A retry can arrive after the database commit or message publication.
            cursor.execute(
                f"""
                SELECT id, {', '.join(PRODUCT_FIELDS)} FROM products
                WHERE submission_key = %s AND producer_id = %s
                  AND publication_status = 'published'
                """,
                (submission_key, producer_id),
            )
            existing = cursor.fetchone()
            expected = dict(product)
            expected["price"] = Decimal(product["price"])
            for field in ("availability_start", "availability_end", "best_before_date", "harvest_date"):
                if expected.get(field):
                    expected[field] = date.fromisoformat(expected[field])
            if not existing or existing[1:] != tuple(expected.get(field) for field in PRODUCT_FIELDS):
                raise ValueError("This submission key is already in use for a different listing.")
            product_id = existing[0]

    result = {
        "productId": product_id,
        "publicationStatus": "published",
        "verificationPending": False,
    }
    message = {
        "name": "listing-published",
        "correlationKey": submission_key,
        "messageId": f"listing-published-{job['jobKey']}",
        "timeToLive": 3600000,
        "variables": result,
    }
    if job.get("tenantId"):
        message["tenantId"] = job["tenantId"]
    post(base_url, "messages/publication", message)
    post(base_url, f"jobs/{job['jobKey']}/completion", {"variables": result})
