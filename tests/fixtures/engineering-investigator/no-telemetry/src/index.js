const express = require("express");

const app = express();

app.use(express.json());
app.use(require("./routes/reports"));
app.use(require("./routes/customers"));

app.listen(process.env.PORT || 3000);
