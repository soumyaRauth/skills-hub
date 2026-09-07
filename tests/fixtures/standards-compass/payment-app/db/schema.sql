CREATE TABLE subscriptions (
  id                 uuid PRIMARY KEY,
  organization_id    uuid NOT NULL,
  stripe_customer_id text UNIQUE NOT NULL,
  status             text NOT NULL,
  current_period_end timestamptz
);

CREATE TABLE payments (
  id               uuid PRIMARY KEY,
  organization_id  uuid NOT NULL,
  stripe_charge_id text UNIQUE NOT NULL,
  amount_cents     integer NOT NULL,
  currency         text NOT NULL DEFAULT 'usd',
  card_brand       text,
  card_last4       text,
  status           text NOT NULL,
  created_at       timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE invoices (
  id              uuid PRIMARY KEY,
  organization_id uuid NOT NULL,
  number          text NOT NULL,
  total           numeric(12,2) NOT NULL,
  issued_at       timestamptz NOT NULL
);

CREATE TABLE invoice_lines (
  id         uuid PRIMARY KEY,
  invoice_id uuid NOT NULL REFERENCES invoices(id),
  descriptor text NOT NULL,
  unit_price numeric(12,2) NOT NULL,
  quantity   integer NOT NULL
);
