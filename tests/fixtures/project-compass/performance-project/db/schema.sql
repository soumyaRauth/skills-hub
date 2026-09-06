CREATE TABLE organizations (id TEXT PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE warehouses (id TEXT PRIMARY KEY, organization_id TEXT NOT NULL, name TEXT NOT NULL);
CREATE TABLE products (id TEXT PRIMARY KEY, sku TEXT NOT NULL);
CREATE TABLE users (id TEXT PRIMARY KEY, email TEXT NOT NULL);

CREATE TABLE adjustments (
  id              TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  warehouse_id    TEXT NOT NULL REFERENCES warehouses(id),
  product_id      TEXT NOT NULL REFERENCES products(id),
  created_by      TEXT NOT NULL REFERENCES users(id),
  amount_cents    INTEGER NOT NULL,
  created_at      TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX adjustments_org_idx ON adjustments (organization_id);
