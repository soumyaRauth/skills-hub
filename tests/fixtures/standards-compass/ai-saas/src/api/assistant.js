const { answer } = require('../ai/agent')
const { requireAuth } = require('../middleware/auth')
const { embed } = require('../ai/embed')
const db = require('../db/client')

module.exports = (app) => {
  app.post('/api/assistant', requireAuth, async (req, res) => {
    const ticket = await db.ticket.findUnique({ where: { id: req.body.ticketId } })
    const embedding = await embed(req.body.question)
    const reply = await answer({
      question: req.body.question,
      ticket,
      user: req.user,
      embedding,
    })
    res.json({ reply })
  })
}
