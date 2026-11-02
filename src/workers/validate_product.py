"""Standardize product details first, then validate them."""

import argparse
from datetime import datetime
from decimal import Decimal, InvalidOperation
import json
import re
from pathlib import Path
import sys


def standardize_date(value):
    """Convert accepted dates to YYYY-MM-DD; leave invalid values for validation."""
    if not isinstance(value, str):
        return value
    value = value.strip()
    for date_format in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(value, date_format).date().isoformat()
        except ValueError:
            continue
    return value


def standardize(product):
    """Return a copy with consistent text, dates and numbers.

    Invalid values are kept so validation can report them without silently
    rounding prices, truncating quantities or changing the original input.
    """
    product = product.copy()

    # Text fields
    for field in ("name", "description", "category", "farm_origin", "certificate_id", "allergens"):
        if isinstance(product.get(field), str):
            product[field] = product[field].strip()

    # Date fields
    for field in ("best_before_date", "availability_start", "availability_end", "harvest_date"):
        if field in product:
            product[field] = standardize_date(product[field])

    # Price: keep currency exact and use two decimal places when possible.
    price = as_decimal(product.get("price"))
    if price is not None and price.is_finite():
        try:
            if price == price.quantize(Decimal("0.01")):
                product["price"] = format(price, ".2f")
        except InvalidOperation:
            pass  # Validation below reports unsupported precision.

    # Quantity: convert whole numeric values to integers.
    quantity = as_decimal(product.get("quantity"))
    if quantity is not None and quantity.is_finite():
        if quantity == quantity.to_integral_value():
            product["quantity"] = int(quantity)

    # Clear an old certificate when the producer removes their organic claim.
    if product.get("organic") is False:
        product["certificate_id"] = None

    return product


def as_decimal(value):
    """Read a numeric value without treating booleans as numbers."""
    if isinstance(value, bool) or not isinstance(value, (str, int, float, Decimal)):
        return None
    try:
        return Decimal(str(value).strip())
    except InvalidOperation:
        return None


def valid_date(value):
    if not isinstance(value, str):
        return False
    try:
        return datetime.strptime(value, "%Y-%m-%d").date().isoformat() == value
    except ValueError:
        return False


def required_error(product, field, label):
    """Explain why a required value is absent before checking its format."""
    if field not in product:
        return f"{label} field is missing."
    value = product[field]
    if value is None:
        return f"{label} field is null; a value is required."
    if isinstance(value, str) and not value.strip():
        return f"{label} field is empty."
    return None


def validate_product(product):
    """Standardize first, then run all validation checks."""
    if not isinstance(product, dict):
        return {
            "detailsValid": False,
            "validationErrors": {"product": "Product must be a JSON object."},
            "standardisedProduct": None,
        }

    product = standardize(product)
    errors = {}

    # Required text
    for field, label in (
        ("name", "Name"), ("description", "Description"),
        ("category", "Category"), ("farm_origin", "Farm origin"),
    ):
        problem = required_error(product, field, label)
        if problem:
            errors[field] = problem
        elif not isinstance(product[field], str):
            errors[field] = f"{label} must be text."

    # Price
    price = as_decimal(product.get("price"))
    problem = required_error(product, "price", "Price")
    if problem:
        errors["price"] = problem
    elif price is None:
        errors["price"] = "Price must be a number, such as 2.50."
    elif not price.is_finite():
        errors["price"] = "Price cannot be NaN or infinity."
    elif price < 0:
        errors["price"] = "Price cannot be negative."
    else:
        try:
            if price != price.quantize(Decimal("0.01")):
                errors["price"] = "Price must have no more than two decimal places."
        except InvalidOperation:
            errors["price"] = "Price exceeds supported decimal precision."

    # Quantity
    quantity = as_decimal(product.get("quantity"))
    problem = required_error(product, "quantity", "Quantity")
    if problem:
        errors["quantity"] = problem
    elif quantity is None:
        errors["quantity"] = "Quantity must be a number."
    elif not quantity.is_finite():
        errors["quantity"] = "Quantity cannot be NaN or infinity."
    elif quantity < 0:
        errors["quantity"] = "Quantity cannot be negative."
    elif quantity != quantity.to_integral_value():
        errors["quantity"] = "Quantity must be a whole number; fractional units are not allowed."

    # Required and optional dates
    for field in ("availability_start", "availability_end", "best_before_date", "harvest_date"):
        value = product.get(field)
        label = field.replace("_", " ").capitalize()
        if field in ("best_before_date", "harvest_date") and value in (None, ""):
            product.pop(field, None)
            continue
        problem = required_error(product, field, label)
        if problem:
            errors[field] = problem
        elif not isinstance(value, str):
            errors[field] = f"{label} must be a date supplied as text."
        elif not valid_date(value):
            if re.fullmatch(r"(?:\d{4}-\d{1,2}-\d{1,2}|\d{1,2}/\d{1,2}/\d{4})", value):
                errors[field] = f"{label} is not a real calendar date; check the day, month and year."
            else:
                errors[field] = f"{label} has an incorrect date format; use YYYY-MM-DD or DD/MM/YYYY."

    start = product.get("availability_start")
    end = product.get("availability_end")
    if "availability_start" not in errors and "availability_end" not in errors:
        if start > end:
            errors["availability_end"] = "Availability end must be on or after its start."

    harvest = product.get("harvest_date")
    best_before = product.get("best_before_date")
    if "harvest_date" not in errors and "best_before_date" not in errors:
        if harvest and best_before and harvest > best_before:
            errors["best_before_date"] = "Best-before date must be on or after harvest."

    # Organic claim and certificate
    organic = product.get("organic")
    problem = required_error(product, "organic", "Organic claim")
    if problem:
        errors["organic"] = problem
    elif not isinstance(organic, bool):
        errors["organic"] = "Organic claim must be the JSON boolean true or false, without quotes."
    elif organic:
        certificate = product.get("certificate_id")
        problem = required_error(product, "certificate_id", "Certificate ID")
        if problem:
            errors["certificate_id"] = f"{problem} A certificate ID is required when organic is true."
        elif not isinstance(certificate, str):
            errors["certificate_id"] = "Certificate ID must be text."

    if "allergens" in product:
        if product["allergens"] in (None, ""):
            product.pop("allergens")
        elif not isinstance(product["allergens"], str):
            errors["allergens"] = "Allergens must be text."

    # Return only product fields; identity belongs to the surrounding process.
    fields = (
        "name", "description", "category", "farm_origin", "price", "quantity",
        "availability_start", "availability_end", "best_before_date",
        "harvest_date", "organic", "certificate_id", "allergens",
    )
    return {
        "detailsValid": not errors,
        "validationErrors": errors,
        "standardisedProduct": None if errors else {
            field: product[field] for field in fields if field in product
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", nargs="?", type=Path, help="Product JSON file; otherwise read stdin")
    args = parser.parse_args()
    try:
        raw = args.file.read_text(encoding="utf-8") if args.file else sys.stdin.read()
        product = json.loads(raw, parse_float=Decimal)
    except (OSError, ValueError) as error:
        parser.exit(2, f"Cannot read product JSON: {error}\n")
    print(json.dumps(validate_product(product), indent=2))


if __name__ == "__main__":
    main()
