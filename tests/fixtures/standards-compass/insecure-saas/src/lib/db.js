const { PrismaClient } = require('@prisma/client')

const prisma = new PrismaClient({
  datasources: {
    db: { url: 'postgresql://acme_app:Pr0duct10n!@db.internal.acme.io:5432/acme' },
  },
})

module.exports = prisma
