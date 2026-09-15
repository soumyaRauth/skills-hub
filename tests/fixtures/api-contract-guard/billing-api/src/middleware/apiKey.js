const db = require('../db')

async function requireApiKey(req, res, next) {
  const key = req.get('Authorization')?.replace(/^Bearer /, '')
  const row = key && (await db.one('SELECT account_id FROM api_keys WHERE key_hash = digest($1)', [key]))
  if (!row) return res.status(401).json({ error: { code: 'unauthorized', message: 'Invalid API key' } })
  req.apiKey = { accountId: row.account_id }
  next()
}

module.exports = { requireApiKey }
