import express from "express";
import { listNotes, createNote } from "./notes.js";

const app = express();
app.use(express.json());

app.get("/notes", (req, res) => res.json(listNotes()));
app.post("/notes", (req, res) => res.status(201).json(createNote(req.body.text)));

app.listen(3000);
