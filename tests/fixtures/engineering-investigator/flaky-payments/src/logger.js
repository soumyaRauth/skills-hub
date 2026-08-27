function emit(level, event, fields) {
  const line = Object.entries(fields || {})
    .map(([k, v]) => `${k}=${v}`)
    .join(" ");
  process.stdout.write(`${new Date().toISOString()} ${level} ${event} ${line}\n`);
}

module.exports = {
  info: (event, fields) => emit("INFO", event, fields),
  warn: (event, fields) => emit("WARN", event, fields),
  error: (event, fields) => emit("ERROR", event, fields)
};
