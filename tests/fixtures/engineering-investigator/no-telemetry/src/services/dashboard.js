const Redis = require("ioredis");
const prisma = require("../prisma");

const redis = new Redis(process.env.REDIS_URL);
const CACHE_KEY = "dashboard:aggregate";
const TTL_SECONDS = 60;

async function getDashboard(organizationId) {
  const cached = await redis.get(`${CACHE_KEY}:${organizationId}`);
  if (cached) return JSON.parse(cached);

  const aggregate = await buildAggregate(organizationId);
  await redis.setex(`${CACHE_KEY}:${organizationId}`, TTL_SECONDS, JSON.stringify(aggregate));
  return aggregate;
}

async function buildAggregate(organizationId) {
  const [jobs, invoices, users] = await Promise.all([
    prisma.job.groupBy({ by: ["status"], where: { organizationId }, _count: true }),
    prisma.invoice.aggregate({ where: { organizationId }, _sum: { totalCents: true } }),
    prisma.user.count({ where: { organizationId } })
  ]);

  return { jobs, invoices, users, builtAt: new Date().toISOString() };
}

module.exports = { getDashboard };
