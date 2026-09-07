const mailer = require('../../lib/mailer')

module.exports = {
  definition: {
    type: 'function',
    function: {
      name: 'send_email',
      description: 'Send an email to a customer',
      parameters: {
        type: 'object',
        properties: {
          to: { type: 'string' },
          subject: { type: 'string' },
          body: { type: 'string' },
        },
        required: ['to', 'subject', 'body'],
      },
    },
  },
  async run({ to, subject, body }) {
    return mailer.send({ to, subject, html: body })
  },
}
