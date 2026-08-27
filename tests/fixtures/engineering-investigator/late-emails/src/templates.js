const fs = require("node:fs/promises");
const path = require("node:path");
const handlebars = require("handlebars");

const cache = new Map();

async function renderTemplate(name, data) {
  if (!cache.has(name)) {
    const source = await fs.readFile(path.join(__dirname, "..", "templates", `${name}.hbs`), "utf8");
    cache.set(name, handlebars.compile(source));
  }
  return cache.get(name)(data);
}

module.exports = { renderTemplate };
