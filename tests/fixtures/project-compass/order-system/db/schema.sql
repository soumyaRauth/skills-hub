CREATE TABLE orders (
  id             TEXT PRIMARY KEY,
  customer_id    TEXT NOT NULL,
  total_cents    INTEGER NOT NULL,
  is_paid        BOOLEAN NOT NULL DEFAULT false,
  is_shipped     BOOLEAN NOT NULL DEFAULT false,
  is_cancelled   BOOLEAN NOT NULL DEFAULT false,
  is_refunded    BOOLEAN NOT NULL DEFAULT false,
  paid_at        TIMESTAMP,
  shipped_at     TIMESTAMP,
  cancelled_at   TIMESTAMP,
  created_at     TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE payments (
  id            TEXT PRIMARY KEY,
  order_id      TEXT NOT NULL REFERENCES orders(id),
  amount_cents  INTEGER NOT NULL,
  provider_ref  TEXT NOT NULL,
  created_at    TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE refunds (
  id            TEXT PRIMARY KEY,
  order_id      TEXT NOT NULL REFERENCES orders(id),
  amount_cents  INTEGER NOT NULL,
  created_at    TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE shipments (
  id          TEXT PRIMARY KEY,
  order_id    TEXT NOT NULL REFERENCES orders(id),
  carrier     TEXT NOT NULL,
  tracking    TEXT,
  created_at  TIMESTAMP NOT NULL DEFAULT now()
);
