function requestLogger(req, res, next) {
  res.on('finish', () => {
    console.log(JSON.stringify({
      method: req.method,
      path: req.path,
      status: res.statusCode,
      at: new Date().toISOString(),
    }));
  });
  next();
}

module.exports = { requestLogger };
