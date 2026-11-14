# Chapter 2 — A quick Python refresher

Before we build an API, let's make sure the Python we need is fresh.

## 2.1 Functions

A function takes inputs, does some work and returns a result:

```python
def add(a, b):
    return a + b

print(add(2, 3))  # 5
```

## 2.2 Dictionaries

A dictionary maps keys to values. APIs send and recieve data that looks a lot
like dictionaries, so you will use them constantly:

```python
task = {"id": 1, "title": "Buy milk", "done": False}
print(task["title"])  # Buy milk
```

## 2.3 Lists of dictionaries

```python
tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Write chapter 3", "done": True},
]
for t in tasks:
    print(t["title"])
```

That's all the Python we need. Let's build an API.
