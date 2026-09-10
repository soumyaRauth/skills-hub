# Decision debt

Technical debt is code that is expensive to change. Decision debt is a question
nobody answered, which every implementation then answers on its own, differently.

It is worse than technical debt in one specific way: technical debt is visible
in the code, and decision debt is visible only in the *pattern* of the code. One
inconsistent conditional looks like an inconsistent conditional. Six of them
across three modules are a question that was never asked out loud.

## What it looks like

Always the same shape — an unanswered question resurfacing as an implementation
detail:

```
"What counts as an active user?"          → three definitions, three features
"When is an order complete?"              → paid? shipped? delivered? settled?
"Can an approved application be edited?"  → the UI says yes, the API says no
"Who owns an organization's data?"        → answered four times, never the same
"What happens when payment succeeds
 but fulfillment fails?"                  → nothing. Nobody decided.
"Is a cancelled subscription readable?"   → depends which endpoint you ask
```

Each was answered locally by whoever hit it first, in the way that made that one
feature work. The answers are not wrong. They are *unrelated*, and users
eventually find the seam.

## Detecting it

The signal is the same question surfacing in different clothes.

```bash
git log --format='%s' -n 200 | grep -icE 'edge case|special case|for now|temporarily'
grep -rn "isActive\|is_active\|active ==" src/ | wc -l
grep -rnE '\b(TODO|FIXME|HACK|XXX)\b.*\?' src/
```

Three cheap reads, each of which turns up decision debt faster than reading the
architecture:

- **Divergent definitions.** The same predicate implemented more than once. Diff
  the implementations; if they disagree, the question was never answered.
- **Growing conditionals.** A branch that gains a clause per feature. Each clause
  is a decision made under pressure.
- **Comment questions.** `// should this include archived?` is decision debt with
  a timestamp on it. `git blame` gives you the age.
- **Contradicting layers.** UI permits, API forbids. Someone will report it as a
  bug, and the fix will be another local decision.

## Pricing it

Decision debt compounds because *every* subsequent feature pays interest —
whoever builds next has to guess, and guesses diverge.

Raise it when:

```
It has resurfaced three times, in three places, and you can name them
   AND it is blocking or distorting work already asked for
   AND the answer is one sentence a human can produce today
```

Do not raise it when the question is genuinely open at the business level and
nobody is waiting. Some questions are correctly unanswered — write them down and
leave them.

## Asking it well

The single highest-leverage skill here is phrasing. A question that costs a
meeting gets deferred; a question that costs a sentence gets answered.

```
Bad    "The lifecycle semantics of the application entity are underspecified.
        We should schedule a discussion about the state model."

Good   "Can an approved application still be edited? The UI allows it, the API
        blocks it, and the export includes edits either way. If it is no, I will
        add an explicit reopen action that gets audited."
```

Four properties make the difference:

1. **One question**, not a topic.
2. **Show the contradiction** — the reason it must be answered by them and not
   by you.
3. **Offer a default** so the answer can be a single word. Most of the time the
   default is accepted, and the whole intervention cost is five seconds.
4. **Say what you will do with the answer.** It converts an abstract decision
   into a concrete consequence.

## Recording it

Answered → `decisions.md`, with what it constrains. Unanswered → `open-questions.md`,
with what it blocks and the default you would take if nobody answers.

The default matters more than it looks. It converts a blocking question into a
non-blocking one: the work proceeds on the recorded default, and the record is
what makes it reversible later, on purpose, instead of discovered by a customer.

```markdown
## Can an approved adjustment be edited?
Impact      High — permissions, audit trail, reporting totals
Blocks      bulk edit (asked 2026-09-02), the approval UI
Surfaced    3× — src/api/adjustments.ts:140, ui/EditPanel.tsx:22, no test at all
Default     No, with an explicit audited reopen. Proceeding on this.
Answered by one sentence from whoever owns the process
```

## Requirement debt

The same thing, one level up: business rules getting defined *accidentally*,
through implementation, without anyone deciding they are the rules.

It is visible when features independently invent statuses, permissions,
notification triggers, or exceptions — and then those inventions become the
product's behavior, permanently, because customers start depending on them.

Say it plainly, once:

> The rules for what a manager can approve now live in four conditionals, and
> they do not agree with each other. Whatever they add up to is currently the
> product's actual policy — worth deciding whether it is the one we want.

## What this is not

- Not an ADR process. One sentence in a file beats a template nobody fills in.
- Not a reason to block work. Record the default and proceed.
- Not an observation. "This question is unanswered" is where the finding starts;
  "answer it in one sentence before the bulk-edit work, and here is the default
  I would take" is where it becomes useful.
- Not a demand for specifications up front. Decision debt is priced when it
  starts charging interest, not when it is created — some of it never does.
