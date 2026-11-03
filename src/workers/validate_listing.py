"""Map a Camunda form submission and complete its validation job."""

import logging
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
    # Invalid input is a completed business check, not a failed technical job.
    send(base_url, f"jobs/{job['jobKey']}/completion", {'variables': result})
    LOGGER.info('Validated job %s: detailsValid=%s', job['jobKey'], result['detailsValid'])

