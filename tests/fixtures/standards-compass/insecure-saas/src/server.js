const express = require('express')
const log = require('./lib/log')

const app = express()
app.use(express.json())

require('./api/auth')(app)
require('./api/search')(app)
require('./api/upload')(app)
require('./api/admin/users')(app)
require('./api/admin/exports')(app)
require('./api/admin/billing')(app)

app.use((err, req, res, next) => {
  log.error(err, req)
  res.status(500).json({ error: err.message, stack: err.stack })
})

app.listen(3000)
