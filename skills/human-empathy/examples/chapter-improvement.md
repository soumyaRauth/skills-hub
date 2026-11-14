# Example: improving a chapter with poor progression

The author has read the evaluation in `book-evaluation.md` and asks for the
chapter to be fixed. The run shows the approval step for a direction change,
a rewrite that keeps the author's voice and running example, and the
cross-chapter consequences handled rather than left behind.

## Contents

- The request
- Step 1: the plan, before writing
- Step 2: after approval, the rewrite
- Step 3: consequences outside the chapter
- Step 4: verification and report
- What made this a good run

## The request

> OK, fix chapter 3 so beginners can follow it.

## Step 1: the plan, before writing

"Fix chapter 3" authorizes improving the chapter. Moving `Depends`,
`BaseSettings` and response models into later chapters changes the book's
plan, and the install fix lives in chapter 1. Both need the author's word.

```
⚡ Human Empathy — rebuilding chapter 3 for its stated reader

MODE   Book improvement · chapter 3 (+ one line in ch. 1, pending your OK)

PROPOSED CHAPTER 3 — "Your first endpoint"
  Outcome       Run an API that returns your tasks as JSON, and fetch one task by id
  Builds on     Ch. 2: functions, dictionaries, lists of dictionaries
  New concepts  (1) what HTTP requests and responses are  (2) an app and a route
                (3) just enough decorator to read @app.get  (4) a path parameter
  Moves out     async/await, Depends, BaseSettings, Pydantic models, response_model
                → a new "Organizing your API" chapter after ch. 4, where the
                code has grown enough to need them
  Running ex.   Unchanged: the to-do API, same tasks
  Practice      Add /tasks/{task_id}/done that returns only the done flag
  Close         Recap, a self-check, and the bridge to ch. 4

NEEDS YOUR DECISION
  D1  Move the advanced material to a later chapter (recommended), or keep it at
      the end of ch. 3 as an optional section marked "skip on first read"?
  D2  Change ch. 1 §1.3 to pip install "fastapi[standard]"? (verified: it
      provides the uvicorn command the chapter uses)
  D3  Chapter 4 uses a Pydantic model for POST. If models move later, ch. 4 needs
      a short introduction to them. Include that in this change?
```

The author answers: *D1 move it, D2 yes, D3 yes.*

## Step 2: after approval, the rewrite

The opening, before and after. The author's plain, friendly register from
chapters 1 and 2 is kept; "production-grade" and the full listing go.

**Before**

> In this chapter we'll build a production-grade async REST API with
> dependency injection, typed models and settings management. Here is the
> whole thing:

**After**

> In chapter 2 you stored tasks in a list of dictionaries. In this chapter,
> you'll make that list available on the web: by the end, your browser will
> show your tasks, fetched from a server you wrote.
>
> First, a few words about how browsers and servers talk, because everything
> else in this book builds on it.
>
> ## 3.1 Requests and responses
>
> When you open a web page, your browser sends a **request** to a server: "GET
> me `/tasks`". The server sends back a **response**: a status code saying how
> it went (`200` means OK, `404` means "there's nothing here") and a body with
> the content. An API is a server whose responses are data for programs,
> usually JSON, rather than pages for people. JSON looks almost exactly like
> the dictionaries and lists from chapter 2.

Then the smallest program that works, explained line by line:

> ## 3.2 A server in five lines
>
> ```python
> from fastapi import FastAPI
>
> app = FastAPI()
>
> tasks = [
>     {"id": 1, "title": "Buy milk", "done": False},
>     {"id": 2, "title": "Write chapter 3", "done": True},
> ]
>
> @app.get("/tasks")
> def list_tasks():
>     return tasks
> ```
>
> The line `@app.get("/tasks")` is a **decorator**: a line starting with `@`
> that sits on top of a function and changes what happens to it. You don't need
> to know how decorators work inside to use this one. It means: *when a request
> for `GET /tasks` arrives, call the function below and send back what it
> returns.* FastAPI turns the list into JSON for you.

The decorator explanation answers reader note 1 at the moment the reader would
ask. Each later section adds exactly one idea, with a run step and the
expected output, including what the reader sees when the server is not
running.

## Step 3: consequences outside the chapter

| Where | Change | Why |
| --- | --- | --- |
| Ch. 1 §1.3 | `pip install "fastapi[standard]"` and one sentence on what it adds | Approved D2; the uvicorn command now exists |
| Ch. 4 §4.1 | Short introduction to Pydantic models before the POST listing; the in-memory list switched to models there | Approved D3; ch. 4 previously relied on ch. 3's model |
| New ch. 5 | Outline only: async, `Depends`, settings with `pydantic-settings`, response models, each introduced by a need in the growing app | Approved D1; drafting it is a separate request |
| Terminology | "endpoint" in prose throughout ch. 3–4; FastAPI's "path operation" named once | F6 |

## Step 4: verification and report

```
IMPLEMENTED
  Ch. 3 rewritten (7 sections → 6; one new concept per section; exercise + self-check)
  Ch. 1 §1.3 install command · Ch. 4 §4.1 model introduction · ch. 5 outline
VERIFIED BY
  Every ch. 1, 3 and 4 command and listing run in order in a fresh venv
  (Python 3.12, FastAPI 0.115), including the exercise's model solution: each one
  listed with EXECUTED · PASS, none failing
  Chapters 2–4 re-read in sequence as the stated reader; concept log shows no use
  before explanation
NOT VERIFIED
  Whether readers can now follow it. Suggested: three readers from the early-access
  list work through ch. 1–3 on their own machines; success = a running endpoint
  and explaining @app.get in their own words.
STILL OPEN
  The PDF theme (examples/pdf-visual-review.md) applies to the new chapter too
```

## What made this a good run

- Direction changes were proposed with the exact questions, then implemented
  only as approved.
- The running example and the author's register survived; only the cliff
  went.
- The fix reached chapters 1 and 4, where its consequences were, and nothing
  else.
- "Readers can follow it now" was left as a hypothesis with a test, not a
  claim.
