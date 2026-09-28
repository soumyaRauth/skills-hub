const express = require("express");
const { SERVICES } = require("./services");

const app = express();
app.use(express.json());

app.get("/health", (req, res) => res.json({ ok: true }));
app.get("/services", (req, res) => res.json(SERVICES));

app.listen(process.env.PORT || 3000);
