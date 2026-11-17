"""Load a producer's published listings for the F2 product selector."""

import psycopg

from shared.camunda import post


def fetch_product_names(job, base_url):
    producer_id = job["variables"].get("producerId")
    options = []
    if type(producer_id) is int and 1 <= producer_id <= 2**53 - 1:
        with psycopg.connect() as connection, connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, name
                FROM products
                WHERE producer_id = %s AND publication_status = 'published'
                ORDER BY name, id
                """,
                (producer_id,),
            )
            options = [
                {"label": f"{name} (#{product_id})", "value": str(product_id)}
                for product_id, name in cursor
            ]

    post(base_url, f"jobs/{job['jobKey']}/completion", {
        "variables": {
            "productOptions": options,
            "hasPublishedProducts": bool(options),
            "productLookupError": "" if options else "No published products found for that producer ID.",
        },
    })
