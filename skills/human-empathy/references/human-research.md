# Understanding people, and knowing what you know

How to build a working picture of the user or reader, how to label what that
picture rests on, and how to recommend research that would replace guesses
with evidence.

## Contents

- Questions to answer before evaluating anything
- Where the evidence comes from
- The four evidence levels
- Building a person profile without inventing one
- Variation inside an audience
- Emotional claims
- Validation methods, and which question each answers
- What inspection alone cannot establish

## Questions to answer before evaluating anything

For a product user or a book reader alike:

| Question | Product phrasing | Book phrasing |
| --- | --- | --- |
| Who is it for? | Which people use this, and in which role? | Who is the reader, and why did they pick this book up? |
| What are they trying to do? | The job: what progress do they want in their situation? | The outcome: what will they be able to do afterwards? |
| Why does it matter to them? | What happens if they fail or give up? | What problem made them buy or open it? |
| What do they already know? | Domain, the product, similar tools | Prerequisites, vocabulary, adjacent skills |
| What do they expect? | From similar products, from the marketing | From the title, subtitle, cover copy, table of contents |
| What gets in their way? | Time, device, connection, permissions, stress | Time, fatigue, missing background, reading environment |
| What will they misunderstand? | Terms, icons, states, consequences | Terms, notation, assumed steps, ambiguous instructions |
| What do they need functionally? | To complete the task correctly | To understand, practise and apply |
| What do they need emotionally? | Confidence, control, reassurance, respect | Confidence, patience, curiosity, no humiliation |
| What limitations affect them? | Abilities, assistive tech, language, literacy | Reading ability, language, screen readers, print vs screen |
| What would make it valuable? | The job done with less effort and worry | Real capability gained, worth the time and money |
| What would make them feel understood? | It speaks their language and anticipates their situation | It starts where they are and answers the question they were about to ask |

