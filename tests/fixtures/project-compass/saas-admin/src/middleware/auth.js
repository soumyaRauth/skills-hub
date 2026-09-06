const { verifySession } = require('../session');

// Establishes who the caller is. What they are allowed to do is decided
// separately by each route handler.
async function requireUser(req, res, next) {
  const user = await verifySession(req.headers.authorization);
  if (!user) return res.status(401).json({ error: 'unauthenticated' });
  req.user = user;
  next();
}

module.exports = { requireUser };
