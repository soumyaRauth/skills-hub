const labels = require('../labels')

async function onOrderShipped(msg) {
  const event = JSON.parse(msg.content.toString())
  await labels.markDispatched(event.orderId, {
    tracking: event.trackingNo,
    carrier: event.carrier,
  })
}

module.exports = { onOrderShipped }
