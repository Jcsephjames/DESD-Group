"""Update stock for an existing published listing."""

import psycopg

from shared.camunda import post


def update_product_stock(job, base_url):
    variables = job["variables"]
    producer_id = variables.get("producerId")
    product_id = variables.get("productId")
    if (isinstance(product_id, str) and len(product_id) <= 19
            and product_id.isascii() and product_id.isdecimal()):
        product_id = int(product_id)
    quantity = variables.get("quantity")

    if (type(producer_id) is not int or not 1 <= producer_id <= 2**53 - 1
            or type(product_id) is not int or not 1 <= product_id <= 2**63 - 1):
        error = "Enter positive whole-number producer and product IDs."
    elif type(quantity) is not int or not 0 <= quantity <= 2**31 - 1:
        error = "Enter a whole-number quantity between 0 and 2147483647."
    else:
        with psycopg.connect() as connection, connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE products
                SET quantity = %s
                WHERE id = %s AND producer_id = %s AND publication_status = 'published'
                RETURNING id
                """,
                (quantity, product_id, producer_id),
            )
            updated = cursor.fetchone()
        error = "" if updated else "No published product matches those IDs."

    post(base_url, f"jobs/{job['jobKey']}/completion", {
        "variables": {"stockUpdated": not error, "stockUpdateError": error},
    })
