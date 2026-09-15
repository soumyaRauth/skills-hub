const express = require('express')
const db = require('../db')
const { sendError } = require('./errors')
const { requireApiKey } = require('../middleware/apiKey')

const router = express.Router()

// POST /v1/refunds — retries with the same Idempotency-Key return the first result
router.post('/v1/refunds', requireApiKey, express.json(), async (req, res) => {
  const key = req.get('Idempotency-Key')
  if (!key) return sendError(res, 400, 'idempotency_key_required', 'Idempotency-Key header is required')
  const prior = await db.oneOrNone('SELECT response FROM idempotency WHERE account_id = $1 AND key = $2', [req.apiKey.accountId, key])
  if (prior) return res.status(200).json(prior.response)
  const refund = await db.one(
    'INSERT INTO refunds (account_id, payment_id, amount_cents) VALUES ($1, $2, $3) RETURNING id, status, created_at',
    [req.apiKey.accountId, req.body.payment_id, req.body.amount_cents],
  )
  await db.none('INSERT INTO idempotency (account_id, key, response) VALUES ($1, $2, $3)', [req.apiKey.accountId, key, refund])
  res.status(201).json(refund)
})

module.exports = router
