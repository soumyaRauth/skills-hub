# Evaluating products, features and journeys

How to inspect a digital product as the person using it: what to look at,
how to get at it in a codebase, and the questions each area must answer.

## Contents

- Getting at the real experience
- The journey walkthrough
- Product purpose
- User journeys
- Interface and interactions
- States: loading, empty, error, success
- Microcopy and messaging
- Emotional experience
- Accessibility and inclusion
- Privacy, consent and trust
- Product relevance and complexity
- Evaluating a proposed feature
- Pre-release experience review

## Getting at the real experience

Use the strongest access available, and say which one you used:

1. **The running product.** Run it locally or use a supplied URL, with a
   browser tool if one is available. Go through the journey, including the
   failure paths (wrong password, taken email, offline, slow network, empty
   account). Capture what you saw.
2. **The code, read state by state.** When the product cannot be run, trace
   the journey through routes, components, forms, validation, API calls and
   error handling. For each screen list every state the code can produce and
   what the person would see in each. Search for: validation messages,
   `catch` blocks and what they render, loading flags, empty-list rendering,
   disabled buttons and why they are disabled, redirects, timeouts, feature
   flags, analytics events.
3. **Designs, screenshots, specifications.** Useful for intent, silent on
   behaviour. Label findings from these as about the design, not the product.

Code reveals what screenshots hide: the error branch nobody designed, the
form state reset in a `finally`, the generic message every failure collapses
into, the field that is required by the API but optional in the form. When
working from code only, say: *"Evaluated from source; the running product was
not seen. Visual and timing findings are inferred."*

## The journey walkthrough

For each step of the journey, as the person from the empathy statement:

