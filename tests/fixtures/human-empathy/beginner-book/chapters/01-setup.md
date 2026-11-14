# Chapter 1 — Getting set up

This book is for you if you know basic Python — variables, functions, lists,
dictionaries, loops — and have never built anything for the web. By the end
you will have built a small to-do API and deployed it so anyone can use it.

We use Python 3.12, FastAPI 0.115 and Pydantic 2 throughout.

## 1.1 Check your Python

Open a terminal and run:

```
python3 --version
```

You should see `Python 3.12` or later.

## 1.2 Create a project folder

```
mkdir todo-api
cd todo-api
python3 -m venv .venv
source .venv/bin/activate
```

On Windows, activate with `.venv\Scripts\activate` instead.

## 1.3 Install FastAPI

```
pip install fastapi
```

That's everything you need. In the next chapter we refresh the Python we'll
rely on.
