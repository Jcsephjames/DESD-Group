"""Publish an approved product through a caller-provided SQL connection."""


PRODUCT_FIELDS = (
    "name", "description", "category", "farm_origin", "price", "quantity",
    "availability_start", "availability_end", "best_before_date",
    "harvest_date", "organic", "certificate_id", "allergens",
)


def publish_product(product, connection, *, placeholder="%s"):
    """Insert an approved product and commit, rolling back on failure.

    The caller supplies a DB-API connection after validation and certificate
    checks pass. The products table/column mapping still needs alignment
    with the PostgreSQL schema. No tables or connections are created here.
    Use placeholder="?" for drivers that use question-mark parameters.
    The caller owns the connection; use a dedicated transaction for this call.
    """
    if not isinstance(product, dict) or not product:
        raise ValueError("A non-empty product is required.")
    if placeholder not in ("%s", "?"):
        raise ValueError("Supported SQL placeholders are %s and ?.")

    fields = [field for field in PRODUCT_FIELDS if field in product]
    if not fields:
        raise ValueError("Product contains no recognised fields.")
    statement = (
        f"INSERT INTO products ({', '.join(fields)}) "
        f"VALUES ({', '.join([placeholder] * len(fields))})"
    )
    values = tuple(product[field] for field in fields)
    cursor = connection.cursor()
    try:
        cursor.execute(statement, values)
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()

    return {"published": True}
