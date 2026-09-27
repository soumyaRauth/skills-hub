# Contributing

Thanks for helping. These skills are plain markdown, so you don't need to install
anything or learn a codebase to contribute. If you can write clearly, you can help.

## Five steps

1. **Fork** the repository and create a branch.
2. **Make one change.** A sharper rule, a new example, a fixed typo, a new fixture.
3. **Run the check:** `./scripts/validate.sh` (it takes a few seconds).
4. **Open a pull request.** The template asks three short questions.
5. **Talk it through.** A maintainer reviews it and updates the changelog for you.

Not sure where to start, or want to propose something bigger first?
[Open an issue](https://github.com/soumyaRauth/skills-hub/issues/new/choose).
There are templates for a [new skill](.github/ISSUE_TEMPLATE/new-skill.md) and for
[improving one](.github/ISSUE_TEMPLATE/skill-improvement.md).

## Where things go

| You want to change | Edit |
| --- | --- |
| How a skill behaves | `skills/<skill>/SKILL.md` |
| Deeper guidance the skill reads when needed | `skills/<skill>/references/` |
| A worked example | `skills/<skill>/examples/` |
| Docs for people | `skills/<skill>/README.md` |
| A test repository for a skill | `tests/fixtures/<skill>/`, plus its expected findings in `tests/README.md` |
| When a skill should load, or stay quiet | `evals/activation/` |

When in doubt, put detail in `references/` and keep `SKILL.md` short.

## Five rules

Every review checks these. Each one links to the reason behind it.

1. **Evidence, not guesses.** Never make a skill list things that "might be related". [Why](.github/CONTRIBUTING-GUIDE.md#1-do-not-make-the-skills-more-speculative)
2. **No invented numbers.** No made-up counts, percentages or scores. [Why](.github/CONTRIBUTING-GUIDE.md#2-no-invented-numbers)
3. **No blanket language claims.** Not "native speakers say X", not "language Y always…". [Why](.github/CONTRIBUTING-GUIDE.md#3-no-unsupported-linguistic-claims)
4. **No compliance claims.** A skill never says a project *is* GDPR compliant, ISO certified, and so on. [Why](.github/CONTRIBUTING-GUIDE.md#4-no-compliance-certification-or-legal-claims)
5. **Quiet by default.** If your change makes a skill load more often, add a case where it must stay quiet. [Why](.github/CONTRIBUTING-GUIDE.md#5-activation-is-earned)

Also: keep examples generic, with no employer code or internal names.

## Going deeper

The **[full guide](.github/CONTRIBUTING-GUIDE.md)** explains what makes a good
contribution for each kind of change: failure scenarios, standards registry
entries, language examples, fixtures, activation cases, and how to test a skill
against a fixture. You only need the section for what you are changing.

## Be kind

Be straightforward and civil. Review contributions on evidence, the same way the
skills review code.
