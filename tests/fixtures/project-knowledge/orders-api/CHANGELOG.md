# Changelog

## 0.3.0
- Charges moved from a nightly cron to the job queue: overlapping cron runs
  double-charged on long nights.

## 0.2.0
- Orders are marked paid by the webhook, not by the charge response.
