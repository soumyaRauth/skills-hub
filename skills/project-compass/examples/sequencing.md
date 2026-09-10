# Example — The interface is ahead of the workflow

Sequencing problems do not look like problems. They look like a productive
month. Screens improve, commits land, and the thing the product is actually for
still does not work end to end.

This example also draws the line the skill gets wrong most often: which UI
request is worth stopping for, and which is just a UI request.

---

## The project

Billsy — invoicing for freelancers. The README says *"send invoices and get paid
faster"*, which is the clearest objective statement in the whole repository and
is worth taking literally.

The core loop it names: **create → send → get paid.**

```
create   OBSERVED  routes/invoices.js:4          works
send     OBSERVED  routes/invoices.js:9          works; marks sent_at
get paid OBSERVED  routes/invoices.js:16         recordPayment sets
                                                 status = 'paid' for ANY amount,
                                                 with a TODO asking what a
                                                 partial payment is
chase    OBSERVED  workers/reminders.js:5        written three weeks ago;
                                                 wired into no scheduler
```

Two of the four steps in *"get paid faster"* are broken or unreachable, and the
one that is broken is broken in a way that produces wrong numbers rather than an
error: `Dashboard.jsx:3` treats `status === 'paid'` as settled, while
`InvoiceView.jsx:4` computes outstanding from `paid_cents`. A €500 invoice with
€50 paid disappears from the dashboard and still shows €450 outstanding on its
own page.

---

## The trajectory

```
2026-08-24  ui     Invoice view: print button, print stylesheet   ui/InvoiceView.jsx
2026-08-31  ui     Dashboard: outstanding total at the top        ui/Dashboard.jsx
2026-09-05  ui     Invoice view: status line, outstanding warning ui/InvoiceView.jsx
                   pattern: presentation-ahead-of-workflow (3rd)
```

Three presentation changes. Nothing in that window touched the payment path, the
reminders worker, or the PDF button on `InvoiceView.jsx:13`, which is wired to
an empty handler.

---

## Request four — and the silence it gets

> Move the invoice number up next to the logo and make the status a coloured
> pill.

**Mode A.** Do it, say nothing.

It is ten minutes, it is independently correct, it makes nothing worse, and it
bakes in nothing. Stopping a person for a sequencing lecture in the middle of a
cosmetic change is exactly the behavior that gets a skill uninstalled — and the
pattern counter still goes up silently, so the evidence is stronger next time,
not re-derived.

```
Trajectory  recorded — presentation-ahead-of-workflow (4th)
Output      the change
```

---

## Request five

> Let's add invoice templates — three designs, and people pick one per client.

Different size, different answer. This is days of work, it is the fifth
consecutive change on the presentation layer, and it lands on a screen whose
main action does nothing.

**Against the gates:**

| Gate | |
| --- | --- |
| Recurrence | Five presentation changes since 24 August; four locations; not one entry on the payment path |
| Convergence | Every one refines how an invoice *looks*, while the loop the product names — get paid — has two broken steps |
| Consequence | Templates render the invoice. The PDF button that would deliver a rendered invoice is `onClick={() => {}}`, so three designs would be visible only on screen and in `window.print()` |
| Actionability | Two small things: wire the PDF button, and answer one question about partial payments. Both smaller than the template work |

Not a contradiction, not irreversible, and templates are a real feature someone
may well be asking for. But building three designs for a document that cannot be
delivered is the sequencing failure in its purest form, so this one gets said.

---

## The response

> **I'd do one thing before this.**
>
> Templates would change how the invoice renders — and right now the invoice
> cannot leave the app. "Download PDF" on `InvoiceView.jsx:13` is
> `onClick={() => {}}`, so the only way a client sees a design today is the
> browser print dialog. Three designs would be three designs nobody receives.
>
> There is a second thing in the same area, and it is the one I would actually
> start with. `recordPayment` sets `status = 'paid'` for any amount, including a
> partial one — there is a TODO on line 20 asking exactly this. The dashboard
> keys off `status`, the invoice page computes outstanding from `paid_cents`, so
> a €500 invoice with €50 paid vanishes from "Outstanding" and still says €450
> owed on its own page. For a tool whose README is *get paid faster*, that is the
> number being wrong in the wrong direction.
>
> **What I'd do, in this order:**
>
> 1. Decide what a partial payment is — my default: keep `status = 'sent'` until
>    `paid_cents >= total_cents`, add `partially_paid` only if you want it visible.
>    One sentence from you and it is a ten-line change. `REQUIRED` — the reminders
>    worker also filters on `status = 'sent'`, so it is currently the third thing
>    depending on this.
> 2. Wire the PDF button, or delete it. `RECOMMENDED` — a button that does nothing
>    is worse than no button, and templates need it either way.
> 3. Then templates, which will be a better feature once there is something to
>    put a template on.
>
> Also worth knowing while you are in there: `workers/reminders.js` has never been
> attached to a scheduler, so nothing chases an overdue invoice today.
>
> If templates are what a customer is actually waiting for, say so and I'll start
> them now — that is a priority I cannot see from the repository.

---

## Why this shape

**It is not about the UI work.** Nothing in the response says the presentation
changes were wrong, because they were not. The recommendation is about *order*,
and the difference between those two framings is the difference between guidance
and complaint.

**The workflow break is named with a location.** `InvoiceView.jsx:13`,
`invoices.js:20`. Checkable in ten seconds, which is what makes the ordering
argument land instead of sounding like a preference.

**The partial-payment question outranks the PDF button**, even though the PDF
button is what the template request runs into. It is a decision three things are
already waiting on, and decisions outrank code — see the ranking in
`next-action.md`.

**A default is offered**, so the blocking question costs one word to answer.

**The request is not refused, and the offer to proceed is specific.** The user
may know a customer is waiting for templates; nothing in the repository could
tell you that.

---

## What this must never become

```
"Before adding more UI, you should focus on core functionality."
```

True, useless, and applicable to almost every project on earth. It names no
break, no location, no decision and no order, and the person reading it is
exactly as stuck as they were — except now slightly annoyed.

The other failure is the mirror image: treating every interface request as
evidence of a sequencing problem. Four of the five requests here got no comment
at all, and the fifth got one because it was substantial, because it landed on a
dead button, and because a decision underneath it was blocking three other
things.
