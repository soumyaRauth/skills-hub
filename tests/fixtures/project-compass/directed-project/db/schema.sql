CREATE TABLE warehouses (id TEXT PRIMARY KEY, name TEXT NOT NULL);

CREATE TABLE adjustments (
  id            TEXT PRIMARY KEY,
  warehouse_id  TEXT NOT NULL REFERENCES warehouses(id),
  sku           TEXT NOT NULL,
  delta         INTEGER NOT NULL,
  state         TEXT NOT NULL DEFAULT 'draft'
                CHECK (state IN ('draft', 'submitted', 'approved', 'rejected')),
  submitted_by  TEXT,
  approved_by   TEXT,
  approved_at   TIMESTAMP,
  created_at    TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE reconciliations (
  id            TEXT PRIMARY KEY,
  warehouse_id  TEXT NOT NULL REFERENCES warehouses(id),
  period        DATE NOT NULL,
  counted_total INTEGER NOT NULL,
  system_total  INTEGER NOT NULL,
  closed_at     TIMESTAMP,
  UNIQUE (warehouse_id, period)
);
