# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); this repository ships
instructions rather than executable code, so versions describe changes in
methodology and documentation.

## [Unreleased]

## [0.3.0] — 2026-08-23

### Added

- `practical-localizer` skill: a context-aware application localization
  methodology with three modes — ANALYZE (read-only inventory and plan),
  LOCALIZE (writes localization resources only), REVIEW (findings with
  recommendations)
- Four-way strategy classification per term — translate, transliterate,
  preserve, adapt — chosen from context, existing project terminology and the
  target locale's software conventions rather than from a blanket rule
- Blocking technical validation: placeholder parity across every syntax
  (`{name}`, `{{name}}`, `%s`, `%1$s`, `:name`, `<0>…</0>`), plural-category
  coverage per locale, key and structure preservation. Placeholder *order* is
  deliberately not checked, because verb-final languages move the interpolation
- Terminology management and translation memory: established project terms win
  over new synonyms, and conflicts are reported with occurrence counts
- Explicit prohibition on native-authority claims and blanket language rules;
  HIGH/MEDIUM/LOW confidence on every non-trivial decision
- References: localization workflow, translation strategy, terminology, context
  analysis, pluralization, locale formatting, RTL, UI fit, confidence, review
  methodology
- Templates: `glossary.yml`, `locale-profile.yml`, `review-report.md`
- Five worked language examples: Bengali, Hindi, Japanese, Arabic, and a
  European three-language pass — each stating what it does not claim
- Six test fixtures with intentionally bad localizations (`basic-json`,
  `nextjs`, `react`, `laravel`, `i18next`, `mixed-localization`) and documented
  expected findings

### Changed

- `scripts/validate.sh` validates a skill's `templates/` directory when one is
  present
- Top-level README, `tests/README.md` and `CONTRIBUTING.md` cover three skills;
  CONTRIBUTING gains a third hard rule against unsupported linguistic claims
- Documentation site gains a Practical Localizer page

## [0.2.0] — 2026-08-20

### Added

- `production-guard` skill: a 14-phase production-readiness validation workflow
  producing a report that ends in 🟢 SHIP, 🟠 CONDITIONAL SHIP, or 🔴 DO NOT SHIP
- Verdict derived from explicit rules rather than judgement; four-level severity
  (blocker, high, medium, low) with evidence, confidence, and recommendation on
  every finding
- Mandatory `EXECUTED` vs `ANALYZED` labelling, so reasoning is never presented
  as an observed test result
- Baseline establishment, so pre-existing failures are never blamed on the change
- Explicit prohibition on invented quality scores, enforced by the validator
- Risk-based depth (low / medium / high) selecting which categories run
- References: behavioral validation, failure analysis, security validation, data
  integrity, performance, observability, report schema, change-type checklists
- Team customization template (`team-standards.template.md`)
- Five worked examples: payment, bulk operation, API change, database migration,
  authentication — one ending in SHIP
- Four test fixtures containing intentional production bugs (payment,
  bulk-operation, api, migration) with documented expected findings

### Changed

- Fixtures are now grouped per skill: `tests/fixtures/<skill>/<name>/`
- `scripts/validate.sh` discovers every skill under `skills/` instead of
  hardcoding one; adds orphan-reference, invented-score, and per-skill fixture
  checks
- Top-level README is now a two-skill catalog
- `tests/README.md` and `CONTRIBUTING.md` cover both skills

## [0.1.0] — 2026-08-20

Initial release.

### Added

- `impact-map` skill: an 11-phase read-only blast-radius analysis workflow
  producing an evidence-based impact report
- Five-way finding classification (must change, likely affected, needs
  verification, hidden coupling, out of scope) with separate High/Medium/Low
  confidence tracking
- Hidden-coupling analysis: raw strings, raw SQL, direct data access, duplicated
  business logic, configuration, events, jobs, serialization, fixtures,
  generated code, documentation
- Normal and deep analysis modes
- Reference documents: report schema, dependency analysis, hidden coupling,
  framework detection
- Team customization template (`company-architecture.template.md`)
- Four worked examples: simple business logic, API response, database schema,
  cross-module enterprise workflow
- Four test fixtures (`simple-node`, `nextjs`, `laravel`, `mixed-architecture`)
  with documented expected findings
- `scripts/validate.sh` and a GitHub Actions workflow running it

[Unreleased]: https://github.com/soumyaRauth/skills-hub/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/soumyaRauth/skills-hub/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/soumyaRauth/skills-hub/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/soumyaRauth/skills-hub/releases/tag/v0.1.0
