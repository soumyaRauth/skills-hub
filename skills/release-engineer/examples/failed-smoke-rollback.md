# Example — a failed smoke check, and the rollback

Production Guard returned SHIP for commit `a4c2e7f`. The human said *deploy it*.
The rollback was drilled on staging last week. Fly.io, one app per environment.

---

## 1. Deploy

```
$ fly deploy --app shop-prod --image ghcr.io/acme/shop@sha256:c19e…
...
$ ./deploy/smoke.sh https://shop.example/health
curl: (22) The requested URL returned error: 503
... (5 retries)
curl: (22) The requested URL returned error: 503
exit 22
```

## 2. Roll back immediately

A failed smoke check triggers the recorded rollback without asking: it undoes
the deploy that was just authorized, and waiting leaves users on the broken
version. The previous image comes from Fly's own release list, not from memory:

```
$ fly releases --app shop-prod --image        # output abridged
v42  failed?  ghcr.io/acme/shop@sha256:c19e…
v41  ...      ghcr.io/acme/shop@sha256:91d0…
$ fly deploy --app shop-prod --image ghcr.io/acme/shop@sha256:91d0…
$ ./deploy/smoke.sh https://shop.example/health
{"ok":true}
```

## 3. The report

```
⚡ Release Engineer — production smoke failed; rolled back

RELEASE      production · ghcr.io/acme/shop@sha256:c19e…  (commit a4c2e7f)
RAN          fly deploy ✓ · smoke ✗
MIGRATIONS   1 applied (0012_add_refund_reason — expand; left in place, old code ignores it)
SMOKE        GET https://shop.example/health → 503 on all 6 attempts
ROLLED BACK  fly deploy --image …@sha256:91d0… · smoke → 200
ROLLBACK     fly deploy --app shop-prod --image <previous from fly releases --image>
```

The migration stays: it was an expand step, and the old code runs against it.
Had it been a contract step, the rollback would not have been safe, and the
reply would say so instead of rolling back blindly.

## 4. Hand over

The deploy output shows no cause. Staging passed with the same digest, so
the difference is in production:

```
HANDOFF → engineering-investigator: sha256:c19e… healthy on staging, 503 on production; rolled back, production on sha256:91d0…
HANDOFF → delivery-planner: T-019 back to in_progress; production deploy rolled back
```

## What did not happen

- No second deploy attempt "in case it was transient".
- No guess at the cause in the RELEASE block.
- No down-migration.
- No claim that production is healthy beyond what the smoke check shows: a 200
  from `/health`.
