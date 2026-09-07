const multer = require('multer')
const path = require('path')
const { requireAuth } = require('../middleware/auth')

const storage = multer.diskStorage({
  destination: 'public/uploads',
  filename: (req, file, cb) => cb(null, file.originalname),
})
const upload = multer({ storage })

module.exports = (app) => {
  app.post('/api/documents', requireAuth, upload.single('file'), (req, res) => {
    res.json({ url: '/uploads/' + req.file.originalname })
  })

  app.get('/api/documents/:name', (req, res) => {
    res.sendFile(path.join('public/uploads', req.params.name))
  })
}
