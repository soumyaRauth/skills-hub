import express from "express";

const app = express();
app.use(express.json());

// T-001 walking skeleton: health check only. Classes and bookings are T-002 onward.
app.get("/health", (req, res) => res.json({ ok: true }));

app.listen(process.env.PORT || 3000);
