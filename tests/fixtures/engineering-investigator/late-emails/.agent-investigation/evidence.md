# Evidence

## E1
FACT — Five forwarded confirmation emails have header timestamps 28–34 minutes
after their order time. Support estimates ~1 in 5 orders affected.
Source: support/ticket-4581.md (customer-supplied headers).
Impact: establishes the delay magnitude; the rate is an estimate, not a measurement.

## E2
FACT — Only `send-order-email` jobs are implicated; `render-invoice-pdf` jobs in
the same period complete normally. No tenant, plan, or region pattern in the
sampled orders.
Source: logs/worker-2026-08-27.log, sampled by job name.
Impact: narrows scope to one job type; weakens any host-wide explanation.

## E3
FACT — Sends that eventually succeed record `provider_status=202` and a runtime
of ~2.2 s. The lateness is present before the provider is called.
Source: logs/worker-2026-08-27.log, `job_finished` lines.
Impact: disproves H1.

## E4
FACT — `job_enqueued` timestamps follow order creation within about a second for
both delayed and on-time orders.
Source: logs/worker-2026-08-27.log, `job_enqueued` vs order ids in the admin export.
Impact: disproves H2.

## E5
ASSUMPTION — The 2026-08-27 log is representative of the behavior reported since
08-20. Earlier logs have rotated out.
Risk: if 08-27 is atypical, rate and pattern conclusions drawn from it are wrong.
