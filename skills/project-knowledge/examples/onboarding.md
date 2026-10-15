# Example — A new developer, through the MCP server

A developer clones the repository, opens Claude Code, approves the
`project-knowledge` MCP server, and asks:

> I'm new here. Why does my test order stay "pending" after the charge succeeds?

This is not a request to learn the codebase, so the skill does not run a
learning pass. It is in **reading mode**: the knowledge exists, so it is read
before the code.

## What happens

1. `knowledge_search` for `order pending paid` returns one section from
   `gotchas.md`:

   ```markdown
   ## An order is paid only when the provider's webhook arrives
   A successful charge leaves the order pending. `payments/webhooks.ts` marks it
   paid. Locally, no webhook arrives unless the provider's CLI forwards it.
   ```

2. `knowledge_status` says the knowledge is 2 commits behind `HEAD`, and neither
   commit touches the payment path.
3. The agent confirms the gate against the code it names, then answers from both.

## The answer

> The charge worked. Orders only turn paid when the provider's webhook reaches
> `payments/webhooks.ts`, and locally nothing forwards it. Run the provider's
> webhook-forwarding CLI against your dev server and place the order again.
> (From the project knowledge, confirmed in `payments/webhooks.ts`.)

## What this example demonstrates

The newcomer got an answer someone already knew, in one search, instead of an
investigation. The agent still checked the code,
because the knowledge was behind `HEAD`, and said where the answer came from.
