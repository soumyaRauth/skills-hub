// Thin wrapper over the pool the SSO proxy hands us. Not interesting.
async function query(sql, args) {
  throw new Error('not wired in this skeleton');
}

module.exports = { query };
