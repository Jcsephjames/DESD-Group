BEGIN;

CREATE TABLE producers (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name text NOT NULL CHECK (btrim(name) <> ''),
    email text NOT NULL UNIQUE,
    farm_name text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE products (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    producer_id bigint NOT NULL REFERENCES producers(id),
    -- Reuse the same submission key when retrying a Camunda task.
    submission_key text NOT NULL UNIQUE CHECK (btrim(submission_key) <> ''),
    name text NOT NULL CHECK (btrim(name) <> ''),
    description text NOT NULL CHECK (btrim(description) <> ''),
    category text NOT NULL CHECK (btrim(category) <> ''),
    farm_origin text NOT NULL CHECK (btrim(farm_origin) <> ''),
    price numeric(10, 2) NOT NULL CHECK (price >= 0 AND price <> 'NaN'::numeric),
    quantity integer NOT NULL CHECK (quantity >= 0),
    availability_start date NOT NULL,
    availability_end date NOT NULL,
    harvest_date date,
    best_before_date date,
    allergens text,
    organic boolean NOT NULL DEFAULT false,
    certificate_id text,
    certification_status text NOT NULL DEFAULT 'not_required'
        CHECK (certification_status IN ('not_required', 'pending', 'verified', 'failed', 'unavailable')),
    publication_status text NOT NULL DEFAULT 'draft'
        CHECK (publication_status IN ('draft', 'pending_verification', 'rejected', 'published')),
    created_at timestamptz NOT NULL DEFAULT now(),
    CHECK (availability_end >= availability_start),
    CHECK (harvest_date IS NULL OR best_before_date IS NULL OR best_before_date >= harvest_date),
    CHECK (
        (NOT organic AND certificate_id IS NULL AND certification_status = 'not_required')
        OR (organic AND certificate_id IS NOT NULL AND btrim(certificate_id) <> ''
            AND certification_status <> 'not_required')
    ),
    CHECK (publication_status <> 'published' OR NOT organic OR certification_status = 'verified')
);

CREATE INDEX products_producer_idx ON products(producer_id);

-- Each request records the certificate that was actually checked, even if edited later.
CREATE TABLE certificate_checks (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id bigint NOT NULL REFERENCES products(id),
    certificate_id text NOT NULL CHECK (btrim(certificate_id) <> ''),
    outcome text NOT NULL CHECK (outcome IN ('verified', 'failed', 'unavailable')),
    message text,
    checked_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE producers (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name text NOT NULL CHECK (btrim(name) <> ''),
    email text NOT NULL UNIQUE,
    farm_name text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX certificate_checks_product_idx ON certificate_checks(product_id);

-- Query this view for the customer listing: zero stock stays visible; out of season does not.
-- Dates are inclusive. Best-before withdrawal is not implemented.
CREATE VIEW marketplace_products AS
SELECT p.*, (quantity > 0) AS available_for_orders
FROM products p
WHERE publication_status = 'published'
  AND CURRENT_DATE BETWEEN availability_start AND availability_end;

COMMIT;
