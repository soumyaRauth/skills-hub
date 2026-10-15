// QUEUE_URL unset: run the job inline, so tests need no broker.
export async function enqueue(job, payload) {
  if (!process.env.QUEUE_URL) return (await import(`./worker/${job}.js`)).run(payload);
  // publish to process.env.QUEUE_URL
}
