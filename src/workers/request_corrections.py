"""Notify the waiting producer process that its submission needs correction."""
from submit_listing import post


def request_corrections(job, base_url, *, send=post):
    # we work from a copy of the job variables to avoid mutating the Camunda job state
    # the original job variables are immutable and should not be changed directly
    # We duplicate the submission key to keep the original submission traceable in the correction flow.
    values = dict(job['variables'])
    key = values['submissionKey']

    # Turn validation issues into a readable summary for the producer to fix.
    errors = values.get('validationErrors') or {}
    summary = '\n'.join(
        f"- {field.replace('_', ' ')}: {message}"
        for field, message in errors.items()
    )

    # Flag this as a correction flow and keep the original submission key for traceability.
    # The producer will see the summary of validation errors and can correct them before resubmitting.
    values.update(
        isCorrection=True,
        originalSubmissionKey=key,
        validationErrorSummary=summary or 'Please correct the certification details or remove the organic claim.',
    )

    # Publish the correction request event.
    
    payload = {
        'name': 'corrections-requested',
        'correlationKey': key,
        'messageId': f"request-corrections-{job['jobKey']}",
        'timeToLive': 3600000,
        'variables': values,
    }
    if job.get('tenantId'):
        payload['tenantId'] = job['tenantId']
    send(base_url, 'messages/publication', payload)
    send(base_url, f"jobs/{job['jobKey']}/completion", {})
