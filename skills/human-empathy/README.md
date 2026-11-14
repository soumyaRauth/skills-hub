# Human Empathy

**Design with empathy: understand the person first, then build for them.**

Human Empathy is an [Agent Skill](https://code.claude.com/docs/en/skills) that
evaluates and improves how people experience what you make, whether that is a
software product or a book. It starts with who the user or reader is and what
they came for, walks the experience as that person, separates what it observed
from what it imagines, and turns what it finds into specific changes. When you
ask, it makes those changes too.

```bash
npx skills add soumyaRauth/skills-hub --skill human-empathy
```

---

## The problem

```
"It works."          ≠  people can finish it
"It looks great."    ≠  people can read it
"It's all in there." ≠  people can learn it
```

Most reviews check the artifact: does the form submit, does the PDF render,
is every topic covered. The expensive failures are in the person's
experience. The form wipes ten fields when the server hiccups. The beginner's
book puts nine new concepts into the first listing of chapter 3, and that
listing does not run. The premium PDF theme draws `--reload` as a dash, so a
beginner types a dash.

Each of those passes a functional check. Each one makes a real person give
up, and usually blame themselves.

## What it does

```
the person → their situation and needs → the real experience (run it, read it, render it)
   → walk it as them → findings with evidence levels → root causes
   → empathy scores from a documented rubric → specific changes → re-check
```

- **Products:** journeys, onboarding, forms, errors, empty and loading
  states, microcopy, emotional experience, accessibility as lived, privacy
  and deceptive patterns, whether each feature serves a real need.
- **Books and documents:** reader fit and promise, structure, learning
  progression, cognitive load, explanation, practice, editorial quality,
  technical accuracy (it runs the code), typography and layout on rendered
  pages, PDF navigation and accessibility, publication readiness. It can also
  help plan and write a new book, starting from the reader.

## Honest by construction

| It does | It never does |
| --- | --- |
| Labels every claim `VERIFIED`, `SUPPORTED`, `HYPOTHESIS` or `PREFERENCE` | Invent user research, reader quotes, personas presented as real, statistics or citations |
| Says what it did not inspect | Call a change "validated with users" when no person tested it |
| Scores ten dimensions against a published rubric, with evidence and confidence | Average scores into a precise-looking number, or score what it could not observe |
| Executes code examples and reports `EXECUTED`, `CHECKED` or `UNVERIFIED` | Call code correct because it looks correct |
| Renders PDF pages and looks at them | Judge layout from extracted text |
| Proposes direction changes and waits | Change a book's audience, a chapter order, a product's data collection or consent on its own |
| Tells you plainly when the design or the manuscript is failing people | Agree to please |

## Modes

| You ask | It runs | Writes |
| --- | --- | --- |
| *"Walk through sign-up as a new user."* | Journey evaluation | No |
| *"Should we add streaks?"* | Proposed feature evaluation | No |
| *"Make our error states kinder."* | Empathy improvement | Code |
| *"Is this flow ready for users?"* | Pre-release experience review | No · verdict |
| *"Review my book."* | Full book evaluation | No |
| *"Readers get lost in chapter 3. Why?"* | Chapter-level evaluation | No |
| *"Is the PDF easy to read?"* | PDF visual review | No |
| *"Fix chapter 3 so beginners can follow it."* | Book improvement | Manuscript, after approval for direction changes |
| *"Help me write a book on X for Y."* | Book creation | Plan first, then chapters |
| *"Is this ready to publish?"* | Publication readiness | No · verdict |

## When it activates

| | |
| --- | --- |
| **Engages** | Questions about how people experience a product, feature, flow, document or book; UX or experience reviews; why people abandon or struggle; improving a journey; whether a feature serves real needs; planning, writing, reviewing, editing or improving a book, chapter, tutorial, course, documentation or PDF for its readers |
| **Stays quiet** | A label change, a typo, a grammar fix, a spacing tweak, or any single mechanical edit nobody framed as an experience question; features with no user-facing experience in question; questions about how code works |
| **Depth** | `ACTIVE` in its modes · `CONSULT` (two or three lines) when a build request names its people and an experience risk would change the build · `GATING` only for a readiness verdict you asked for |
| **Works with** | `standards-compass` (WCAG, PDF/UA, consent and privacy obligations), `practical-localizer`, `proof-driven-dev`, `project-compass`, `production-guard` |

## Example

```
You:  People keep giving up halfway through our sign-up. Walk through it as a
      new user would and tell me what it's like.

Agent: ⚡ Human Empathy — sign-up journey review; support tickets describe lost input

       F1  People lose everything they typed when sign-up fails        Critical · HIGH
           VERIFIED: setForm(initial) in the catch block (SignupForm.jsx:38);
           ticket #4812 describes it and the abandonment that followed
           Fix: keep every field on error; move focus to the message

       F2  An existing customer is told "something went wrong"         High · HIGH
           VERIFIED: every non-OK status throws one message (api.js:9)
       …
       Overall 2 · Significant weaknesses (median 2 of 8; capped: Respect = 1) · MEDIUM
       Not inspected: the running product. Validate with three think-aloud
       sessions on phones.
```

Full worked examples: [a registration flow](examples/product-evaluation.md) ·
[a technical book for beginners](examples/book-evaluation.md) ·
[improving a chapter](examples/chapter-improvement.md) ·
[an attractive, unreadable PDF](examples/pdf-visual-review.md) ·
[staying quiet](examples/stays-quiet.md).

## Inside the skill

| File | What it holds |
| --- | --- |
| [`SKILL.md`](SKILL.md) | Activation, rules, modes and the workflow |
| [`references/core-philosophy.md`](references/core-philosophy.md) | Design with empathy, "made for them alone", simplicity, the six confusions |
| [`references/human-research.md`](references/human-research.md) | Understanding people, evidence levels, validation methods |
| [`references/product-evaluation.md`](references/product-evaluation.md) | Journeys, interactions, states, microcopy, trust, proposed features |
| [`references/book-evaluation.md`](references/book-evaluation.md) | Reader, promise, architecture, chapter review |
| [`references/learning-experience.md`](references/learning-experience.md) | Progression, explanation, practice, cognitive load, confidence |
| [`references/editorial-standards.md`](references/editorial-standards.md) | Clarity, tone, terminology, editing without imposing a style |
| [`references/pdf-design-and-accessibility.md`](references/pdf-design-and-accessibility.md) | Typography, layout, code, navigation, PDF accessibility, the rendering tool ladder |
| [`references/technical-accuracy.md`](references/technical-accuracy.md) | Running code and commands, versions, security in examples, citations |
| [`references/book-creation.md`](references/book-creation.md) | The twelve-stage lifecycle from reader research to publication readiness |
| [`references/empathy-scoring.md`](references/empathy-scoring.md) | Ten dimensions, five levels, anchors, the overall rule |
| [`references/implementation-guidelines.md`](references/implementation-guidelines.md) | Changing products and manuscripts safely |
| [`references/reporting.md`](references/reporting.md) | Report template, finding format, severity, verdicts |

## Limitations

- It cannot know how people feel. It can find what is likely to cause a
  feeling, say why, and tell you how to find out.
- Without the running product it reads code, and says so; visual and timing
  findings are then inferred.
- Visual PDF review needs something that renders pages (poppler, PyMuPDF,
  Ghostscript or a headless browser). Without one it limits itself to what
  the source proves and asks for screenshots.
- Conformance with WCAG, PDF/UA or privacy law is not its call; it hands the
  evidence to `standards-compass`.
- It writes and edits in any language the model handles well, but its
  judgements about natural phrasing in a language other than English carry
  lower confidence unless the project or the author supplies conventions.

## License

MIT