Jobs to Be Done is useful framing for the "trying to do" row: describe the
progress a person wants in a circumstance ("when I finish a client project, I
want to send a correct invoice quickly so I get paid without chasing"), not a
feature ("use the invoice builder").

## Where the evidence comes from

In rough order of strength for questions about people:

1. **Direct research the person supplies:** interview notes, usability test
   recordings or notes, reader feedback, reviews, support tickets, survey
   results, analytics, learning assessment results.
2. **Traces in the artifact:** the README or product brief, marketing copy,
   the book's introduction and prerequisites, onboarding questions, analytics
   events (which show what someone *wanted* to measure, not the results),
   issue trackers, FAQ pages (each FAQ is a recorded confusion).
3. **Established research and convention:** cognitive load theory, usability
   heuristics, readability and typography conventions, accessibility
   guidance, deceptive-pattern taxonomies. These support inferences about
   people in general, never facts about these people.
4. **Your reasoning** about the situation. Valuable, and always labelled.

Read what exists before inferring. A `support/` folder, a `feedback.md`, an
analytics export or a reviews file changes the evidence level of everything
built on it.

## The four evidence levels

Every finding and every claim about people carries one:

| Level | Means | Example |
| --- | --- | --- |
| `VERIFIED` | Observed directly in the artifact, or stated in research the person supplied | "The form clears every field when the server returns an error (`SignupForm.jsx:88`)." · "Two of the three supplied reader notes say they stopped at section 3.2." |
| `SUPPORTED` | An inference from verified facts plus named established research or convention | "Clearing a nine-field form on error is very likely to cause abandonment: re-entry cost is high and the user did nothing wrong (well-established form-usability finding)." |
| `HYPOTHESIS` | Plausible, untested, and could be wrong in either direction | "Freelancers may hesitate at the company-size field because it implies the product is for agencies." |
| `PREFERENCE` | Taste or style, with no evidence that it changes the experience | "A warmer colour for the success state." |

Rules:

- A fact about the artifact can be `VERIFIED`. A fact about how people react
  to it can only be `VERIFIED` by research involving people.
- Supplied research is evidence of what those people said or did. Two reader
  notes are not "readers"; say "two of the supplied reader notes".
- Name the research or convention behind a `SUPPORTED` claim in a few words.
  Never invent a study, an author, a statistic or a percentage.
- `PREFERENCE` findings go last, and only if asked or clearly worth it.

## Building a person profile without inventing one

A profile is useful as a lens for the walkthrough. It becomes harmful when it
is presented as research. Write it like this:

```
PERSON (ASSUMED, from the README and landing copy; no user research supplied)
  Who        Freelance designers and developers, solo, invoicing 2–10 clients
  Goal       Send a correct first invoice the same day they sign up
  Knows      Their own work; not accounting terms
  Context    Often on a phone, between other tasks; may be anxious about getting paid
  Edge       Uses a screen reader · on a prepaid mobile connection · English is a second language
  Unknown    Whether most sign-ups come from mobile; what they expect the product to cost
```

- Keep a line for **Unknown**. It is where recommended research comes from.
- Never give a profile a name, a photo, a quote or an age unless they came
  from real research. Invented specifics create false confidence.
- One primary person plus the edge cases is usually enough. Add another only
  when their needs genuinely diverge (an administrator and an end user; a
  beginner and an experienced reader of the same book).

## Variation inside an audience

People in one audience differ in ways that change the verdict:

- **Experience:** first-time vs returning; beginner vs expert (what helps a
  beginner can slow an expert, and the reverse: the expertise reversal effect).
- **Abilities:** vision, hearing, motor control, cognition, attention, memory,
  temporary and situational limits (a broken arm, a sunny screen, a noisy
  train, a baby on one arm).
- **Context:** device, screen size, connection speed, time pressure, privacy
  of the setting, stress.
- **Language and culture:** reading in a second language, literal
  interpretation of idioms, date and name formats, cultural meaning of
  colours and imagery.
- **Literacy and numeracy**, including technical and financial literacy.

Check the experience for at least one person at an edge. An experience that
works for the edge usually works better for everyone; one that works only for
the centre excludes people silently.

## Emotional claims

Statements about feelings are the most tempting to invent and the most
damaging when wrong.

- Write them as what the design is **likely to cause**, with the mechanism:
  "Losing all nine fields after a server error is likely to feel punishing:
  the user did nothing wrong and pays for it in effort." Not: "Users feel
  furious."
- Ground them in observable behaviour where possible: abandonment, retries,
  support tickets, rage clicks, reviews, a reader's own words.
- Distinguish **frustration** (blocked goal), **anxiety** (uncertainty about
  consequences, often around money, data or irreversible actions),
  **confusion** (no working model), **shame** (made to feel incompetent) and
  **distrust** (feeling handled or deceived). Each needs a different fix.

## Validation methods, and which question each answers

Recommend the cheapest method that would answer the open question:

| Method | Answers | Not good for |
| --- | --- | --- |
| User or reader interviews | Goals, context, expectations, vocabulary, why they came | Whether a design works (people predict their behaviour poorly) |
| Moderated usability testing (think-aloud, five or so people per round is a common starting point) | Where people stall and why, in a specific flow | How often it happens across the whole population |
| Reading comprehension testing | Whether readers can explain or apply a concept after a section | Whether they enjoyed it |
| Learning assessments and exercises with answers checked | Whether the book's outcomes are achieved | Why they were not |
| Contextual observation | Real environment, interruptions, workarounds | Rare events |
| Surveys | How widespread a known issue or attitude is | Discovering issues you have not thought of |
| Behavioural analytics | Where people drop off, how often, on which devices | Why they drop off |
| Feedback and review analysis | Recurring themes in what people volunteer | The silent majority who left without a word |
| Accessibility testing with assistive-technology users | Whether people with disabilities can complete the task | Conformance on its own (that is `standards-compass`'s audit) |
| Beta readers, technical reviewers | Clarity and correctness of a manuscript before release | Statistical confidence |

For each recommended method, say what question it answers, who to involve,
and what result would change the recommendation.

## What inspection alone cannot establish

Say so explicitly when it matters to a conclusion:

- How many people experience a problem, or how often.
- How people actually feel, as opposed to how the design is likely to make
  them feel.
- Whether readers understood a concept or can apply it.
- Which of several plausible causes of abandonment is the real one.
- Whether a proposed feature will be used or valued.
- Whether an experience works with a specific assistive technology, unless
  you tested it.
