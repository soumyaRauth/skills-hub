const express = require('express')
const db = require('../db')
const { sendError } = require('./errors')
const { requireApiKey } = require('../middleware/apiKey')

const router = express.Router()

// GET /v1/payments?cursor=&limit=
router.get('/v1/payments', requireApiKey, async (req, res) => {
  const limit = Number(req.query.limit ?? 25)
  if (!Number.isInteger(limit) || limit < 1 || limit > 100) {
    return sendError(res, 400, 'invalid_limit', 'limit must be between 1 and 100')
  }
  const before = req.query.cursor ? Buffer.from(req.query.cursor, 'base64url').toString() : null
  const rows = await db.many(
    `SELECT id, amount_cents, currency, status, created_at FROM payments
      WHERE account_id = $1 AND ($2::timestamptz IS NULL OR created_at < $2)
      ORDER BY created_at DESC LIMIT $3`,
    [req.apiKey.accountId, before, limit + 1],
  )
  const page = rows.slice(0, limit)
  const next = rows.length > limit ? Buffer.from(page[page.length - 1].created_at.toISOString()).toString('base64url') : null
  res.json({ data: page, next_cursor: next })
})

module.exports = router
