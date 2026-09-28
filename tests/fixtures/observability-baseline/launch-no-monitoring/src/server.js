import express from "express";
import { listBooks, addBook } from "./db.js";

const app = express();
app.use(express.json());

app.use((req, res, next) => {
  console.log(req.method, req.url, req.body);
  next();
});

// ponytail: fixture stand-in for real auth
app.use((req, res, next) => {
  req.userId = req.get("x-user-id");
  next();
});

app.get("/books", async (req, res) => {
  try {
    res.json(await listBooks(req.userId));
  } catch (err) {
    console.log("error", err);
    res.status(500).send("Something went wrong");
  }
});

app.post("/books", async (req, res) => {
  try {
    res.status(201).json(await addBook(req.userId, req.body.title, req.body.author));
  } catch (err) {
    console.log("error", err);
    res.status(500).send("Something went wrong");
  }
});

const port = process.env.PORT || 3000;
app.listen(port, () => console.log("listening on " + port));
