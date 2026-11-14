# Chapter 4 — Accepting data

So far our API only sends data. Now clients will send us tasks with `POST`.

## 4.1 A POST endpoint

```python
@app.post("/tasks", response_model=Task, status_code=201)
async def create_task(task: Task):
    tasks.append(task)
    return task
```

Because `task` is a Pydantic model, FastAPI reads the JSON body, validates it,
and gives you a `Task`.
