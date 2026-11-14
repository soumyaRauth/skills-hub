# Example: a registration flow

A journey evaluation of an invoicing app's sign-up, from source code and
supplied support tickets. The running product was not available, which the
report says, and which caps the confidence of every visual and timing claim.

## Contents

- The request
- Framing
- The walk
- The report
- What made this a good run

## The request

> People keep giving up halfway through our sign-up. Walk through it as a new
> user would and tell me what it's like.

Repository: `README.md` (product: invoicing for solo freelancers),
`src/SignupForm.jsx`, `src/validation.js`, `src/api.js`, `src/analytics.js`,
`support/tickets.md` (three tickets).

## Framing

```
⚡ Human Empathy — sign-up journey review; support tickets describe lost input

MODE        Journey evaluation (no edits)
EMPATHY     A solo freelancer, probably on a phone between client work, creating an
STATEMENT   account to send a first invoice today. Evaluating landing on /signup
            through to the first dashboard.
PERSON      ASSUMED from README ("solo designers, developers and writers") and
            tickets; no user research supplied
EDGES       Screen-reader user · second-language English · has an old account
UNKNOWN     Device mix; where in the form people stop (analytics events exist,
            results were not supplied)
```

## The walk

What the person meets, step by step (from source; not observed running):

1. **Ten fields and a checkbox** before anything happens: names, email,
   password twice, phone in `+15551234567` format, company name, company size,
   country, terms. Nothing says why phone or company size are needed.
2. **Company size starts at "2-10".** A solo freelancer, the product's core
   customer, has no true answer. Ticket #4851 says exactly this.
3. **The button stays greyed out** until every field and the terms box are
   filled (`isComplete`, `SignupForm.jsx:20`). Nothing says what is missing.
4. **Password rules arrive after failure.** Only after a full submit does the
   person learn the 12-character, uppercase, number and symbol policy.
5. **A server failure empties the form.** Any non-2xx response becomes
   "Something went wrong. Please try again." (`api.js:9`) and the catch block
   resets every field (`SignupForm.jsx:38`). Ticket #4812: filled in on a
   phone, error, form empty, tried twice, gave up.
6. **An existing account looks like an outage.** The 409 for a registered
   email collapses into the same generic message, with no route to sign in or
   reset. Ticket #4830 is someone who cannot tell whether they have an account.
7. **Marketing is pre-ticked** with "Uncheck if you don't want to grow your
   business."

## The report

