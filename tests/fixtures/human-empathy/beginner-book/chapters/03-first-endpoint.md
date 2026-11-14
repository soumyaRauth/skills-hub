# Chapter 3 — Your first endpoint

In this chapter we'll build a production-grade async REST API with dependency
injection, typed models and settings management. Here is the whole thing:

```python
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, BaseSettings

class Settings(BaseSettings):
    app_name: str = "Todo API"

class Task(BaseModel):
    id: int
    title: str
    done: bool = False

app = FastAPI()
tasks: list[Task] = [Task(id=1, title="Buy milk")]

def get_settings() -> Settings:
    return Settings()

@app.get("/tasks", response_model=list[Task])
async def list_tasks(settings: Settings = Depends(get_settings)):
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    for t in tasks:
        if t.id == task_id:
            return t
    raise HTTPException(status_code=404, detail="Not found")
```

Save it as `main.py`.

## 3.1 Running it

Start the server:

```
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/tasks` and you'll see your tasks as JSON.
Obviously, FastAPI also generates interactive docs at `/docs`.

## 3.2 Path operations

Simply decorate your function with `@app.get` and FastAPI registers the route.
The handler is `async`, so the endpoint can serve other requests while it
waits. Each path operation declares its response model, and FastAPI validates
what the route returns against it.

`task_id: int` in the signature makes `{task_id}` in the path a typed path
parameter; FastAPI converts it for you and rejects anything that isn't an
integer. This is trivially extended to query parameters.

## 3.3 Dependency injection

`Depends(get_settings)` tells FastAPI to call `get_settings` and pass the
result in. Dependencies can depend on other dependencies, which gives you a
clean way to share database sessions, authentication and configuration across
endpoints.

## 3.4 Settings

`BaseSettings` reads values from environment variables, so you can change
`app_name` without changing code.

## 3.5 Response models

`response_model=list[Task]` filters and validates the output. If a route
returns a field that isn't on the model, it's dropped.

## 3.6 What is HTTP, anyway?

HTTP is the protocol your browser uses to talk to a server. A client sends a
request with a method (`GET`, `POST`, ...) and a path (`/tasks`); the server
sends back a response with a status code (`200`, `404`, ...) and a body —
here, JSON.

## Summary

Now you know how to build APIs! In the next chapter we'll accept data from
clients.
