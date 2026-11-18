# 0002 - Credit per Checkout session, record the event after success

**Context.** Stripe delivers webhooks at least once and retries failures for up
to three days. A naive handler can credit twice, or mark an event done before
the credits land and lose the payment.

**Options.**
1. Record the event ID first, then credit (a crash in between loses credits).
2. Credit keyed on the Checkout session ID, then record the event ID.

**Decision.** Option 2. The signature is checked on the raw body. Credits are
granted with the session ID as the ledger key, then `claim_stripe_event` records
the event. Any failure returns 500 so Stripe retries.

**Consequences.** Duplicate deliveries and retries are safe. Prices come from the
server pack list, so the browser cannot change the amount.
