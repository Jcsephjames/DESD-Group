"""Learning walkthrough only: no real Camunda, HTTP service, or database.

Camunda's job is to decide which step happens next.
A Python worker's job is to do the work requested at a service task.
This script simulates the process engine and workers.
"""
import argparse


def validate_product(product):
    """Simplified validation for the learning simulation."""
    errors = []
    if not product['name'].strip():
        errors.append('Product name is missing.')
    if product['price'] < 0:
        errors.append('Price cannot be negative.')
    return errors


def verify_certificate(certificate_id, attempt):
    """Pretend external service response, not real certificate verification."""
    if certificate_id == 'RETRY' and attempt == 1:
        return 'unavailable'
    if certificate_id in ('VALID', 'RETRY'):
        return 'valid'
    return 'invalid'


def save_listing(listings, product, status):
    """Pretend database: the same ID always updates the same entry."""
    listings[product['id']] = {**product, 'status': status}


def run_demo(scenario, pause=True):
    def step(who, message):
        print(f'\n[{who}] {message}')
        if pause:
            input('Press Enter to continue... ')

    product = {'id': 'demo-1', 'name': 'Carrots', 'price': 2.50,
               'organic': False, 'certificate': ''}
    listings = {}
    if scenario == 'correction':
        product['name'] = ''
    if scenario in ('certificate', 'outage'):
        product['organic'] = True
        product['certificate'] = 'INVALID' if scenario == 'certificate' else 'RETRY'

    print('\nLEARNING SIMULATION — nothing connects to Camunda or saves to disk.')
    step('USER / FORM', f'The producer submits: {product}')
    step('CAMUNDA', 'The process reaches Validate Product and creates a job for Python.')

    while True:
        errors = validate_product(product)
        step('PYTHON WORKER', f'Checks the details. Returns detailsValid = {not errors}.')
        if not errors:
            step('CAMUNDA / GATEWAY', 'Details are valid. Continue to the organic decision.')
            break
        step('CAMUNDA / GATEWAY', 'Details are invalid. Take the correction route.')
        step('USER / CORRECTION FORM', f'{errors[0]} The producer changes the name to Carrots and resubmits.')
        product['name'] = 'Carrots'
        step('CAMUNDA', 'Send the corrected details through validation again, keeping the same submission ID.')

    if product['organic']:
        step('CAMUNDA', 'Organic is true. Create a Verify Certificate job for Python.')
        attempt = 0
        while True:
            attempt += 1
            result = verify_certificate(product['certificate'], attempt)
            step('PYTHON WORKER / PRETEND EXTERNAL SERVICE', f'Certificate check returns: {result}.')
            if result == 'valid':
                step('CAMUNDA / GATEWAY', 'Certificate is valid. Continue to publication.')
                break
            if result == 'invalid':
                step('CAMUNDA', 'Certificate rejected. Ask the producer to correct it; do not publish.')
                step('USER / CORRECTION FORM', 'The producer replaces the certificate with VALID and resubmits.')
                product['certificate'] = 'VALID'
                step('PYTHON WORKER', f'Revalidates corrected details: detailsValid = {not validate_product(product)}.')
                step('CAMUNDA', 'Details are valid and organic is still true. Request verification again.')
                continue
            step('CAMUNDA / ERROR PATH', 'The worker reports service unavailability. Take the boundary-error route.')
            save_listing(listings, product, 'PENDING_VERIFICATION')
            step('PYTHON WORKER', 'Save one pending listing and notify the producer.')
            step('CAMUNDA / TIMER', 'Wait before retrying. In this demo, pressing Enter stands in for the timer.')
    else:
        step('CAMUNDA / GATEWAY', 'Organic is false. Skip certificate verification.')

    step('CAMUNDA', 'Create a Publish Product job for Python.')
    save_listing(listings, product, 'PUBLISHED')
    step('PYTHON WORKER', 'Save the published listing and send a publication notification.')
    step('CAMUNDA', 'The publication process finishes. Stock and seasonal availability are a separate process.')
    print(f'\nPretend database: {listings}')
    print(f'Number of listings: {len(listings)}. This data disappears when the script exits.')
    return listings


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('scenario', nargs='?', choices=['success', 'correction', 'certificate', 'outage'])
    parser.add_argument('--auto', action='store_true', help='Show the whole walkthrough without pausing')
    args = parser.parse_args()
    scenario = args.scenario
    if scenario is None:
        print('1. Publish a non-organic product\n2. Correct missing details\n3. Correct a rejected certificate\n4. Service outage, then retry')
        choice = input('Choose 1–4: ').strip()
        scenarios = {'1': 'success', '2': 'correction', '3': 'certificate', '4': 'outage'}
        if choice not in scenarios:
            parser.error('Choose 1, 2, 3, or 4.')
        scenario = scenarios[choice]
    run_demo(scenario, pause=not args.auto)
