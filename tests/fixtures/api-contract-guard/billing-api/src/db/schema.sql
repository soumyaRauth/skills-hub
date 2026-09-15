CREATE TABLE payments (
  id           TEXT PRIMARY KEY,
  account_id   TEXT NOT NULL,
  amount_cents INTEGER NOT NULL,
  currency     TEXT NOT NULL,
  status       TEXT NOT NULL,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE invoices (
  id           TEXT PRIMARY KEY,
  account_id   TEXT NOT NULL,
  amount_cents INTEGER NOT NULL,
  currency     TEXT NOT NULL,
  status       TEXT NOT NULL CHECK (status IN ('draft', 'open', 'paid', 'void')),
  due_at       TIMESTAMPTZ,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE refunds (
  id           TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
  account_id   TEXT NOT NULL,
  payment_id   TEXT NOT NULL REFERENCES payments(id),
  amount_cents INTEGER NOT NULL,
  status       TEXT NOT NULL DEFAULT 'pending',
  created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE idempotency (
  account_id TEXT NOT NULL,
  key        TEXT NOT NULL,
  response   JSONB NOT NULL,
  PRIMARY KEY (account_id, key)
);

CREATE TABLE api_keys (
  key_hash   BYTEA PRIMARY KEY,
  account_id TEXT NOT NULL
);
