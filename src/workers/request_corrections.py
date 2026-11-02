"""Notify the waiting producer process that its submission needs correction."""
from submit_listing import post


def request_corrections(job, base_url, *, send=post):
    values = dict(job['variables'])
    key = values['submissionKey']
    errors = values.get('validationErrors') or {}
    summary = '\n'.join(f"- {field.replace('_', ' ')}: {message}" for field, message in errors.items())
    values.update(isCorrection=True, originalSubmissionKey=key,
                  validationErrorSummary=summary or 'Please correct the certification details or remove the organic claim.')
    payload = {'name': 'corrections-requested', 'correlationKey': key,
               'messageId': f"request-corrections-{job['jobKey']}",
               'timeToLive': 3600000, 'variables': values}
    if job.get('tenantId'):
        payload['tenantId'] = job['tenantId']
    send(base_url, 'messages/publication', payload)
    send(base_url, f"jobs/{job['jobKey']}/completion", {})
