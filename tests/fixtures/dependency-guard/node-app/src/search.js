const { z } = require('zod')

const Query = z.object({ q: z.string().max(200) })

function onSearchInput(input, runSearch) {
  const { q } = Query.parse({ q: input })
  runSearch(q) // fires on every keystroke
}

module.exports = { onSearchInput }
