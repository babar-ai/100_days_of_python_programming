# 🚦 Rate Limiting — System Design Interview Notes

> **Purpose:** Quick revision notes for designing a distributed Rate Limiter in a system design interview.

---

## 1. What is Rate Limiting?

A **rate limiter** controls how many requests a client/user/service can make within a specified period.

### Example

Suppose an API allows:

```text
100 requests / minute / user
```

If a user sends:

```text
Request 1  → ✅
Request 2  → ✅
...
Request 100 → ✅
Request 101 → ❌ 429 Too Many Requests
```

The rate limiter sits **before the backend service** and decides whether a request should continue.

---

# 2. Why Do We Need Rate Limiting?

### 1. Protect against DoS / abuse

Prevents a single user, bot, or attacker from consuming all system resources.

### 2. Prevent server overload

If traffic suddenly increases:

```text
Millions of requests
       ↓
Rate Limiter
       ↓
Only allowed traffic
       ↓
API Servers
```

### 3. Reduce infrastructure cost

Fewer unnecessary API calls → fewer compute resources.

Especially important when using **paid third-party APIs**.

### 4. Fair usage

Prevents one user from consuming resources that should be available to other users.

---

# 3. Functional Requirements

A good rate limiter should:

* Accurately limit excessive requests
* Support different rate-limiting rules
* Support limits by:

  * User ID
  * IP address
  * API endpoint
  * Device
  * API key
* Inform clients when they are throttled
* Work in a distributed environment

---

# 4. Non-Functional Requirements

Important interview requirements:

### Low latency

Rate limiting should add very little latency.

### High scalability

Must handle a huge number of requests and users.

### Low memory usage

Don't store unnecessary request information.

### High availability

Failure of the rate limiter should not bring down the entire application.

### Distributed consistency

Multiple API servers must share rate-limit state correctly.

---

# 5. Where Should Rate Limiting Be Implemented?

There are two common approaches.

## Client-side

```text
Client
  ↓
Rate Limiter
  ↓
Server
```

### Problem

Client-side rate limiting is **not trustworthy**.

A malicious client can simply bypass or modify it.

Therefore:

> ❌ Don't rely on client-side rate limiting for security.

---

## Server-side

```text
Client
   ↓
Rate Limiter
   ↓
API Servers
```

This is much more reliable.

The rate limiter can be implemented as:

* Middleware
* API Gateway
* Separate rate-limiting service

### Common architecture

```text
              ┌──────────────┐
              │    Client    │
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
              │ Rate Limiter │
              └──────┬───────┘
                     │
              ┌──────┴───────┐
              │              │
             Allow          Reject
              │              │
              ▼              ▼
        API Servers       HTTP 429
```

---

# 6. HTTP 429

When a request exceeds the limit:

```http
HTTP/1.1 429 Too Many Requests
```

The client should know when it can try again.

Useful headers include:

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Retry-After: 30
```

Meaning:

```text
Limit      = 100 requests
Remaining  = 0
Retry      = wait 30 seconds
```

---

# 7. Main Rate-Limiting Algorithms

Know these five:

| Algorithm              | Main Idea                          | Major Advantage          | Major Problem          |
| ---------------------- | ---------------------------------- | ------------------------ | ---------------------- |
| Token Bucket           | Requests consume tokens            | Allows controlled bursts | Parameter tuning       |
| Leaky Bucket           | Queue drains at fixed rate         | Smooth traffic           | Adds queue/latency     |
| Fixed Window           | Counter per time window            | Very simple              | Boundary burst problem |
| Sliding Window Log     | Store request timestamps           | Very accurate            | High memory usage      |
| Sliding Window Counter | Combine current + previous windows | Good balance             | Approximation          |

---

# 8. Token Bucket ⭐

> **Most important algorithm to understand for interviews.**

Imagine a bucket containing tokens.

```text
             Refill
               ↓
        ┌──────────────┐
        │ 🟡 🟡 🟡 🟡 │
        │    BUCKET    │
        └──────┬───────┘
               │
            Request
               ↓
         Consume token
