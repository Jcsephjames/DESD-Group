request_corrections.py

Job type: request-corrections

Workflow: Failed validation -> Request Corrections -> producer correction task -> resubmission -> validation again.

Publishes corrections-requested with the existing values, errors, readable summary, originalSubmissionKey and isCorrection=true. The correction form uses the same form ID. The marketplace waits for product-resubmitted with the same key.

The shared runner owns polling and technical failure handling. Only handlers in
runner.py HANDLERS are active. Do not start a second standalone polling process
when demonstrating the shared runner.
