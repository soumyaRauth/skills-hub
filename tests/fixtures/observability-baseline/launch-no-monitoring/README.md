# Bookshelf

Small reading-list app: sign in, add books, mark them read.

Launching publicly next week on Fly.io (`fly.toml`). Database is a managed
Postgres; `DATABASE_URL` is set as a Fly secret.

## Run locally

    DATABASE_URL=postgres://localhost/bookshelf npm start