```

Every request consumes **one token**.

If a token exists:

```text
Request → ✅ Allowed
```

If no token exists:

```text
Request → ❌ Rejected
```

---

## Token Bucket Parameters

There are two important parameters:

### 1. Bucket Size

Maximum number of tokens.

Example:

```text
Bucket size = 10
```

Maximum burst = approximately 10 requests if the bucket is full.

### 2. Refill Rate

How quickly tokens are added.

Example:

```text
Refill rate = 2 tokens / second
```

Therefore:

```text
Bucket size = 10
Refill rate = 2/sec
```

A user can make a short burst of 10 requests, but sustained traffic is controlled by the refill rate.

---

## Token Bucket Example

Configuration:

```text
Bucket = 5 tokens
Refill = 1 token/sec
```

Initial state:

```text
🟡 🟡 🟡 🟡 🟡
```

Five requests:

```text
Request → 🟡 → allowed
Request → 🟡 → allowed
Request → 🟡 → allowed
Request → 🟡 → allowed
Request → 🟡 → allowed
```

Bucket becomes:

```text
EMPTY
```

Next request:

```text
Request → ❌ 429
```

After one second:

```text
🟡
```

One request can pass.

---

## Token Bucket Advantages

✅ Simple

✅ Memory efficient

✅ Allows controlled bursts

✅ Good fit for APIs

## Token Bucket Disadvantages

❌ Bucket size needs tuning

❌ Refill rate needs tuning

---

# 9. Leaky Bucket

Instead of storing **tokens**, we store **requests in a queue**.

```text
Incoming Requests
       ↓
┌───────────────────┐
│ Request Queue     │
│ R1                │
│ R2                │
│ R3                │
└─────────┬─────────┘
          │
          ↓
 Process at fixed rate
```

Example:

```text
Queue size = 10
Outflow = 2 requests/sec
```

Requests are processed at a constant rate.

If the queue becomes full:

```text
New request → ❌ rejected
```

---

## Token Bucket vs Leaky Bucket

### Token Bucket

```text
Allows bursts
      ↓
Requests can be processed immediately
```

### Leaky Bucket

```text
Smooths traffic
      ↓
Requests wait in queue
      ↓
Processed at fixed rate
```

### Remember

> **Token Bucket = controls average rate + allows bursts**

> **Leaky Bucket = smooths output rate**

---

# 10. Fixed Window Counter

Divide time into fixed intervals.

Example:

```text
Limit = 5 requests/minute
```

Windows:

```text
12:00:00 ───── 12:01:00
12:01:00 ───── 12:02:00
12:02:00 ───── 12:03:00
```

For each window:

```text
counter = 0
```

Every request:

```text
counter += 1
```

If:

```text
counter >= limit
```

reject the request.

---

## Fixed Window Problem ⚠️

The biggest problem is the **boundary burst**.

Suppose:

```text
Limit = 5 requests/minute
```

User sends:

```text
12:00:59 → 5 requests
12:01:01 → 5 requests
```

The system allows:

```text
10 requests within ~2 seconds
```

Even though the intended limit is:

```text
5 requests/minute
```

### Interview phrase

> "Fixed windows are simple and memory efficient, but they suffer from boundary bursts."

---

# 11. Sliding Window Log

Instead of counting requests per fixed window, store their timestamps.

Example:

```text
Limit = 3 requests/minute
```

Store:

```text
12:00:10
12:00:25
12:00:40
```

When a new request arrives:

### Step 1

Remove timestamps older than the current rolling window.

### Step 2

Add the new timestamp.

### Step 3

Count timestamps.

```text
count <= limit
      ↓
    Allow

count > limit
      ↓
    Reject
```

---

## Advantages

✅ Very accurate

A rolling window will not exceed the configured limit.

## Disadvantages

❌ Stores individual timestamps

❌ High memory consumption at large scale

A Redis sorted set can be used for storing timestamps.

---

# 12. Sliding Window Counter

A hybrid approach between:

```text
Fixed Window Counter
        +
Sliding Window Log
```

Instead of storing every timestamp, maintain counters for windows.

The current rolling count can be estimated using:

```text
Current Window Count
+
Previous Window Count × Overlap Percentage
```

### Why use it?

It provides a good balance between:

```text
Accuracy
   +
Memory efficiency
```

---

# 13. Algorithm Comparison — Interview Cheat Sheet

```text
                    BURST     MEMORY     ACCURACY
----------------------------------------------------
Token Bucket          ✅         ✅          Good
Leaky Bucket          ❌         ✅          Good
Fixed Window          ✅         ✅          Low
Sliding Log           ❌         ❌          Excellent
Sliding Counter       ⚠️         ✅          Good
```

### Quick selection

**Need bursts?**

→ Token Bucket

**Need smooth constant output?**

→ Leaky Bucket

**Need simplest implementation?**

→ Fixed Window

**Need maximum accuracy?**

→ Sliding Window Log

**Need good balance?**

→ Sliding Window Counter

---

# 14. Where Do We Store Rate-Limit Data?

❌ Database is usually not ideal.

Why?

```text
Database
   ↓
