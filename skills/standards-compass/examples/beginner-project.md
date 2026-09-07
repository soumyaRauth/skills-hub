# Beginner — "what standards do I need?"

**Request:** *"I'm building my first real app. What standards do I need to
follow? I keep reading about ISO and OWASP and GDPR and I have no idea where to
start."*

**Project:** a habit tracker. React frontend, Firebase auth and Firestore, ~3k
lines, deployed, about 40 users, all friends of the developer.

The failure mode is answering the question as asked. The person does not need a
standards curriculum; they need to know that almost none of it applies to them
yet, and which small part does.

---

## Response

```markdown
Short answer: almost none of them, yet. Here's how to tell which ones will
eventually matter, so you're not carrying this question around.

Standards fall into groups, and they apply for different reasons:

- **Laws** (GDPR and similar) apply based on where you and your users are, and
  what data you hold. Nothing to do with how you write code.
- **Industry rules** (PCI DSS for cards) apply if you handle the thing they
  cover. You don't take payments, so this one is simply off the table.
- **Certifications** (ISO 27001, SOC 2) are things a *company* gets when a
  customer demands proof. You have no customers demanding proof. Ignore these
  entirely for now — they're not a code thing at all.
- **Engineering guidance** (OWASP, WCAG) is useful to anyone. This is the group
  that's actually relevant to you today.

So, for your app specifically:

**Worth caring about now — three things**

1. **You're storing personal data** (email, and habit data, which is more
   personal than it looks — sleep, exercise, mood are all in there). Two
   practical consequences: don't collect what you don't use, and make sure
   someone can delete their account and actually be gone. Right now
   `deleteAccount` in `src/auth.js:44` removes the auth user but leaves the
   Firestore documents, so their data survives the deletion. That's the single
   most worthwhile fix in your codebase.

2. **Your Firestore rules are the whole security model.**
   `firestore.rules:12` allows any signed-in user to read the `habits`
   collection, not just their own documents. Anyone with an account can read
   everyone's habits. This is the one I'd fix today — it's four lines.

3. **Keyboard access.** Your habit checkboxes are `<div onClick>`
   (`src/components/HabitRow.jsx:18`), so they can't be reached by keyboard at
   all. Making them `<button>` elements fixes it and removes code. WCAG is the
   standard behind this, but you don't need to read WCAG — you need buttons to
   be buttons.

**Worth knowing about, not acting on yet**

If you ever add payments, take on business customers, put an AI feature over
user data, or get users in the EU while being outside it, come back and ask
again — each of those changes the answer.

**Safe to ignore**

ISO 27001, SOC 2, ISO 42001, PCI DSS, HIPAA, and every governance framework.
Not because they're unimportant, but because they're about organizations
proving things to other organizations, and nobody is asking you to prove
anything.

Want me to fix the Firestore rule and the deletion gap? Both are small.
```

---

## What makes this work

- It answers the question underneath ("where do I start?") rather than the
  question asked ("which standards?").
- The taxonomy is four lines, and it is what makes the rest make sense.
- Every finding is in *their* code with a real path, not a general principle.
- Three findings, not thirty. The severity ordering is real: the Firestore rule
  is the emergency.
- The dismissals are explicit and reassuring, which is what stops the anxiety
  the question came from.
- No condescension, no "you should have thought about this earlier", and no
  homework.