```
HUMAN EMPATHY — Journey evaluation · sign-up
────────────────────────────────────────────────────────
EXECUTIVE ASSESSMENT
The flow asks a solo freelancer for agency-shaped information, hides its rules
until after failure, and punishes any server error by erasing everything they
typed. Two of the three supplied tickets describe exactly the erase-on-error
path, the third the company-size field. The fix for the worst problem is a few
lines. Overall 2 · Significant weaknesses · confidence MEDIUM (source only).

SCOPE
Inspected: SignupForm.jsx, validation.js, api.js, analytics.js, support/tickets.md.
Not inspected: the running product (layout, timing, mobile keyboards), the
server's actual error responses, analytics results, the post-sign-up dashboard.

CRITICAL FINDINGS (verified in the artifact)

F1  People lose everything they typed when sign-up fails
  Affected person   Anyone whose submit fails: outage, taken email, server validation
  Evidence          VERIFIED: setForm(initial) in catch (SignupForm.jsx:38);
                    ticket #4812 describes it and the abandonment that followed
  Underlying need   To recover from a failure they did not cause, without starting over
  Root cause        Failure paths were never designed; the reset treats an error as
                    something to clean up rather than something to recover from
  Impact            Re-entry of ten fields, on a phone; trust drops at the moment of
                    commitment. Likely a direct cause of abandonment (SUPPORTED:
                    re-entry cost after a failed submit is a well-established
                    form-abandonment driver)
  Severity          Critical · frequency unknown (analytics results not supplied)
  Confidence        HIGH
  Recommendation    Keep all fields on error (clear only the two password fields if
                    policy requires); move focus to the message
  Validation        Compare signup_server_error → signup_completed within a session,
                    before and after

F2  An existing customer is told "something went wrong" instead of "you already
    have an account"
  Affected person   Returning users, people who signed up long ago
  Evidence          VERIFIED: every non-OK status throws one message (api.js:7-10),
                    the comment names 409; ticket #4830
  Underlying need   To know what happened and what to do next
  Root cause        Errors are collapsed at the API layer, before the UI can explain
  Impact            The person cannot tell an outage from a duplicate; contacts
                    support or leaves
  Severity          High · Confidence HIGH
  Recommendation    409 → "There's already an account for this email. Sign in or
                    reset your password", with both links. 422 → the field
                    messages. 5xx → "We couldn't create your account just now.
                    Your details are still here; try again in a minute."
                    Avoiding account enumeration is a real concern here:
                    HANDOFF → standards-compass: confirm whether the 409 message is
                    acceptable or should move to an email-based flow

F3  The sign-up assumes a company; the core customer is one person
  Evidence          VERIFIED: companyName and companySize required
                    (validation.js:30-31); smallest option "2-10"; ticket #4851
  Underlying need   To recognize themselves in the product
  Root cause        Sales segmentation shaped the form, not the first-use need
  Severity          High · Confidence HIGH
  Recommendation    Remove both from sign-up; ask later, optionally, where they
                    serve the person (invoice header). Needs your decision: if
                    sales relies on the field, say so and we can discuss a
                    "Just me" option instead

F4  Rules and requirements are revealed only by failing
  Evidence          VERIFIED: password policy shown only in the error branch
                    (SignupForm.jsx:58-62); disabled Submit with no reason
                    (SignupForm.jsx:96); phone format only in the placeholder
  Severity          High · Confidence HIGH
  Recommendation    Show the password rules under the field from the start and tick
                    them off as typed; keep the policy (it is a security control);
                    enable the button and explain what is missing on submit;
                    accept common phone formats or drop phone (see F3's question)

F5  Marketing consent is pre-ticked and shames people who untick it
  Evidence          VERIFIED: marketing: true in initial state (SignupForm.jsx:9); label
                    "Uncheck if you don't want to grow your business" (:91)
  Underlying need   To decide freely, and to be treated with respect
  Root cause        A growth target written into the form
  Impact            Deceptive patterns (preselection, confirmshaming) erode trust in
                    a product that will handle the person's income
  Severity          High · Confidence HIGH
  Recommendation    Unticked, neutral: "Email me product tips (about one a month)."
                    HANDOFF → standards-compass: consent obligations for the
                    countries in the selector

F6  Screen-reader users get unlabeled fields and unannounced errors
  Evidence          VERIFIED: placeholder-only inputs, no <label>; error spans not
                    associated with fields; banner not in a live region
  Severity          High for those users · Confidence HIGH for the markup,
                    LOW for the lived experience (no assistive-technology test)
  Recommendation    Visible labels, aria-describedby for errors, focus to the banner.
                    HANDOFF → standards-compass for the conformance check

HYPOTHESES (not established by inspection)
H1  Mobile users struggle most: no inputMode/type="email"/type="tel"; ticket #4812 was
    on a phone. Test with three think-aloud sessions on phones.
H2  Double submissions create duplicate accounts: no pending state on the button.
    Check server logs for duplicate creations within seconds.

ROOT CAUSES
R1  The failure paths were never designed (F1, F2, F4, H2).
R2  The form serves the organization's segmentation before the person's first
    invoice (F3, F5, and the phone field).
R3  No shared form pattern for labels and errors (F4, F6).

EMPATHY SCORES (rubric: references/empathy-scoring.md)
  Human Understanding         2   HIGH     Core customer cannot answer company size
  Emotional Experience        2   MEDIUM   Lost input, blame-shaped messages
  Cognitive Simplicity        2   HIGH     Ten fields, rules hidden until failure
  Clarity and Communication   2   HIGH     One message for every failure
  Personal Relevance          2   MEDIUM   Agency-shaped questions for solo users
  Accessibility & Inclusion   2   MEDIUM   Unlabeled fields; untested with AT
  Respect for the User        1   HIGH     Preselected consent with confirmshaming
  Practical Value             —   INSUFFICIENT EVIDENCE (journey ends at sign-up)
  Experience Consistency      —   INSUFFICIENT EVIDENCE (one journey)
  Trustworthiness             2   MEDIUM   Errors conceal what happened
  Overall                     2 · Significant weaknesses (median 2 of 8; cap
                              applies, Respect = 1) · MEDIUM

RECOMMENDED ORDER
1  F1 keep input on error (small, removes the worst cost)
2  F2 distinct messages per failure, after the enumeration question is answered
3  F4 rules up front, explain the disabled state
4  F5 consent unticked and neutral
5  F3 remove company fields (needs your decision)
6  F6 labels and error association

RECOMMENDED VALIDATION
- Supply or pull the signup_validation_failed field counts and signup_server_error
  rates: which fields fail most, how often the server fails.
- Three to five think-aloud sessions with solo freelancers on phones, before and
  after F1–F4.
- One session with a screen-reader user.
```

## What made this a good run

- The tickets were quoted as what *those* customers said, never as "users".
- Every feeling was written as a likely effect with its mechanism.
- The password policy stayed: the finding was its presentation.
- Two scores were left empty rather than guessed, and the overall followed the
  documented rule, including the cap.
- Consent law and account enumeration were handed to `standards-compass`
  instead of being decided here.
