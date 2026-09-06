CREATE TABLE projects (
  id         TEXT PRIMARY KEY,
  name       TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE tasks (
  id          TEXT PRIMARY KEY,
  project_id  TEXT NOT NULL REFERENCES projects(id),
  title       TEXT NOT NULL,
  assignee_id TEXT,
  status      TEXT NOT NULL DEFAULT 'todo',
  priority    TEXT NOT NULL DEFAULT 'normal',
  due_at      TIMESTAMP,
  labels      TEXT[],
  created_at  TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE saved_views (
  id         TEXT PRIMARY KEY,
  user_id    TEXT NOT NULL,
  name       TEXT NOT NULL,
  filters    JSONB NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT now()
);
