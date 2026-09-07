module.exports = {
  info: (msg) => console.log(new Date().toISOString(), 'INFO', msg),
  error: (err, req) =>
    console.error(new Date().toISOString(), 'ERROR', err.stack, JSON.stringify(req?.body)),
}
