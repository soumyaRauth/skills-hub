# Example — a large request that is not a run

## Request

> Add subscription billing with Stripe: plans, trials and cancellation.

The repository has `.delivery/` with a plan and tickets.

## What happens

Nothing here loads. The request is one piece of work, however large. Standards
Compass, Dependency Guard, API Contract Guard and ProofBuild engage because this
request earns them, each at its own depth. No ticket is picked, no branch is
named `t/…`, no ledger is written.

If billing belongs in the plan, `delivery-planner` may notice and offer a
ticket. That is its call.

## When it would engage

- *"Work through the backlog."*
- *"Take the next ticket."*
- *"Keep going until M1 ships."*
- *"Build the whole thing from the plan."*
- *"Use delivery-lead."*

And not for `/skills-pipeline …`, which runs one sequence the user picks, once.
