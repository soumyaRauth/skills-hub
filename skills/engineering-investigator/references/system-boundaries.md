# System Boundaries

A symptom is observed at one point in a chain and caused at another. The chain
is long, and investigating all of it is how an investigation becomes a survey.

```
user → network → browser/device → frontend → CDN/proxy/LB → backend
     → database/cache → queues/workers → third parties → infrastructure
```

The rule is not *check every layer*. It is: **name the layers the evidence
implicates, visit those, and record why the others were excluded.**

## What each layer can produce

| Layer | Symptoms it produces | Cheapest observation |
| --- | --- | --- |
| Client network | Slow for one user, fine for others; large payloads slow, small fine; timeouts on upload | Transfer time vs server time for one request; throughput on the affected connection |
| Device / browser | Slow only on one browser or old devices; jank while the API is fast; one browser's errors | Same page on another browser/device; client-side timing |
| Frontend | Slow render with fast responses; wrong display of correct data; request waterfalls | Payload timing vs paint timing; count requests per interaction |
| CDN / proxy / LB | Regional differences; stale content; intermittent 502/504; timeouts at a round number | Response headers (cache status, served-by); same request bypassing the edge |
| Backend | Elevated server processing time; errors in application logs; failures on one endpoint | Server-side duration for the affected route; error log for the window |
| Database | Latency proportional to data size; slow under concurrency; lock and timeout errors | Query count and time per request; slow-query log; comparison against a prior version |
| Cache | First-request slowness; stale or inconsistent reads; thundering herd after eviction | Hit rate; behavior with cache warm vs cold |
| Queues / workers | Delayed effects rather than failed requests; duplicates; growing backlog | Queue depth over time; job latency from enqueue to completion |
| Third party | Failures correlated with one vendor call; provider error codes; latency inside one client | Error codes and durations attributed to that call; the provider's own status |
| Infrastructure | Symptoms after a deploy or scaling event; one instance misbehaving; resource ceilings | Per-instance comparison; deploy timeline; resource limits vs usage |

## Splitting a latency complaint

The single most valuable measurement in performance work is the split, because
every branch kills something:

```
total time
 ├─ DNS + connect + TLS      → network path, DNS, edge
 ├─ server processing (TTFB) → backend, database, third-party calls
 ├─ transfer                 → payload size, throughput, compression
 └─ render                   → frontend, device
```

Any tool that reports these — browser devtools, `curl -w`, a trace, an access
log with duration and bytes — resolves the first fork of most slowness
investigations in one shot.

```bash
curl -o /dev/null -s -w \
  'dns=%{time_namelookup} connect=%{time_connect} ttfb=%{time_starttransfer} total=%{time_total} size=%{size_download}\n' \
  "$URL"
```

Run it from a network resembling the affected one where possible; a fast office
connection cannot reproduce a slow client's transfer time.

## Boundary attribution

At every boundary, ask which side owns the time or the failure. Attribution
survives the whole investigation, so record it as a fact with its source:

```
E7  FACT  Checkout endpoint: server processing 148 ms, transfer 4.8 s,
          payload 1.9 MB · source: browser devtools, affected session
          → the time is not in our processing
```

Watch for boundaries that hide time: a slow third-party call inside your handler
looks like backend latency until it is attributed; a retry loop turns one
vendor timeout into three; a synchronous queue write turns a worker backlog into
request latency.

## Deciding it is not the application

The application can be exonerated — but only by evidence, and the shape of that
evidence is specific:

1. Our side is healthy **on the same window** the failures occupy — not
   healthy in general, and not healthy today for an incident that was yesterday.
2. The unaffected comparison exists: other users, regions, or requests on the
   same code path behave normally.
3. The external factor is measured, not assumed — throughput, provider error
   codes, edge headers, DNS resolution — with a number or a response.
4. No plausible application mechanism produces this pattern. State it, and say
   what would change your mind.

With 1–3, the honest level is HIGHLY LIKELY. With only 1, it is "no evidence of
an application-side problem yet", which is a different sentence and must be
written as one. See `communication.md` for how to say this without blaming
anyone.

## External causes worth naming

Network throughput, latency, packet loss, DNS failures or slow resolution, ISP
routing, VPN or corporate proxy interception, TLS interception by security
software, browser extensions, device CPU or memory limits, CDN edge behavior and
cache misses, regional connectivity, third-party API degradation or rate
limiting, expired credentials on an external service, and client clock skew.

Each of these has an observable signature. Name the signature you found, never
the category alone — "their internet" is not a finding; "4.8 s to transfer 1.9 MB
while server processing was 148 ms" is.
