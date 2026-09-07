const { complete } = require('./client')
const { buildMessages } = require('./prompt')
const { retrieveContext } = require('./retrieve')
const lookupCustomer = require('./tools/lookupCustomer')
const sendEmail = require('./tools/sendEmail')
const db = require('../db/client')

const TOOLS = { lookup_customer: lookupCustomer, send_email: sendEmail }

async function answer({ question, ticket, user, embedding }) {
  const context = await retrieveContext(embedding, user.tenantId)
  let messages = buildMessages({
    question,
    context,
    ticketNotes: ticket.notes,
    attachmentText: ticket.attachmentText,
  })

  for (let i = 0; ; i++) {
    const res = await complete(messages, Object.values(TOOLS).map((t) => t.definition))
    const choice = res.choices[0].message
    messages.push(choice)

    if (!choice.tool_calls) {
      await db.aiLog.create({
        data: {
          userId: user.id,
          prompt: JSON.stringify(messages),
          completion: choice.content,
        },
      })
      return choice.content
    }

    for (const call of choice.tool_calls) {
      const tool = TOOLS[call.function.name]
      const output = await tool.run(JSON.parse(call.function.arguments))
      messages.push({
        role: 'tool',
        tool_call_id: call.id,
        content: JSON.stringify(output),
      })
    }
  }
}

module.exports = { answer }
