"""Run the supported Camunda job handlers in one workers container."""

# This file is used to run the supported Camunda job handlers
# We give a list of Jobs we have defined in Camunda
# The runner cycles through these jobs asking Camunda on its interal network whether job_type = one of them
# If it does then it that relevant handler is called.

import logging
import os
import time

# We must import all handlers that are going to be used in the Camunda
from shared.camunda import post
from f1.submit_listing import submit_listing
from f2.fetch_product_names import fetch_product_names
from f2.update_product_stock import update_product_stock
from f1.validate_listing import validate_listing
from f1.request_corrections import request_corrections
from f1.publish_product import publish_listing
from f1.verification import mark_pending, notify_verification_unavailable, verify_certificate

LOGGER = logging.getLogger(__name__)

# Job types here must match the Job Types in the Camunda Graphs and Task Definitions in the .BPMN file
# These handlers are more often than not a Service Task in the Camunda Graphs.
# They will be a python script that is called by the runner.
# These Python scripts will be in the src/workers directory.
HANDLERS = {
    'fetch-product-names': fetch_product_names,
    'update-product-stock': update_product_stock,
    'submit-listing': submit_listing,
    'validate-product': validate_listing,
    'request-corrections': request_corrections,
    'verify-certificate': verify_certificate,
    'mark-pending': mark_pending,
    'notify-verification-unavailable': notify_verification_unavailable,
    'publish-product': publish_listing,
}


def run(base_url):
    """Poll Camunda for the job types in HANDLERS and run the matching handler.

    Each pass requests one waiting job per type from http://camunda:8080/v2.
    An empty pass waits one second before asking again.
    """
    while True:
        found = False
        for job_type, handler in HANDLERS.items():
            try:
                # Request one job at a time so its handler finishes before polling again.
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
