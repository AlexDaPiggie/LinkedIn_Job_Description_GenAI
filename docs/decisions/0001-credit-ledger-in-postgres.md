# 0001 - Credits change only through SQL functions

**Context.** Refine requests cost one credit. The first version read the balance
in Python, then wrote the new balance. Two requests at once could both pass the
check, and a retried request could charge twice.

**Options.**
1. Read-then-write in Python with a lock (breaks with more than one container).
2. A single SQL function that checks and subtracts in one statement, with a
   unique key per charge.

**Decision.** Option 2. `spend_credits`, `refund_credits` and `grant_credits` in
`docs/migrations/001_credit_ledger.sql` write to an append-only `credit_ledger`
with a unique key, and are callable only with the service-role key.

**Consequences.** A repeated request with the same key changes nothing. The
ledger doubles as an audit trail. Without the migration or the key, credit
operations fail closed instead of giving free use.