Disk I/O
   ↓
Higher latency
```

Instead:

```text
Redis / In-memory cache
```

because rate limiting needs extremely fast reads/writes.

ByteByteGo specifically discusses Redis and commands such as:

```text
INCR
EXPIRE
```

---

# 15. Basic Architecture with Redis

```text
                  ┌──────────┐
                  │  Client  │
                  └────┬─────┘
                       │
                       ▼
              ┌────────────────┐
              │ Rate Limiter   │
              │  Middleware    │
              └───────┬────────┘
                      │
                 Check Counter
                      │
                      ▼
                ┌───────────┐
                │   Redis   │
                └─────┬─────┘
                      │
             ┌────────┴────────┐
             │                 │
          Allowed            Limit
             │                 │
             ▼                 ▼
       API Servers            429
```

---

# 16. Basic Rate-Limiter Flow

```text
Request
   ↓
Identify client
   ↓
Load rate-limit rule
   ↓
Load state from Redis
   ↓
Check limit
   ↓
 ┌───────────────┐
 │               │
 ▼               ▼
Allowed       Rejected
 │               │
 ▼               ▼
Increment      HTTP 429
counter
 │
 ▼
API Server
```

---

# 17. Rate-Limiting Rules

Rules can be different depending on the use case.

### By user

```text
user:123
100 requests/min
```

### By IP

```text
IP:192.168.x.x
100 requests/min
```

### By endpoint

```text
POST /login
5 requests/min
```

### By API key

```text
API_KEY_X
10,000 requests/day
```

### Multiple rules

A user might have:

```text
POST /posts      → 1/sec
POST /friends    → 150/day
POST /likes      → 5/sec
```

Therefore, multiple buckets/counters may be required.

---

# 18. Distributed Rate Limiting ⚠️

This is one of the **most important interview topics**.

Imagine:

```text
             Client
                │
        ┌───────┴───────┐
        ↓               ↓
 Rate Limiter 1    Rate Limiter 2
        │               │
        ↓               ↓
       ??              ??
```

If each server maintains its own counter:

```text
Server 1 → 100 requests
Server 2 → 100 requests
```

The user may actually get:

```text
200 requests
```

when the intended limit is:

```text
100 requests
```

---

# 19. Why Centralized Redis?

Use a shared store:

```text
                    ┌──────────────┐
                    │    Redis     │
                    └──────┬───────┘
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
      Rate Limiter 1             Rate Limiter 2
             ▲                           ▲
             │                           │
          Client 1                    Client 2
```

All rate limiter instances see the same state.

### Key idea

> In a distributed rate limiter, rate-limit state must be shared or otherwise coordinated across instances.

---

# 20. Race Condition ⚠️

A naive implementation might do:

```text
1. READ counter
2. CHECK counter
3. INCREMENT counter
```

Suppose:

```text
Counter = 3
Limit = 4
```

Two requests arrive simultaneously.

### Request 1

```text
Read → 3
Check → 3 < 4
Increment → 4
```

### Request 2

At the same time:

```text
Read → 3
Check → 3 < 4
Increment → 4
```

Both requests are allowed.

But expected result:

```text
5
```

Actual result:

```text
4
```

This is a **race condition**.

---

# 21. How to Solve Race Conditions?

The check + update operation should be **atomic**.

Possible approaches:

### Redis atomic operations

Use atomic Redis commands where appropriate.

### Redis Lua scripts

Perform:

```text
CHECK
+
UPDATE
```

as one atomic operation.

### Atomic increment

Avoid separate:

```text
GET
CHECK
SET
```

operations when an atomic operation can perform the required logic.

---

# 22. Sticky Sessions?

One possible solution:

```text
User A
  ↓
Always Rate Limiter 1
```

This is called **sticky sessions**.

But it is generally not a good solution because:

❌ Poor scalability

❌ Uneven load

❌ Reduced flexibility

❌ Failure of one rate limiter can cause problems

Better:

```text
Multiple Rate Limiters
        ↓
 Shared Redis
```

---

# 23. Rate-Limited Requests: What Should We Do?

There are two major choices.

### Option 1 — Drop

```text
Request
   ↓
