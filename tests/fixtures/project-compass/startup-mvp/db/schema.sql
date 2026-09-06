CREATE TABLE users (
  id         TEXT PRIMARY KEY,
  email      TEXT NOT NULL UNIQUE,
  created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE clients (
  id         TEXT PRIMARY KEY,
  user_id    TEXT NOT NULL REFERENCES users(id),
  name       TEXT NOT NULL,
  email      TEXT NOT NULL,
  portal_key TEXT
);

CREATE TABLE invoices (
  id           TEXT PRIMARY KEY,
  user_id      TEXT NOT NULL REFERENCES users(id),
  client_id    TEXT NOT NULL REFERENCES clients(id),
  number       TEXT NOT NULL,
  total_cents  INTEGER NOT NULL,
  paid_cents   INTEGER NOT NULL DEFAULT 0,
  status       TEXT NOT NULL DEFAULT 'draft',
  due_at       TIMESTAMP,
  sent_at      TIMESTAMP,
  created_at   TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE invoice_lines (
  id            TEXT PRIMARY KEY,
  invoice_id    TEXT NOT NULL REFERENCES invoices(id),
  description   TEXT NOT NULL,
  amount_cents  INTEGER NOT NULL
);

CREATE TABLE recurring_schedules (
  id           TEXT PRIMARY KEY,
  user_id      TEXT NOT NULL REFERENCES users(id),
  client_id    TEXT NOT NULL REFERENCES clients(id),
  every_days   INTEGER NOT NULL,
  template     JSONB NOT NULL,
  next_run_at  TIMESTAMP
);
