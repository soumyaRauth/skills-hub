# Investigation — late order confirmation emails

## Report
"Order confirmation emails arrive late for some customers." — support ticket
4581, opened 2026-08-24

## Normalized symptom
Symptom     A fraction of order confirmation emails are sent ~30 min after the order
Who         All tenants; no pattern found by plan or region                  (E2)
Where       Production                                                       FACT
What        send-order-email jobs only; invoice PDFs unaffected              (E2)
Since       First complaint 2026-08-20; no confirmed earlier bound           PARTIAL
Frequency   Roughly 1 in 5 orders per support's sampling                     (E1)
Impact      Customers do not receive confirmation for ~30 min; no lost emails

## Capabilities
Available     repository, git history, worker log (logs/worker-2026-08-27.log),
              support ticket
Not available production Redis, SendGrid dashboard, production scheduler,
              staging environment

## Scope
Population all · Surface one job type · Time since ~08-20 · Persistence ~20% of attempts

## Status
Leading: H3 (queue backlog). Confidence Medium.
Open: H3, H4. Disproven: H1, H2. Blocked: H5.

Next: establish whether the delay is queue wait or job runtime — that single
measurement separates H3 from H4.
