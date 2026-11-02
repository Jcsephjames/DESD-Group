# PostgreSQL setup

PostgreSQL is defined as the `database` service in the root `docker-compose.yml`.
No local PostgreSQL installation or Python virtual environment is required to run it.

When ready, start only the database from the repository root:

```sh
docker compose up -d --wait database
```

The database and username are `marketplace`. The development password defaults to
`marketplace_dev`; override it with `POSTGRES_PASSWORD` in a root `.env` file before
first initialization. Workers connect to `database:5432`; connections from your
computer use `localhost:5432`.

The named `postgres_data` volume preserves records when containers are stopped or
recreated. `docker compose stop database` stops the service without deleting data.
Changing the configured password does not change an already initialized database password.

## Database Tables

Producers

id — bigint (automatically generated primary key)
name — text
email — text
farm_name — text
created_at — timestamptz

Products

id — bigint (automatically generated primary key)
producer_id — bigint (foreign key to producers.id)
submission_key — text
name — text
description — text
category — text
farm_origin — text
price — numeric(10, 2) (10 digits total, including 2 decimal places)
quantity — integer
availability_start — date
availability_end — date
harvest_date — date (optional)
best_before_date — date (optional)
allergens — text (optional)
organic — boolean
certificate_id — text (required when organic is true)
certification_status — text
publication_status — text
created_at — timestamptz

Certificate Checks

id — bigint (automatically generated primary key)
product_id — bigint (foreign key to products.id)
certificate_id — text
outcome — text
message — text (optional)
checked_at — timestamptz

timestamptz means timestamp with time zone. Fields marked optional allow NULL;
all other fields are required, with some supplied automatically by database defaults.
The status and outcome fields use text with CHECK constraints limiting allowed values.

## Empty schema

`init/schema.sql` defines `producers`, `products`, `certificate_checks` and the
`marketplace_products` view. There are no seed records or check scripts.
The SQL CHECK constraints in the schema enforce data rules such as non-negative
stock; these are separate from the removed check.sql test script.

On first startup with an empty data volume, PostgreSQL runs `init/schema.sql`
automatically. This creates the tables and view without inserting data. Existing
volumes are left untouched; schema edits are not applied automatically to them.
Workers use Europe/London for the connection timezone and seasonal dates.

The view shows published, in-season products, including zero-stock listings with
`available_for_orders = false`. Best-before withdrawal is not implemented.

The existing `publish_product.py` still needs producer ID, submission key,
publication/certificate-state handling and duplicate handling to match this schema.
The workers image installs its own Python dependencies and starts runner.py.
The backend application is not implemented yet.