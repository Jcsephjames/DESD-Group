"""Map a Camunda form submission and complete its validation job."""

import logging

import psycopg

from submit_listing import post
from validate_product import validate_product

LOGGER = logging.getLogger(__name__)
FORM_FIELDS = {
    'productName': 'name', 'description': 'description', 'category': 'category',
    'farmOrigin': 'farm_origin', 'price': 'price', 'quantity': 'quantity',
    'availabilityStartDate': 'availability_start', 'availabilityEndDate': 'availability_end',
    'harvestDate': 'harvest_date', 'bestBeforeDate': 'best_before_date',
    'organicStatus': 'organic', 'certificateId': 'certificate_id', 'allergens': 'allergens',
}


def validate_listing(job, base_url, *, send=post):
    values = job['variables']
    product = {target: values[source] for source, target in FORM_FIELDS.items() if source in values}
    result = validate_product(product)
    if result['detailsValid']:
        producer_id = values.get('producerId')
        registered = False
        if type(producer_id) is int and 0 < producer_id <= 9223372036854775807:
            with psycopg.connect() as connection:
                registered = connection.execute(
                    'SELECT 1 FROM producers WHERE id = %s', (producer_id,),
                ).fetchone() is not None
        if not registered:
            result.update(
                detailsValid=False,
                standardisedProduct=None,
                validationErrors={'producer_id': 'Enter a registered producer ID.'},
            )
    # Invalid input is a completed business check, not a failed technical job.
    send(base_url, f"jobs/{job['jobKey']}/completion", {'variables': result})
    LOGGER.info('Validated job %s: detailsValid=%s', job['jobKey'], result['detailsValid'])

