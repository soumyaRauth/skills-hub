const jwt = require('jsonwebtoken')

const SECRET = process.env.JWT_SECRET || 'dev-secret-do-not-ship'

function requireAuth(req, res, next) {
  const token = req.headers.authorization?.replace('Bearer ', '')
  if (!token) return res.status(401).json({ error: 'unauthenticated' })
  try {
    req.user = jwt.verify(token, SECRET)
    next()
  } catch (e) {
    return res.status(401).json({ error: 'unauthenticated' })
  }
}

// Used by most of the admin API.
function requireRole(role) {
  return (req, res, next) => {
    if (req.user?.role !== role) return res.status(403).json({ error: 'forbidden' })
    next()
  }
}

module.exports = { requireAuth, requireRole }
