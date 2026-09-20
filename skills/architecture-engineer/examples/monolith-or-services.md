# Example — "should this be microservices?"

The question that most reliably produces a fashionable answer instead of a
correct one. Illustrative.

---

**Request:**

> Should we split this into microservices?

---

## The two bad answers

> *"Yes — microservices give you independent scaling, deployability and fault
> isolation."*

> *"No — microservices are overkill and you should use a monolith."*

Both are answers to a question nobody asked, given without knowing the team
size, the deploy pipeline, what actually hurts, or whether anything needs to
scale independently. The second is right more often, which makes it more
dangerous: it is reflex disguised as wisdom.

## What actually decides it

Four questions, and the first is the only one that matters most of the time.

> 1. **What is the problem you are hoping this solves?** Splitting is a cost
>    that buys specific properties. If deploys are scary, the fix may be tests
>    and a pipeline rather than a network boundary.
> 2. **How many engineers, and do they collide?** Independent deployment is an
>    organizational property before a technical one. Four people on one codebase
>    rarely collide; forty do.
> 3. **Does any part need to scale, fail or deploy separately — with evidence?**
>    One CPU-bound component next to a mostly-idle app is a real reason. "The
>    system is big" is not.
> 4. **Who operates it on a bad night?** Distribution moves complexity from the
>    code into the spaces between services, where it is harder to see and needs
>    tooling most teams do not have yet.

## The answers

> *Deploys are scary — one bad change takes everything down. Six engineers. The
> PDF generation is heavy and occasionally makes the whole app slow. We deploy
> once a week because we're nervous.*

Three distinct problems, and only one of them is about architecture.

```
R-01  A bad change can take down the whole application         STATED
R-02  PDF generation degrades unrelated requests               STATED, and
      OBSERVED — sync call in the request path, workers/ unused
R-03  Six engineers, one codebase                              STATED
R-04  Weekly deploys, driven by fear rather than process       STATED
```

## The trade-off, stated plainly

> R-02 is real and has evidence. R-01 and R-04 are about confidence in
> deployment, and splitting the system makes both *worse* before better — you
> get more deploys to be nervous about, plus partial failures.
>
> - **A — extract PDF generation to a queue and worker.** Days of work. Fixes
>   R-02 completely: heavy work leaves the request path, and it can fail without
>   taking requests with it. One moving part, which you already have unused.
> - **B — split into services along module lines.** Weeks to months. Buys
>   independent deploys, which addresses R-01 only if the boundaries are right.
>   With six engineers and no service tooling, it also buys distributed tracing,
>   network failure modes, and cross-service versioning.
> - **C — do nothing structural; invest in tests and a deploy pipeline.** Fixes
>   R-01 and R-04, which is what you actually described as painful, and costs
>   no architecture at all.
>
> **I'd do A and C, and not B.** A is the only structural change the evidence
> supports. C addresses the fear directly — nervous weekly deploys are a testing
> and pipeline problem, and splitting the system does not make a bad change
> safer, it makes it smaller and more numerous.
>
> Worth saying: A is also the first step of B if you ever need it. Extracting
> the heavy component behind a queue is exactly the seam a service would use,
> so nothing here forecloses that.

No scores. Three options, priced in real units, with a recommendation and its
reason.

## The decision

```markdown
# D-002 — Extract PDF generation to a background worker; stay one deploy unit

Status    Accepted · 2026-09-20
Drivers   R-02 PDF generation degrades unrelated requests   STATED + OBSERVED
          R-03 six engineers on one codebase                STATED
Options   A worker · B split into services · C pipeline investment only
Chosen    A, plus C as non-architectural work
Why       A is the only split the evidence supports. B addresses deployment
          fear, which is a testing and pipeline problem, and adds distributed
          failure modes to a team with no service tooling
Trade-off PDF results become asynchronous — the UI needs a pending state
Reverses  Cheap. Call the generator inline and delete the worker
Revisit   If engineers start colliding, or a component needs to scale
          independently with evidence
```

## What this run did not do

- **Did not answer the question as asked.** "Should this be microservices" is
  rarely the real question; here it was three problems wearing one costume.
- **Did not recommend microservices**, and did not reflexively dismiss them —
  it named what B would buy and what it would cost.
- **Did not score the options.** A weighted total would have laundered the same
  judgment into arithmetic.
- **Did not treat a non-architectural answer as a failure.** The most useful
  recommendation here was tests and a deploy pipeline, which is not an
  architecture change at all.
- **Did note that the chosen option is the first step of the rejected one**,
  which is what makes it reversible.
