const next = require("next");
const http = require("http");
const { queue } = require("./queue/connection");

const app = next({ dev: false });
const handle = app.getRequestHandler();

app.prepare().then(() => {
  http.createServer((req, res) => {
    if (req.url === "/api/health") {
      res.writeHead(200, { "Content-Type": "application/json" });
      return res.end(JSON.stringify({ status: "ok" }));
    }
    return handle(req, res);
  }).listen(3000, () => {
    console.log("listening on 3000");
  });
});

module.exports = { queue };
