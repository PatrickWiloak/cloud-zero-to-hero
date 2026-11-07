---
last-updated: 2026-11-07
difficulty: beginner
reading-time: 6 min
---

# Idempotency explained

> **6-minute read. No prerequisites.**

## The one-line answer

An operation is **idempotent** if running it once or running it five times has the same final effect. In a world of retries, network failures, and at-least-once delivery, idempotency is what keeps your system correct.

If you remember nothing else from this page: design every consumer of network messages to be idempotent. The retries are coming whether you planned for them or not.

## Why retries are unavoidable

Three categories of failure all look the same to the caller:

```mermaid
flowchart LR
  C[Client] -->|request| S[Server]
  S -.timeout.-> X[?]
  X --> Q[Did the server process<br/>the request or not?]
```

1. **Request never arrived** - safe to retry; the server didn't see it.
2. **Server processed but response was lost** - the server already did the work; retrying would do it again.
3. **Server is processing right now** - retrying duplicates the work.

The client cannot tell which case it's in. The only safe default is to retry. The only safe way to retry is to make sure duplicates don't break anything.

## What makes an operation idempotent

The standard examples:

- **PUT /resource/123 with full state** - idempotent. Second PUT replaces with the same state.
- **DELETE /resource/123** - idempotent. After the first call, the resource is gone; subsequent calls return "not found" or are no-ops.
- **GET /resource/123** - idempotent (and safe; it doesn't change state).

The non-idempotent classic:

- **POST /transfer { amount: 100 }** - not idempotent. Two POSTs transfer $200.

Anything that adds, sends, charges, or otherwise produces a side effect when invoked is non-idempotent by default. You make it idempotent.

## The idempotency key pattern

The standard fix: the client generates a unique ID per operation and the server deduplicates by it.

```http
POST /transfers
Idempotency-Key: 87a1f-b2c3-..unique-per-attempt..
Content-Type: application/json

{ "from": "alice", "to": "bob", "amount": 100 }
```

Server logic:

1. Look up the key in a deduplication store (Redis, DynamoDB, Postgres).
2. If found, return the previously stored response. Do not run the side effect again.
3. If not found, run the side effect, store the response under the key, return it.

Stripe, AWS APIs (`ClientToken`/`ClientRequestToken`), and most modern payment systems use this pattern. It works.

### Choosing the key
- **Per-attempt** - the client picks a new UUID for every distinct intent. Wrong: this means a retry of the same intent generates a new key, and you're back to duplication.
- **Per-intent** (correct) - the client picks a key tied to the *intent* of the request. The retry uses the *same* key. The server deduplicates.

Practically: generate the key when the user clicks "Pay", reuse it for every retry of that click.

### TTL on the dedup store
Don't keep keys forever. Stripe defaults to 24 hours. After that, the same key submitted again is treated as a new request. Match the TTL to your retry window.

## Without an idempotency key

Three other approaches for when you can't or don't want to use idempotency keys:

### Make the operation conceptually idempotent
Reformulate. Instead of "add $100 to balance", express it as "set balance to $X" - the second write doesn't double-credit. Useful for state-style APIs.

### Conditional writes / optimistic concurrency
"Update record where version = 5 to version = 6". The first write succeeds; the retry sees version = 6 and the condition fails, so it's a no-op (or you handle the conflict explicitly). DynamoDB ConditionExpressions, Cosmos DB ETags, Postgres SELECT ... FOR UPDATE / WHERE version = $expected.

### Natural keys
"INSERT INTO orders WHERE order_id = abc unless exists." The order_id is the natural key; duplicates fail constraint checks.

## In message queues

When SQS, Kafka, or any other system delivers at-least-once, your consumer will see duplicates. Two strategies:

### Idempotent message handler
Same key pattern: dedupe on a message ID, process once, store the result.

### Exactly-once via transaction
Some systems support "process the message and write to the database in one atomic transaction; if either fails, both roll back." Kafka transactions, FoundationDB-style stores. Powerful but limited to specific ecosystems.

## Common pitfalls

### Idempotency at the wrong layer
You made the API endpoint idempotent. The downstream service it calls isn't. The retry through the dedupe API succeeds, but the underlying side effect happened twice. Idempotency must extend through the call chain.

### Dedup window too short
Retry happens at hour 25; the dedup TTL was 24 hours. You charge the customer twice. Pick a TTL longer than your retry window plus headroom.

### Storing the result, not just the key
A retry should return the *same response* the original returned, not just "200 OK." Otherwise the client reconciles wrong. Store the response payload alongside the key.

### Side effects in handler before dedup check
You logged "processing payment for $100" before checking the idempotency key. Now retries log multiple times. Check the dedup store first; return early on hit.

### Parallel retries before the first completes
The user double-clicks "Pay". Two requests with the same idempotency key arrive at the server simultaneously. Both check the store, both miss, both proceed. Now you've charged twice. Use atomic operations (INSERT ... ON CONFLICT, conditional writes, distributed locks) to make the dedup check race-free.

### Ignoring the case where the dedup store fails
The Redis is down. Now your idempotency check fails open or fails closed - either way, you're degraded. Plan for this. Some teams treat dedup-store unavailability as service unavailability.

### Assuming HTTP retries are idempotent
By spec, GET / PUT / DELETE are idempotent; POST is not. But proxies, load balancers, and SDKs sometimes retry POSTs anyway. Assume retries can happen on anything; design accordingly.

## A worked example

A webhook handler that creates a record on each event:

```python
def handle_webhook(event):
    # Check dedup store - the event has its own ID from the source
    if seen_recently(event.id):
        return cached_response(event.id)

    # Atomically claim the ID, then process
    if not try_claim(event.id, ttl=24*3600):
        return cached_response(event.id)  # someone else got it

    result = process_event(event)
    save_response(event.id, result)
    return result
```

This handles duplicates at the source level (webhook providers retry on non-2xx responses). Without it, you'd create the record twice for any webhook that times out client-side.

## What to look at next

- **[Eventual consistency](https://data.noblerworks.com/learn/concepts/eventual-consistency/)** - the world that demands idempotency
- **[Queues vs streams](https://data.noblerworks.com/learn/concepts/queues-vs-streams/)** - delivery semantics
- **[Topic: databases](https://data.noblerworks.com/topics/databases/)** - where dedup state usually lives
- **[Architecture pattern: Event-driven](../../resources/architecture-patterns/event-driven-architecture.md)**

## Check yourself

Try these before you move on. Each answer is collapsed; click it to check yourself.

1. What does it mean for an operation to be idempotent?

    <details>
    <summary>Answer</summary>
    Running it once or running it five times has the same final effect. See: <a href="#the-one-line-answer">The one-line answer</a>
    </details>

2. Why can a client not tell whether to worry about a timed-out request, and what is the safe default?

    <details>
    <summary>Answer</summary>
    It cannot tell whether the request never arrived, was processed with a lost response, or is still processing. The only safe default is to retry, and retrying is only safe if duplicates do not break anything. See: <a href="#why-retries-are-unavoidable">Why retries are unavoidable</a>
    </details>

3. Should an idempotency key be generated per attempt or per intent, and why?

    <details>
    <summary>Answer</summary>
    Per intent. If every retry made a new key, the retry would look like a new request and duplicate the work. See: <a href="#choosing-the-key">Choosing the key</a>
    </details>

4. Two requests with the same idempotency key arrive at the same moment and both miss the dedup store. What happens, and how do you prevent it?

    <details>
    <summary>Answer</summary>
    Both proceed and the customer is charged twice. Use atomic operations such as INSERT ... ON CONFLICT, conditional writes or distributed locks to make the check race-free. See: <a href="#common-pitfalls">Common pitfalls</a>
    </details>
