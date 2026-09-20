const fs = require("fs/promises");
const path = require("path");

const UPLOAD_DIR = path.join(process.cwd(), "uploads");

async function storeAttachment(name, buffer) {
  await fs.mkdir(UPLOAD_DIR, { recursive: true });
  const target = path.join(UPLOAD_DIR, name);
  await fs.writeFile(target, buffer);
  return `/uploads/${name}`;
}

async function readAttachment(name) {
  return fs.readFile(path.join(UPLOAD_DIR, name));
}

module.exports = { storeAttachment, readAttachment, UPLOAD_DIR };
