"""Run the supported Camunda job handlers in one workers container."""

import logging
import os
import time

from submit_listing import post, submit_listing
from validate_product import validate_product
from request_corrections import request_corrections

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


HANDLERS = {'submit-listing': submit_listing, 'validate-product': validate_listing,
            'request-corrections': request_corrections}


def run(base_url):
    while True:
        found = False
        for job_type, handler in HANDLERS.items():
            try:
                response = post(base_url, 'jobs/activation', {
                    'type': job_type, 'worker': 'marketplace-workers',
                    'timeout': 120000, 'maxJobsToActivate': 1, 'requestTimeout': -1,
                })
                for job in response.get('jobs', []):
                    found = True
                    try:
                        handler(job, base_url)
                    except Exception as error:
                        LOGGER.exception('Handler failed for %s job %s', job_type, job['jobKey'])
                        post(base_url, f"jobs/{job['jobKey']}/failure", {
                            'retries': max(job['retries'] - 1, 0), 'retryBackOff': 10000,
                            'errorMessage': str(error)[:2000],
                        })
            except Exception:
                LOGGER.exception('Camunda request failed for %s', job_type)
                time.sleep(5)
        if not found:
            time.sleep(1)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    LOGGER.info('Listening for job types: %s', ', '.join(HANDLERS))
    try:
        run(os.environ.get('CAMUNDA_REST_URL', 'http://camunda:8080/v2'))
    except KeyboardInterrupt:
        pass
