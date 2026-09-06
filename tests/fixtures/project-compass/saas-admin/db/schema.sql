CREATE TABLE organizations (
  id           TEXT PRIMARY KEY,
  name         TEXT NOT NULL,
  plan         TEXT NOT NULL DEFAULT 'starter',
  created_at   TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE users (
  id              TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  email           TEXT NOT NULL UNIQUE,
  role            TEXT NOT NULL DEFAULT 'member',
  created_at      TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE tickets (
  id              TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  author_id       TEXT NOT NULL REFERENCES users(id),
  subject         TEXT NOT NULL,
  body            TEXT NOT NULL,
  status          TEXT NOT NULL DEFAULT 'open',
  created_at      TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE refunds (
  id              TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  amount_cents    INTEGER NOT NULL,
  approved_by     TEXT REFERENCES users(id),
  created_at      TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE audit_log (
  id         TEXT PRIMARY KEY,
  actor_id   TEXT NOT NULL REFERENCES users(id),
  action     TEXT NOT NULL,
  target     TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE invoices (
  id              TEXT PRIMARY KEY,
  organization_id TEXT NOT NULL REFERENCES organizations(id),
  amount_cents    INTEGER NOT NULL,
  issued_at       TIMESTAMP NOT NULL DEFAULT now()
);
