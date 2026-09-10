# What the project is becoming

Software changes category without anyone deciding that it should. A task list
becomes a task management system. A collection of user screens becomes an
administration system. Three payment features become a billing lifecycle. Each
step is a reasonable request; the sum is a different system with different
obligations, and nobody announced the change.

This file is about noticing the crossing, sizing it honestly, and saying it in a
way that helps rather than alarms.

## The question that produces it

Not *"what has been implemented?"* — that produces a count, and a count is
useless:

```
Useless    8 features implemented this month
Useful     those 8 features are an administration system, and nobody has
           defined the administration workflow
```

The second sentence is available only from the sequence. The person making the
requests cannot see it, because each request was individually correct and
arrived alone.

## The blind-spot request

The highest-value pattern in this file. A developer asks for isolated things,
one after another, because they do not yet have a picture of what the project
should become. The requests look like a healthy backlog:

```
Add search.        Add export.          Add user groups.
Add filtering.     Add bulk delete.     Add permissions.
Add sorting.       Add saved filters.
```

Individually legitimate. Collectively they say: *we are building an
administration system, and the administration workflow has never been defined.*

The failure mode is to keep implementing. The second failure mode is to say
"you seem to be adding a lot of features", which is a complaint rather than a
contribution. What is actually useful is naming the thing they have been
building and the one decision that makes the next ten features cheaper:

> We are past adding user features — this is an administration system now:
> groups, permissions, bulk operations and saved views over the same records.
> Before the next capability, I would define the user-management model: who
> administers whom, what a group is for, and whether permissions attach to
> groups or to people. It is one page, and every one of these features currently
> answers it differently.

## Crossings worth recognizing

Each row needs its own evidence before it is said out loud. The right column is
the *name of the thing they are now building*, which is usually the most useful
sentence available.

| What accumulated | What it has become | Cheapest thing that makes the rest work |
| --- | --- | --- |
| Search · filter · sort · bulk action · export · saved views | List/query management workflow | One sentence naming who uses the list and what they are finishing |
| Draft · submit · approve · reject · return · publish | A lifecycle — a state machine | The states, the legal transitions, and who may cause each |
| Invite · role · permission · organization · access · audit | Authorization and tenancy model | Subjects, resources, actions, and whether ownership outranks role |
| Payments · refunds · subscriptions · invoices · dunning | Billing lifecycle | How those objects interact, especially on failure |
| Notification rules added per feature | Event-driven communication system | The domain's actual events, their consumers, their guarantees |
| Several reporting screens | Analytics product | What decision each report supports; who reads it |
| Several approval features | Workflow engine | Whether this is one configurable flow or several hardcoded ones |
| Several third-party connections | Integration platform | What is shared across integrations — auth, retries, mapping, failure |
| Accounts · orgs · roles · billing · audit on an internal tool | A multi-tenant product | Whether that is the plan, before the next layer |

The last row is different in kind and worth its own care: see **Product
crossing** below.

## Evidence a crossing actually needs

A crossing is a claim about the system's category, so it needs more than three
instances in a row. Require all three of these:

**Breadth.** The features are not one feature being built. Three controls added
during "build the admin table" story is a feature. Three controls added across
five weeks in three different sessions is accumulation.

**A shared unnamed concept.** The features all reference something the codebase
has no definition of — *what a member is here*, *what approved means*, *what a
notification is triggered by*. Two implementations disagreeing about it is the
proof.

**A cost that is already being paid.** Somebody has already had to guess, or
work around the absence, or write a second version of the same rule. Without
this, the crossing may be real and still not worth saying.

```
Enough      six controls, five weeks, three different field sets across
            TaskFilters.jsx:3, SavedViews.jsx:4, api/tasks.js:3
Not enough  six controls, five weeks, all consistent, nothing blocked
Not enough  "this is starting to look like an admin system" with no locations
```

The second line matters as much as the first. A project that has genuinely
become an administration system and is handling it coherently does not need to
be told; it needs the work done.

## Product crossing

The version worth separating: the *product* changes without anyone noticing. An
internal tool acquires accounts, then organizations, then permissions, then
billing, then notifications, then an audit log.

Each step is reasonable. The sum is a different product with different
obligations — support, migrations, uptime, data protection, an upgrade path —
that nobody signed up for.

Report it as an observation, once, never as a criticism and never as a request
to stop:

> This is not behaving like the internal tool it started as. In two months it has
> grown accounts, orgs, roles and an audit trail — that is the shape of a
> multi-tenant product, with the support and upgrade obligations that come with
> it. Worth deciding whether that is the plan before the next layer goes on.

The failure mode here is moralizing. State it once, and drop it.

## Saying it well

Four properties separate a useful crossing from an unwelcome lecture.

1. **Name the thing.** *"This is a lifecycle now"* is more useful than any amount
   of description, because it makes the problem searchable and turns a vague
   discomfort into a topic with known answers.
2. **Show the instances.** Dates and locations, because the claim is about a
   sequence and the developer only remembers the last one.
3. **Give one decision, not an architecture.** The output of a crossing is a
   page someone writes, not a refactor someone schedules.
4. **Do not ask them to stop.** The features were fine. The next ten are what
   the decision is for.

```
Bad     "The project's domain boundaries are becoming unclear and would benefit
         from an explicit architectural review."
Good    "This is a lifecycle now rather than a set of flags. Ten lines listing
         the states and the legal transitions, and the next status is a one-line
         change instead of a fourth special case."
```

## Do not force structure early

The mirror-image failure: declaring a crossing on three features and demanding a
model. Most projects should reach a lifecycle, an authorization rule or an event
model *late*, after the shape is known from use, and a premature model is a
worse constraint than no model at all.

Hold off when any of these is true:

- The project is `FORMING` or the feature set is a few weeks old.
- The user has said they are prototyping, experimenting, or building a
  throwaway. Their word settles it.
- Nothing has had to guess yet — the features are consistent.
- The likely model is cheap to introduce later. Reversibility lowers urgency
  more than anything else on this page.
- It is one person's project, pre-users, and the cost of the wrong abstraction
  exceeds the cost of the missing one.

The test is not *"has it become a system?"* but **"is somebody already paying
for the absence of the model?"** If nobody is, record the crossing in
`direction.md` and stay quiet. The evidence keeps accumulating on its own, and
the observation is stronger next month.

## Recording it

`direction.md` holds the current answer and is rewritten rather than appended
to — it is a view of now, not a log:

```markdown
**Appears to be**  Team task tracker
**Becoming**       A list/query management workflow          INFERRED (High)
**Evidence**       CHANGELOG 0.5.0–0.9.0, seven releases, all controls on one
                   screen; three inconsistent field sets
**Not yet said**   nothing is blocked; raise at the next control request
```

That last line is what makes silence deliberate rather than forgetful. When the
crossing is eventually raised, it is raised once, with the accumulated evidence,
and then it is either acted on or recorded in `decisions.md` as closed.