Rate limited
   ↓
429
```

Good for:

* API calls
* spam
* unnecessary requests

### Option 2 — Queue

```text
Request
   ↓
Rate limited
   ↓
Message Queue
   ↓
Worker
   ↓
Process later
```

Good when requests should eventually be processed.

Example:

```text
Order processing
```

You may not want to simply discard the order.

---

# 24. Multi-Data-Center Architecture

A global application may have:

```text
           Users
             │
       Global Routing
             │
      ┌──────┴──────┐
      ▼             ▼
   US Region      Asia Region
      │             │
      ▼             ▼
 Rate Limiter    Rate Limiter
      │             │
      ▼             ▼
    Redis         Redis
```

Users should ideally be routed to a nearby/appropriate region.

Why?

```text
User → nearby rate limiter
```

reduces network latency.

---

# 25. Consistency

In distributed systems, perfect synchronization can be expensive.

Rate limiters can often tolerate **eventual consistency**, depending on the business requirement.

For example:

```text
Configured limit = 100 req/sec
```

A tiny temporary discrepancy may be acceptable.

But for extremely sensitive limits, stronger consistency may be required.

### Interview question

> "Do we need strong consistency?"

Answer:

> "It depends on the business requirement. For many rate-limiting scenarios, a small amount of temporary inconsistency is acceptable in exchange for lower latency and higher availability."

---

# 26. Fault Tolerance

What happens if Redis goes down?

This is an important interview question.

Possible strategies:

### Fail-open

```text
Redis unavailable
      ↓
Allow request
```

Pros:

* Application remains available

Cons:

* Rate limiting is temporarily bypassed

### Fail-closed

```text
Redis unavailable
      ↓
Reject request
```

Pros:

* Protects backend

Cons:

* A Redis failure can block legitimate users

### Which should you choose?

Depends on the system.

For a critical payment/security API:

```text
Fail-closed may be safer
```

For a general consumer API:

```text
Fail-open may provide better availability
```

Always explain the trade-off.

---

# 27. Performance Optimization

Rate limiter itself must not become a bottleneck.

Important techniques:

### 1. Use in-memory systems

Redis is much faster than a traditional database for this workload.

### 2. Keep state small

Store only what is necessary.

For token bucket:

```text
tokens
last_refill_time
```

may be enough.

### 3. Use geographically close rate limiters

Reduce network latency.

### 4. Cache rules locally

Rate-limit configuration doesn't necessarily need to be fetched from a database for every request.

---

# 28. Monitoring

A production rate limiter should expose metrics.

Important metrics:

```text
Total requests
Allowed requests
Rejected requests
429 rate
Latency
Redis latency
Redis errors
Queue size
Requests per user/IP
```

Monitor:

### Are rules too strict?

If many legitimate requests are rejected:

```text
Too many 429s
      ↓
Rules may be too strict
```

### Are rules too weak?

If backend traffic is still overwhelming the system:

```text
Traffic spike
    ↓
Rate limiter ineffective
```

Consider changing the algorithm/rules.

---

# 29. Hard vs Soft Rate Limiting

### Hard limit

The threshold cannot be exceeded.

```text
Limit = 100

100 → ✅
101 → ❌
```

### Soft limit

The system may temporarily exceed the limit.

```text
Limit = 100

Short burst → 105 → possibly allowed
```

Useful when small temporary bursts are acceptable.

---

# 30. Layer at Which Rate Limiting Happens

Rate limiting does not have to happen only at HTTP/application level.

### Layer 7

Application/API level.

Example:

```text
POST /login
```

### Layer 3

Network/IP level.

Example:

```text
IP-based traffic filtering
```

---

# 31. Interview Design — Recommended Answer

If the interviewer says:

> "Design a distributed rate limiter."

A strong approach is:

### Step 1 — Clarify requirements

Ask:

```text
What are we limiting?

User?
IP?
API key?
Endpoint?

What is the scale?

Do we allow bursts?

Do requests need to be queued?

What consistency is required?
```

---

### Step 2 — Choose algorithm

For a general API:

> "I would start with a Token Bucket because it is memory efficient, simple, and supports controlled bursts."

---

### Step 3 — Draw architecture

```text
Client
  │
  ▼
Load Balancer / API Gateway
  │
  ▼
Rate Limiter
  │
  ├──────────► Redis
  │
  ▼
