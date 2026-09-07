# Internal standards — template

Copy this file to `references/internal-standards.md` inside the installed skill,
or to `.project-standards/internal-standards.md` in your project, and fill it in.

Internal standards **outrank everything in the registry**. They are the rules
your organization has actually agreed to, and where they conflict with a general
framework, they win — with the conflict noted, not silently resolved.

Delete every section you do not have. An empty template is better than an
invented one, and inventing organizational rules is the fastest way to make this
skill wrong.

---

## Organizational context

```
Industry
Jurisdictions we operate in
Where our users are
Do we hold or pursue an ISMS (ISO 27001) or SOC 2 report?
Do customers require specific certifications?
Regulated data we handle
```

Filling in these seven lines removes most of the `POTENTIALLY APPLICABLE`
ambiguity from every future assessment.

## Standards we have committed to

```
Standard / framework      Version    Why           Scope        Owner
```

## Standards we have explicitly decided not to pursue

```
Standard      Reason                          Revisit if
```

Recording the negatives is as valuable as recording the positives — it stops
every assessment re-raising the same question.

## Our security requirements

Things stricter than, or different from, the general frameworks. For example:

- Password hashing algorithm and parameters we require
- Session lifetime and idle timeout
- Where secrets must live, and how they rotate
- Which encryption is mandatory, for which data
- Authorization pattern all services must use
- What must be audit logged
- Dependency policy — allowed registries, update cadence, license constraints

## Our accessibility target

```
Target level
Scope (which surfaces)
Manual testing cadence, and who does it
Known and accepted exceptions
```

## Our privacy rules

```
Data categories we allow ourselves to collect
Retention periods, by category
Deletion guarantees we have made to customers
Approved sub-processors
What must never be logged
```

## Our AI rules

```
Approved providers and models
Data that must never reach a model
Whether provider training on our data is permitted
Human review requirements, by decision type
Logging and retention of prompts and outputs
```

## Architecture rules

```
Patterns that are mandatory
Patterns that are forbidden
Approved technologies
Things requiring architecture review before use
```

## Exceptions already granted

```
What            Why            Compensating control      Expires      Approved by
```

## How to treat conflicts

When an internal standard is stricter than a framework, assess against the
internal one and note the framework as also satisfied. When it is *looser*, say
so plainly and let the team decide:

> Your internal standard allows a 30-day session lifetime; ASVS would suggest
> shorter for an application handling this data. Assessed against your standard
> as `PASS`, flagged here so the decision is visible rather than accidental.
