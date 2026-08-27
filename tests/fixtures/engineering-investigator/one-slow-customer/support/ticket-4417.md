# Ticket 4417 — Northwind Logistics: "portal is unusably slow"

**Opened:** 2026-08-24
**Plan:** Enterprise · **Tenant:** northwind · **Users:** 34 seats

## Customer description

> The portal has been getting slower for about two weeks and is now close to
> unusable. Loading the dashboard takes forever. Our other web tools are fine.
> We have 34 people affected and we are reviewing our renewal.

## Notes

- 2026-08-24 — Asked whether it is one page or all of them. Reply: "the
  dashboard is the worst, everything is slower than it used to be."
- 2026-08-25 — Asked whether it happens for everyone in the office. Reply: "yes,
  everyone here. One of our directors says it is fine from home."
- 2026-08-26 — Their IT ran the command we sent, from a machine in the office:

```
$ curl -o /dev/null -s -w 'dns=%{time_namelookup} connect=%{time_connect} ttfb=%{time_starttransfer} total=%{time_total} size=%{size_download} speed=%{speed_download}\n' https://portal.example.com/api/dashboard
dns=0.024 connect=0.061 ttfb=0.173 total=6.594 size=1712004 speed=259632
```

- 2026-08-26 — No other tenant has reported slowness this month.