API Servers
```

---

### Step 4 — Explain Redis

Redis stores:

```text
client identifier
+
rate-limit state
```

For example:

```text
user:123
tokens = 7
last_refill = timestamp
```

---

### Step 5 — Discuss concurrency

Say:

> "Because multiple rate limiter instances can update the same user's state concurrently, the check-and-update operation must be atomic."

Mention:

```text
Redis atomic operations
Lua scripts
```

---

### Step 6 — Discuss failures

Ask/decide:

```text
Redis failure?
      ↓
Fail-open or fail-closed?
```

Explain the trade-off.

---

### Step 7 — Discuss scaling

Mention:

```text
Redis Cluster
Multiple rate limiter instances
Multi-region deployment
Local caching of rules
Load balancing
```

---

### Step 8 — Discuss monitoring

Mention:

```text
429 rate
Latency
Request volume
Redis health
Rejected requests
```

---

# 32. 60-Second Interview Answer ⭐

If you need to answer quickly:

> "I would implement the rate limiter on the server side, preferably at an API gateway or middleware layer. For a general API, I'd use a Token Bucket because it is memory efficient and allows controlled bursts. Each client, such as a user ID or API key, would have a bucket with a configurable capacity and refill rate.
>
> Since we have multiple API servers, the rate-limit state should be stored in a shared low-latency store such as Redis. The check-and-update operation needs to be atomic to avoid race conditions when concurrent requests arrive.
>
> Requests within the limit are forwarded to the backend, while excessive requests receive HTTP 429. We can return rate-limit headers such as remaining quota and retry information.
>
> For scalability, we can run multiple rate limiter instances and use Redis clustering or sharding. For multi-region systems, we can place rate limiters close to users and consider eventual consistency where appropriate. Finally, we'd monitor 429 rates, latency, Redis health, and rule effectiveness."

---

# 33. Questions Interviewers May Ask

### Q1. Why not store counters in a database?

Because rate limiting requires very frequent reads/writes and low latency. An in-memory store such as Redis is generally more appropriate.

---

### Q2. Why Token Bucket?

Because it is:

```text
Simple
+
Memory efficient
+
Burst-friendly
```

---

### Q3. Token Bucket vs Leaky Bucket?

```text
Token Bucket → allows bursts

Leaky Bucket → smooths traffic
```

---

### Q4. Why is Fixed Window problematic?

Because requests can burst around the boundary of two windows.

---

### Q5. Why not store every timestamp?

You can with Sliding Window Log, but memory consumption becomes high at large scale.

---

### Q6. What happens if two servers update the same counter?

Race condition.

Use an atomic operation / Redis Lua script.

---

### Q7. Why Redis?

```text
Fast
In-memory
Atomic operations
Expiration support
Distributed/shared state
```

---

### Q8. What HTTP status code is returned?

```text
429 Too Many Requests
```

---

### Q9. What if Redis goes down?

Discuss:

```text
Fail-open
vs
Fail-closed
```

based on business requirements.

---

### Q10. Can rate limiting be based on IP?

Yes.

Other identifiers include:

```text
User ID
API Key
Device ID
Endpoint
Tenant
IP address
```

---

# 34. Final Mental Model 🧠

Remember this:

```text
             RATE LIMITER
                  │
        ┌─────────┴─────────┐
        │                   │
     ALGORITHM            STATE
        │                   │
   Token Bucket           Redis
   Leaky Bucket
   Fixed Window
   Sliding Log
   Sliding Counter
        │                   │
        └─────────┬─────────┘
                  │
             DECISION
             /       \
          ALLOW      REJECT
            │           │
            ▼           ▼
        API Server     429
```

And remember the **four most important interview topics**:

```text
1. Algorithm
      ↓
   Token Bucket

2. Distributed State
      ↓
   Redis

3. Concurrency
      ↓
   Atomic operations

4. Scalability & Failure
      ↓
   Redis cluster + fail-open/closed
```

---

# 35. One-Line Revision

> **Rate Limiter = Algorithm + Shared State + Atomicity + Scalability + Failure Handling**

For most system-design interviews:

```text
Token Bucket
     +
Redis
     +
Atomic update
     +
HTTP 429
     +
Distributed rate limiter
     +
Monitoring
```

is an excellent starting point.

---

## Source

ByteByteGo — **Design a Rate Limiter**

[Read the original ByteByteGo article](https://bytebytego.com/courses/system-design-interview/design-a-rate-limiter?utm_source=chatgpt.com)
