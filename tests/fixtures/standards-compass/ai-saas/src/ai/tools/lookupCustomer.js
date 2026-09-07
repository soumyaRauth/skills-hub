const db = require('../../db/client')

module.exports = {
  definition: {
    type: 'function',
    function: {
      name: 'lookup_customer',
      description: 'Look up a customer by email address',
      parameters: {
        type: 'object',
        properties: { email: { type: 'string' } },
        required: ['email'],
      },
    },
  },
  async run({ email }) {
    return db.customer.findUnique({
      where: { email },
      include: { invoices: true, tickets: true },
    })
  },
}
