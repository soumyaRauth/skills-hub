const { channel } = require('./broker')

async function orderShipped(order, shipment) {
  await channel.publish('orders', 'order.shipped', Buffer.from(JSON.stringify({
    orderId: order.id,
    trackingNo: shipment.tracking,
    carrier: shipment.carrier,
    shippedAt: shipment.created_at,
  })))
}

module.exports = { orderShipped }
