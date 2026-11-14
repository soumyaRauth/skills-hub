# Core philosophy

The working beliefs behind every rule in `SKILL.md`. Read this when a
judgement call is not covered by a rule, or when someone asks why the skill
reasons the way it does.

## Contents

- Design with empathy
- One relationship, two kinds of product
- What "made for them alone" means
- The feelings a good experience leaves behind
- Simplicity is the removal of unnecessary effort
- The six confusions
- Challenging convention
- Empathy in the reasoning, not the vocabulary

## Design with empathy

Start with how a person feels while using what we build, and with what they
need that they may never say. A product that is functional but leaves people
anxious, lost or talked down to has failed at the part that matters most to
them. A book that is accurate but leaves readers feeling stupid has failed
the same way.

Empathy here is a working discipline, not a mood:

1. **Find out** who the person is and what they came for, from evidence where
   it exists.
2. **Imagine carefully** what the experience is like for them, and label that
   imagination as hypothesis.
3. **Inspect** what they actually meet, not what the creator intended.
4. **Change** what fails them, at the cause.
5. **Check** whether the change helped, with real people when it matters.

Steps 2 and 5 are where most "empathetic" reviews cheat: they present
imagination as knowledge, and stop before checking. This skill does neither.

## One relationship, two kinds of product

A software product and a book look unrelated. Both are a relationship between
a creator who knows a lot and a person who came for something:

| | Product | Book |
| --- | --- | --- |
| The person arrives with | a task, a problem, limited time | a question, a goal, limited background |
| The creator's blind spot | knowing how the system works | knowing the subject too well (the curse of knowledge) |
| Failure looks like | abandonment, errors, support tickets, distrust | confusion, skipped chapters, a book put down for good |
| Success looks like | the task done, the person feeling capable | the idea understood and used, the reader feeling capable |
| The journey | discovery, first use, core tasks, recovery, return | promise, first chapter, progression, practice, application |

Both are judged by the same ten dimensions (`empathy-scoring.md`). Only the
evidence differs: interactions for products, reading, learning and applying
for books.

## What "made for them alone" means

It does **not** mean a separate product or book for every person, and it does
not mean personalization features.

It means each person comes away feeling:

| Felt as | Instead of |
| --- | --- |
| Understood | stereotyped |
| Guided | controlled |
| Respected | manipulated |
| Capable | overwhelmed |
| Supported | abandoned |
| Valued | treated as a metric |

A plain, well-ordered tutorial can make a reader feel it was written for them,
because it starts where they are and answers the question they were about to
ask. A heavily personalized feed can make a person feel watched and handled.
Personal relevance never comes at the cost of privacy, autonomy,
accessibility or intellectual honesty.

## The feelings a good experience leaves behind

Self-determination theory names three needs that predict whether people stay
motivated: **autonomy** (I chose this and I am in control), **competence** (I
can do this) and **relatedness** (someone here understands me). They map onto
what this skill looks for:

- **Control:** the person can predict what will happen, undo it, leave and
  come back, and is never trapped or rushed.
- **Capability:** the next step is within reach; errors teach rather than
  scold; difficulty arrives with support.
- **Being understood:** the language, examples and defaults match their world,
  not the creator's.

Treat these as lenses for forming hypotheses, not as measurements. Whether a
specific person felt in control is known only by asking or observing them.

## Simplicity is the removal of unnecessary effort

Simplicity is not removing everything.

- A simple product removes **unnecessary** effort: fields nobody needs, steps
  that exist for the organization's convenience, decisions the system could
  make safely.
- A simple book makes complex ideas understandable **without destroying their
  depth**: the order is right, the prerequisites are there, the example comes
  at the moment it is needed.
- A simple explanation makes the underlying idea clearer; an oversimplified
  one makes it wrong.

Before cutting anything, separate **necessary complexity** (inherent in the
task or subject; it needs support, not removal) from **unnecessary
complexity** (added by the design, the writing or the organization; it needs
removal). Never simplify at the cost of correctness or usefulness. A
beginner's book that omits error handling to stay short has not simplified
the subject; it has moved the difficulty to the reader's first real program.

## The six confusions

| Never confuse | With | Because |
| --- | --- | --- |
| Functionality | usability | Every feature can work while nobody can find or finish it |
| Beauty | quality | An attractive page can be unreadable; a lovely diagram can obscure the idea |
| Simplicity | incompleteness | Removing what people need is not simplifying |
| Personalization | empathy | Tailoring without understanding is targeting |
| Content quantity | educational value | More pages often means more load and less learning |
| Technical sophistication | human value | Clever architecture the person never benefits from is cost, not value |

## Challenging convention

Conventions are compressed experience, and usually right. They are wrong when
the people or the context differ from the ones the convention was formed for.
Examples worth checking rather than assuming:

- A standard onboarding tour may be unnecessary for a tool people open to do
  one thing.
- A minimal interface may hide the one function an occasional user needs.
- A thorough book may overwhelm its beginners; a short one may leave them
  unable to finish a real project.
- A beautiful diagram may make a concept harder to understand than a plain
  sentence.
- A familiar pattern may fail a specific group: a drag-and-drop interaction
  for keyboard users; a "swipe to delete" for people with tremor.
- A personalization feature may violate the privacy expectations of the very
  people it is meant to delight.
- A technically efficient workflow may be mentally exhausting.

When you depart from a convention, say which convention, why it fails these
people here, and what evidence would show you were wrong.

## Empathy in the reasoning, not the vocabulary

A report that says "empathy" thirty times and invents a persona's feelings is
the opposite of this skill. Empathy shows in:

- naming a specific person and situation instead of "users";
- noticing the person at the edge of the audience;
- being exact about what is known and what is imagined;
- recommendations that cost the creator effort to save the person effort;
- telling the creator the uncomfortable truth, kindly and with evidence;
- tone toward the creator that is as respectful as the tone you ask them to
  use with their own users and readers.
