# 0004 - Free generate, paid refine

**Context.** The product has to be useful without an account, but every LLM call
costs money and the free endpoint attracts bots.

**Options.**
1. Paywall everything behind sign-in.
2. Free generate, quick edits and quality checks; charge only for open-ended
   typed refine requests.

**Decision.** Option 2, with Turnstile, a per-IP daily limit and a global daily
cap on the free path. New accounts get 20 credits once per mailbox.

**Consequences.** A visitor gets a full draft in one step. Spend on the free path
is bounded by the global cap. Refunds are automatic when the model fails.
