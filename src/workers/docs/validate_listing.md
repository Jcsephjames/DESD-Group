validate_listing.py

Job type: validate-product

Workflow: Submission Received -> Validate and Standardise Details -> Details valid? gateway.

Maps camelCase form keys to the snake_case keys expected by validate_product.py. Calls that function and completes the job with detailsValid, validationErrors and standardisedProduct. Invalid input is a normal result; technical exceptions are failed jobs.

The shared runner owns polling and technical failure handling. Only handlers in
runner.py HANDLERS are active. Do not start a second standalone polling process
when demonstrating the shared runner.