| Ask | Looking for |
| --- | --- |
| What is the person trying to do right now? | The goal at this moment, which may differ from the screen's purpose |
| What do they see first? | Visual hierarchy, what competes for attention |
| Will they know what to do? | Affordances, labels, the obvious next action (Norman's gulf of execution) |
| Will they know what happened? | Feedback, state changes, confirmation (the gulf of evaluation) |
| What could they misread? | Ambiguous labels, icons without text, jargon, unclear consequences |
| What does it cost them? | Typing, decisions, waiting, remembering, switching apps to look something up |
| What if it goes wrong? | Can they tell, understand why, recover without losing work? |
| How might this moment feel? | Frustration, anxiety, confusion, shame, distrust, relief, confidence |

Mark each stall, guess, lost-work moment, trust break and likely exit. These
become findings.

## Product purpose

- Is there a genuine human problem here, stated in the person's terms?
- Can a newcomer tell, within the first screen, what this is for and whether
  it is for them?
- Is there evidence that the intended people need it (supplied research,
  traction, support requests), or only the creator's belief? Say which.
- Does the product add complexity to the person's life that outweighs what it
  removes?

## User journeys

Cover the ones in scope, in order: discovery → first visit → sign-up →
onboarding → first value (the first moment the product does something useful
for this person) → core repeated tasks → errors and recovery → returning
after a gap → leaving (cancelling, exporting, deleting the account).

Key measures of a journey, judged by inspection:

- **Time to first value:** how many steps, fields and decisions stand between
  arrival and the first useful result? Which of them could wait?
- **Dead ends:** states with no next action.
- **Forced detours:** the person must leave to find information the product
  already has or could explain.
- **Re-entry:** having to type the same thing twice.
- **Leaving:** is it as easy to cancel, export or delete as to join? An
  asymmetric exit is a trust finding.

## Interface and interactions

- **Navigation and information architecture:** can people predict where
  things are? Do labels use the person's words or the org chart's?
- **Forms:** only the fields needed now; visible labels (placeholder text is
  not a label); requirements stated before the attempt, not after the failure;
  inline validation that helps rather than nags; input kept on every error;
  sensible input types on mobile (email, number, tel); autofill and password
  managers not blocked; no forced format the system could parse.
- **Buttons and controls:** the label says what will happen ("Create
  account", not "Submit"); destructive actions are distinct and confirmable or
  undoable; disabled controls explain why they are disabled.
- **Feedback:** every action gets an acknowledgement; slow actions show
  progress; double submission is prevented.
- **Consistency:** the same thing looks and behaves the same way everywhere.
- **Controls that cause friction on purpose** (password rules, verification,
  rate limits, consent) are kept. The finding is about how they are
  presented and explained, never a recommendation to weaken them.

## States: loading, empty, error, success

| State | Good | Failing |
| --- | --- | --- |
| Loading | Shows progress or a skeleton; keeps what is already known on screen | A blank page; a spinner with no end; layout that jumps when content arrives |
| Empty | Explains why it is empty and offers the first action | "No data" |
| Error | Says what happened in plain words, why if known, and what to do next; keeps the person's work | "Something went wrong"; a code; blame ("Invalid input"); lost work |
| Partial failure | Says what succeeded and what did not | All-or-nothing silence |
| Success | Confirms what happened and what comes next | Nothing, so the person repeats the action |
| Offline / timeout | Says so, retries or lets the person retry without loss | Silent failure |

## Microcopy and messaging

- Plain words the person would use; no internal terms, no codes as the only
  message.
- Error messages answer: what happened, is my work safe, what do I do now.
  They never blame the person for the system's constraint.
- Tone fits the moment: brief and calm when something failed; no jokes about
  money, data loss or health.
- Consequences are stated before irreversible actions, in concrete terms
  ("This deletes 14 invoices. You cannot undo it.").

## Emotional experience

Look for the design causes of:

- **Frustration:** repeated effort, blocked goals, unexplained refusals.
- **Anxiety:** unclear consequences (especially money, data, privacy,
  irreversibility), no confirmation, no undo, unexplained waiting.
- **Confusion:** missing mental model, inconsistent behaviour, unexplained
  terms.
- **Shame:** messages that imply the person is incompetent, tutorials that
  patronize, prices or plans that make them feel small.
- **Distrust:** surprises, hidden costs, dark patterns, data requested without
  reason.

And for what builds the opposite: predictability, undo, progress the person
can see, acknowledgement of their effort, honest explanations.

## Accessibility and inclusion

Evaluate who is excluded and what that costs them; leave conformance verdicts
to `standards-compass`.

- Keyboard: every action reachable and operable; visible focus; logical
  order; no traps; focus moved sensibly in dialogs.
- Screen readers: real labels and names; errors announced and associated with
  their fields; headings and landmarks; status messages announced.
- Vision: contrast, text resizing to 200% without loss, information not
  carried by colour alone.
- Motor: target sizes, no time limits without extension, no precise gestures
  without alternatives.
- Cognitive: plain language, one decision at a time, recognition over recall,
  no memorizing codes between screens.
- Experience levels, language and culture: second-language readers, name and
  address formats that fit real people, date formats.

## Privacy, consent and trust

- Is every piece of data asked for justified at the moment it is asked, and
  does the person understand why?
- Is consent freely given: unticked by default, separate from the terms,
  as easy to withdraw as to give?
- Are there deceptive patterns? Common forms: preselected options,
  confirmshaming ("No thanks, I don't like saving money"), hidden costs,
  forced continuity, roach-motel cancellation, nagging, disguised ads, trick
  questions with double negatives, false urgency or scarcity.
- Does the product respect autonomy: no manipulation toward choices that
  serve the business against the person's interest?

Deceptive patterns are always findings, regardless of their business
results. Legal and regulatory questions about consent go to
`standards-compass`.

## Product relevance and complexity

- For each feature in scope: what need does it serve, for whom, and is there
  evidence they have that need?
- Which actions does the product ask for that serve the organization rather
  than the person (marketing questions in sign-up, mandatory tours,
  "complete your profile" nags)?
- Is personalization genuinely useful to the person, transparent, and under
  their control? Or does it mainly collect data?
- Which features add complexity for everyone to serve a few? Could they be
  progressive (revealed when needed) instead of removed?

## Evaluating a proposed feature

Before anything is built:

1. **The need:** which person, in which situation, with what evidence?
2. **The job:** what progress does the feature give them, and how do they make
   that progress today without it?
3. **The cost to everyone else:** added surface, decisions, notifications,
   data collected.
4. **The risks:** privacy, manipulation, exclusion, dependence.
5. **The smallest test:** what is the cheapest way to learn whether people
   need it (an interview round, a fake-door test with honest follow-up, a
   manual concierge version)?
6. **The verdict:** build / build smaller / test first / don't build, with
   reasons and what evidence would change it.

## Pre-release experience review

When asked whether a flow or product is ready for users, give an experience
verdict, separate from any ship verdict:

- **READY:** no finding of high severity; the core journey completes for the
  primary person and the edge cases checked.
- **READY WITH CONDITIONS:** named findings must be fixed or accepted by a
  person first.
- **NOT READY:** a person in the intended audience cannot complete the core
  task, loses work, is deceived, or is excluded from the core journey.

State what was not inspected. The decision to ship belongs to the people
asking, and to `production-guard` where it is in use.
