# Workers

One container starts `python runner.py`. The runner polls Camunda, selects the
handler by job type, and reports technical failures with a reduced retry count.
Each handler is in its own Python file. Validation rules stay in validate_product.py;
validate_listing.py is the adapter between those rules and Camunda jobs.

Worker workflows:

- [Submission](docs/submit_listing.md)
- [Validation adapter](docs/validate_listing.md)
- [Correction requests](docs/request_corrections.md)
- [Certificate verification helper](docs/verification.md)
- [Product publication helper](docs/publish_product.md)

The first three are connected. Verification and publication helpers are not yet
registered in the runner, so valid submissions wait at those BPMN tasks.

From the repository root:

```sh
docker compose up -d --build workers
docker compose logs -f workers
```

Compose starts the required Camunda, Elasticsearch and PostgreSQL services.
The workers folder is mounted at /app. The Dockerfile installs requirements.txt.
The runner connects through CAMUNDA_REST_URL, normally http://camunda:8080/v2.
PostgreSQL connection details are supplied through PGHOST, PGPORT, PGDATABASE,
PGUSER and PGPASSWORD. Inside a container, localhost means that same container.

For a standalone validation check:

```sh
docker compose exec workers python validate_product.py mock.json
```

Use a unique submissionKey for each new listing. Corrections keep the original
key and resume the existing marketplace instance. Process versions already running
retain their deployed definitions; start a new instance after BPMN changes.
