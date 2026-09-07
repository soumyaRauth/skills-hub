const { Pinecone } = require('@pinecone-database/pinecone')

const pinecone = new Pinecone({ apiKey: process.env.PINECONE_API_KEY })
const index = pinecone.index('tickets')

// Semantic search across the ticket corpus.
async function retrieveContext(embedding, tenantId, k = 8) {
  const result = await index.query({ vector: embedding, topK: k, includeMetadata: true })
  return result.matches
    .filter((m) => m.metadata.tenantId === tenantId)
    .map((m) => m.metadata)
}

module.exports = { retrieveContext }
