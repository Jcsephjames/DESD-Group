submit_listing.py

Job type: submit-listing

Workflow: Form completion -> Submit Listing -> message publication -> producer waits for response.

Reads the form variables. Initial submissions publish product-submitted; isCorrection=true publishes product-resubmitted using originalSubmissionKey. The job completes only after publication succeeds. Message IDs reduce duplicates for the one-hour TTL; they do not guarantee permanent exactly-once delivery.

The shared runner owns polling and technical failure handling. Only handlers in
runner.py HANDLERS are active. Do not start a second standalone polling process
when demonstrating the shared runner.
