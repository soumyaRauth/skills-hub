CREATE TABLE customers (
  id            SERIAL PRIMARY KEY,
  email         TEXT NOT NULL UNIQUE,
  name          TEXT,
  plan          TEXT,
  region        TEXT,
  status        TEXT NOT NULL DEFAULT 'active',
  last_seen_at  TIMESTAMP,
  created_at    TIMESTAMP NOT NULL DEFAULT now(),
  deleted_at    TIMESTAMP
);

CREATE TABLE staff (
  id        SERIAL PRIMARY KEY,
  email     TEXT NOT NULL UNIQUE,
  role      TEXT NOT NULL DEFAULT 'support'
);

CREATE TABLE staff_groups (
  id          SERIAL PRIMARY KEY,
  name        TEXT NOT NULL,
  can_manage  BOOLEAN NOT NULL DEFAULT false
);

CREATE TABLE staff_group_members (
  group_id  INTEGER NOT NULL REFERENCES staff_groups(id),
  staff_id  INTEGER NOT NULL REFERENCES staff(id)
);

CREATE TABLE saved_segments (
  id          SERIAL PRIMARY KEY,
  staff_id    INTEGER NOT NULL REFERENCES staff(id),
  name        TEXT NOT NULL,
  plan        TEXT,
  status      TEXT
);
