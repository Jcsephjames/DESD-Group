# Workers

The workers container mounts `src/workers` at `/app`, its working directory.
Its Dockerfile installs `requirements.txt` when the image is built. Psycopg is
the PostgreSQL driver; the existing validation and HTTP code use Python's standard
library and need no additional packages. The runner uses the Camunda REST API through Python’s standard library.

From the repository root, when ready to start the containers:

```sh
docker compose up -d --build workers
docker compose exec workers python validate_product.py mock.json
```

Starting workers also starts PostgreSQL and waits for it to be healthy.
The container runs runner.py, which dispatches submit-listing and validate-product jobs. Database connection settings use the Compose service name `database`,
not `localhost`. They are available through the standard `PG*` environment
variables for `psycopg.connect()` calls.


# Workers List

- `validate_product.py`: standardise and validate product details.
- `verification.py`: send a certificate ID to the certification service.
- `publish_product.py`: insert an approved product using a supplied SQL connection.



## Validate Product



## Send a certificate

```sh
python3 src/workers/verification.py src/workers/mock.json --service-url http://localhost:8001/verify
```

Replace the example URL with the certification service endpoint, or set
`CERTIFICATION_SERVICE_URL`. Input can also be supplied as JSON on stdin.
The worker sends a JSON POST body such as `{"certificate_id": "CERT-123"}`
and prints the service's JSON response. The request times out after 10 seconds.
Request failures exit with status 2 so the caller can handle retries separately
from certificate rejection. The service endpoint and response schema still need
to be agreed with the certification service implementation.


## Publish a product

Call `publish_product(product, connection)` after product validation
and any required certificate verification succeed. Supply the
`standardisedProduct` object from validation, rather than the full result.
The worker uses parameterised SQL, commits on success, rolls back on failure,
and returns `{"published": true}`. Errors propagate so the caller can handle them.
The caller supplies and closes a DB-API connection dedicated to this operation.
The default parameter marker is `%s`; pass `placeholder="?"` for drivers that
require it.

The publication worker still needs alignment with the PostgreSQL schema. This worker does not create a database,
tables, credentials, or connections, and adds no dependencies. It is an insert
only; duplicate handling for retries after an uncertain commit is not implemented.

## Submit listing worker

`submit_listing.py` listens for the `submit-listing` job type and publishes a
`product-submitted` message with the form variables, correlated by `submissionKey`.
It completes the job only after publication succeeds. Failed jobs reduce retries;
zero retries creates a Camunda incident. Message deduplication lasts for the message's
one-hour TTL, so persistent duplicate handling is still needed later.

Run inside the existing workers container:

```sh
docker compose exec workers python submit_listing.py
```

The default endpoint is `http://camunda:8080/v2`. Override `CAMUNDA_REST_URL` or pass
`--camunda-url` if needed. `--once` performs one activation request then exits.
This uses only Python's standard library; no new dependency is needed.
Compose now starts runner.py automatically. The F1 Submit Listing service
task and marketplace product-submitted message start are wired. Validation is connected through runner.py. Later worker handlers are not connected yet.

## Shared runner

Compose and the Dockerfile start `python runner.py`. The runner polls both
`submit-listing` and `validate-product` job types in one container. Validation maps
the current form field names to the existing validate_product function and completes
the job with detailsValid, validationErrors and standardisedProduct. Invalid input
completes with detailsValid=false; technical failures reduce job retries.

Rebuild/start with `docker compose up -d --build workers` and inspect progress with
`docker compose logs -f workers`. No extra Python dependencies are required.
Certification and publication handlers are not implemented yet;
the process waits when it reaches one of those job types.

## Correction loop

The runner also handles `request-corrections` using `request_corrections.py`.
It sends the validation errors and a readable summary to the producer process.
The producer opens `Correct Product Details`, reusing `Prod-sub-form` and its values.
The submission worker sends `product-resubmitted` for corrections, keeping the
original submission key even if the form's key field was edited. The existing
marketplace instance receives that message and validates again.

Start a new producer instance on the latest deployed version to use this loop.
Older versions without the correction user task are blocked from automatic
resubmission to prevent loops. Certification/publication handlers remain pending.
