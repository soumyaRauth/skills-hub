const express = require("express");
const orders = require("./api/orders");
const checkout = require("./api/checkout");

const app = express();
app.use(express.json());
app.use(orders);
app.use(checkout);

app.listen(process.env.PORT || 3000);
