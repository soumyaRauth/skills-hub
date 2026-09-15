const { format, isBefore } = require('date-fns')

function dueLabel(dueAt, now = new Date()) {
  const label = format(dueAt, 'd MMM yyyy')
  return isBefore(dueAt, now) ? `${label} (overdue)` : label
}

module.exports = { dueLabel }
