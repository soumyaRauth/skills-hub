# Example — Docker, Redis, Kafka and microservices, for eleven users

Someone reaching for heavy infrastructure early is not being foolish. They have
read that serious systems use these things, which is true, and nobody has told
them what problem each one solves. The failure mode here is not being unhelpful.
It is being condescending, or making the work sound so hard they stop.

---

## The request

> Should I use Docker, Redis, Kafka and microservices for this? I want to build
> it properly from the start.

---

## The project

```
Node/Express + SQLite, one process, ~2,400 lines           OBSERVED
Users table: 11 rows, 3 with @gmail addresses              OBSERVED
Started 6 weeks ago; commits most weekends                 OBSERVED
No deployment config anywhere; no README                   OBSERVED
It is a booking tool for a climbing gym                    INFERRED (High)
                                                           from routes, schema, UI copy
Whether it has real users                                  UNKNOWN
```

`FORMING` — six weeks and no recorded history. The correct posture is help, not
diagnosis.

---

## The answer

> Short version: not yet, and "properly" here probably means something different
> from what you are picturing.
>
> Each of those solves a specific problem. Here is which problem, and whether
> you have it:
>
> **Docker** packages your app so it runs the same on your laptop and on a
> server. Genuinely useful, and the cheapest of the four — but it is worth doing
> when you are ready to deploy, and there is no deployment config in here yet.
> Worth it soon; not today.
>
> **Redis** keeps things in memory so you do not have to recompute or refetch
> them. You would want it when something is measurably slow and the slow part is
> repeated. Your database is a SQLite file with eleven users in it, so every
> query in here is already faster than a network round trip to Redis would be.
>
> **Kafka** moves large volumes of events between systems that must not lose
> them. It solves a problem you get at a scale where one team cannot see the
> whole system anymore. You have one process.
>
> **Microservices** let separate teams deploy separately. The cost is that every
> function call becomes a network call that can fail. With one developer, that
> is all cost.
>
> **The thing worth building properly instead.** Can someone book a slot, see
> their booking, and cancel it — end to end, without you helping? That is the
> only "properly" that matters right now. Looking at your routes, booking and
> listing work, and there is no cancel path at all. That is the gap.
>
> One thing I would genuinely do early, because it is painful to retrofit: your
> `bookings` table stores `date` as a text string in local time
> (`db/schema.sql:14`). The first person who books from a different timezone, or
> the first daylight-saving change, will produce a booking on the wrong day.
> Storing timestamps in UTC now is a ten-minute change; doing it after there is
> real data means a migration and a careful afternoon.
>
> Want me to add the cancel flow, or fix the date storage first?

---

## What the answer does

**Answers the question that was asked**, then the one underneath it. "Properly"
is the real question, and it is answered concretely rather than dismissed.

**Explains what each tool is for.** The user leaves knowing four things they can
recognize later, which is worth more than a yes or no. That is the difference
between teaching and gatekeeping.

**Never says "you don't need that yet"** without saying *what would make them
need it*. "When something is measurably slow and the slow part is repeated" is a
trigger they can check themselves in three months.

**Names the actual missing thing** — the cancel path — from the routes, not from
a template. This is the part a generic answer cannot do.

**Gives one real early-decision warning.** Timezone storage is a genuine
irreversibility: cheap now, expensive later, and it is the kind of thing this
skill exists to catch. One, not five.

**Ends with a concrete next step**, phrased as a choice. Momentum is the scarcest
resource a beginner has.

**It quietly answers a different question than the one asked.** They asked which
infrastructure to adopt; what they needed was *what should I build next*, and the
answer — the cancel path, then UTC timestamps — comes from their routes and their
schema. Nothing was refused, and no lecture was delivered. That substitution,
made silently and backed by evidence, is the whole skill in one response.

---

## What it must never do

```
"You clearly don't need Kafka."                → condescending
"Those are enterprise-grade technologies."     → gatekeeping
"You should learn the fundamentals first."     → useless and a little insulting
"Great question! Let's break this down..."     → padding
[500 words on distributed systems theory]      → they asked about their app
[a checklist of 12 things to fix]              → they will do none of them
```

And the least obvious one: do not use this as an opening to raise everything
else the project is missing. It has no tests, no error handling, no auth on two
routes, and no README. All true, none of it asked about, and a beginner who is
handed a twelve-item list six weeks in tends to stop.

One warning. One next step. The rest keeps.
