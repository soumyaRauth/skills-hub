# Product questions

Stage 1 asks at most five questions, in one block, and only the ones whose
answer changes what gets built. This file holds the wording and the defaults.

## The test for a question

Ask it only if two different answers would produce two different v1s. *What
colour should the buttons be?* fails the test. *Do members pay in the app?*
passes: one answer adds a payment provider, refunds and receipts, the other
adds nothing.

A question a beginner cannot answer is the wrong question. *REST or GraphQL?*,
*which database?*, *monorepo?* are yours to default, and never asked.

## Wording that works

| Instead of | Ask |
| --- | --- |
| Who are your personas? | Who will use it? For example: members, instructors, the front desk |
| Describe the core user journey | Walk me through one booking from start to finish, as a member would do it |
| What is the MVP scope? | What can wait until after the first version works? |
| Do you need PCI compliance? | Should people pay inside the app in the first version, or not yet? |
| What PII will you store? | Besides name and email, will it keep anything personal, such as phone numbers, health notes, or children's details? |
| What are your deployment targets? | Where will people use it: on their phone, on a computer, or somewhere specific like a tablet at the front desk? |
| What is your tech background? | What do you already know how to program in, if anything? |
| Timeline? | Is there a date this needs to be working by? |

Close the block with the assumptions you are making in the meantime, so the
user can correct them in the same reply:

```
Meanwhile I am assuming: <default>, <default>, <default>. Say so if any of that is wrong.
```

## Defaults for what you do not ask

State these as `[assumed]` in the spec. Each one names what would change it.

| Topic | Default | Changes if |
| --- | --- | --- |
| Where it runs | A web app that works in a phone's browser | They need an app store listing, offline use, or device hardware |
| Payments | None in v1 | They say people pay inside the app |
| Personal data | Name and email only | The domain or the user says more |
| Locations / tenants | One organization | They mention several branches or selling it to others |
| Languages | The language the user wrote in | They mention another audience |
| Accounts | Sign-in only for the people whose workflow needs it | The workflow is anonymous (then no accounts at all) |
| Admin | The framework's built-in admin screen if it has one; otherwise none | Staff have a workflow of their own that needs its own screen |
| Notifications | None; the page shows the result | They say people must be told by email or text |
| Deadline | None | Only the user sets one. Never invent it |

## When the user answers

- **"You decide"** — take the smallest option, mark it `[assumed]`, move on.
- **An answer that adds scope** (*and also a shop, and a chat*) — the core
  workflow stays v1; the rest goes to non-goals as *later*, with the user's
  words. Say that in one line; do not argue.
- **An answer that forces a non-default stack** (*it must work with no
  internet*) — record it `[you said]` and hand it to `architecture-engineer`
  at stage 3.
- **No answer to one question** — proceed with its default and say which.
  Do not ask twice.
