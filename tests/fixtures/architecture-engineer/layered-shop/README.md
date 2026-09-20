# layered-shop

Order management service.

## Structure

    src/domain/          entities and business rules, no framework dependencies
    src/application/     use cases, orchestration
    src/infrastructure/  persistence, external services
    src/api/             HTTP handlers — thin, delegate to application/

Dependencies point inward: api → application → domain. Infrastructure is wired
in at the edges and the domain never imports it.
