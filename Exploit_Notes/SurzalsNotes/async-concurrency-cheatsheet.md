# Async and Concurrency Cheatsheet

## 1. Quick Definitions

| Term | Meaning | Best Use |
| --- | --- | --- |
| Concurrency | Multiple tasks make progress during the same time window. | Handling lots of waiting tasks. |
| Parallelism | Multiple tasks run at the exact same time on different cores. | CPU-heavy workloads. |
| Async | A task yields control instead of blocking while it waits. | Network, disk, timers, APIs. |
| Threading | Multiple execution paths in one process. | Mixed I/O work, legacy APIs. |
| Multiprocessing | Multiple OS processes. | CPU-bound work, isolation. |

## 2. Fast Decision Guide

| Situation | Use |
| --- | --- |
| Many sockets, HTTP calls, timers, DB requests | Async/event loop |
| CPU-heavy parsing, hashing, image work, compression | Processes or true parallel workers |
| Blocking library you cannot replace | Threads or run-in-executor |
| Need strict ordering and simple code | Synchronous flow |
| Shared mutable state is getting messy | Message passing / queues |

## 3. Golden Rules

1. Do not block the event loop.
2. Prefer message passing over shared mutable state.
3. Bound concurrency; do not spawn unbounded work.
4. Always set timeouts on I/O.
5. Treat cancellation as a normal path.
6. Protect critical sections with locks only when you must.
7. Keep critical sections small.
8. Design for backpressure, not infinite buffering.
9. Make retries explicit and idempotent.
10. Measure before assuming concurrency made it faster.

## 4. Core Mental Model

**Ask first:** is the task waiting on something, or burning CPU?

- Mostly waiting -> async helps.
- Mostly CPU -> async alone does not help much.
- Mixed -> async for orchestration, threads/processes for the heavy parts.

## 5. Safe Design Patterns

### Fan-out / fan-in

Run several independent tasks, then gather results.

```text
input -> spawn N tasks -> wait for all -> combine results
```

### Worker pool

Limit work with a fixed number of workers.

```text
producer -> queue -> N workers -> results
```

### Pipeline

Break work into stages with queues between them.

```text
fetch -> parse -> enrich -> store
```

### Actor / ownership model

Each worker owns its state and communicates by messages.

```text
send message -> worker mutates its own state -> replies
```

## 6. Shared State Rules

### Prefer

- Immutable data
- Queues/channels
- Copying small values
- One owner per resource

### Avoid

- Global mutable state
- Nested locks
- Holding locks across I/O
- Reading and writing the same structure from many threads without protection

## 7. Common Failure Modes

| Problem | Usually Caused By | Fix |
| --- | --- | --- |
| Race condition | Unsynchronized shared state | Lock, channel, single owner |
| Deadlock | Circular lock waits | Lock ordering, fewer locks, timeouts |
| Starvation | One task never gets scheduled/resources | Fair queues, smaller critical sections |
| Livelock | Tasks keep reacting but never finish | Add coordination / backoff |
| Event-loop freeze | Blocking call inside async code | Offload blocking work |
| Memory blow-up | Unbounded queue / task creation | Bounded queue, semaphore |
| Thundering herd | Too many retries or wakeups | Jitter, backoff, limits |

## 8. Backpressure Checklist

- Use bounded queues.
- Use semaphores or worker limits.
- Drop, batch, or defer low-priority work.
- Fail fast when overloaded.
- Expose queue depth and latency in logs/metrics.

## 9. Cancellation and Timeouts

Every concurrent system should answer:

- How does work stop?
- What happens to in-flight tasks?
- What gets retried?
- What is the timeout at each layer?

### Good defaults

- Add request timeout.
- Add overall operation timeout.
- Propagate cancellation downward.
- Clean up resources in `finally`/defer blocks.

## 10. Retry Rules

Retry only when the operation is:

- transiently failing
- idempotent, or safely deduplicated

Use:

- exponential backoff
- jitter
- max retry count
- circuit breaking when a dependency is sick

## 11. Async Code Smells

- `async` function doing heavy CPU work
- `await` inside a loop when batching is possible
- fire-and-forget tasks with no tracking
- no timeout on network calls
- huge `gather`/`Promise.all` over thousands of items
- lock held while awaiting or doing I/O
- swallowing cancellation exceptions

## 12. Python Cheatsheet

### Good

```python
import asyncio

sem = asyncio.Semaphore(20)

async def fetch_one(client, url):
    async with sem:
        return await client.get(url, timeout=10)

async def main(client, urls):
    tasks = [fetch_one(client, url) for url in urls]
    return await asyncio.gather(*tasks)
```

### Do not do this

```python
async def bad():
    data = slow_cpu_work()   # blocks the event loop
    return data
```

### Offload blocking work

```python
async def better():
    return await asyncio.to_thread(blocking_call)
```

### Python rules

- Use `asyncio` for I/O concurrency.
- Use `asyncio.Semaphore` to cap concurrency.
- Use `asyncio.Queue` for pipelines.
- Use `asyncio.to_thread()` for blocking calls.
- Use processes for real CPU-bound work.

## 13. JavaScript Cheatsheet

### Good

```js
const limit = 10;

async function mapWithLimit(items, fn) {
  const results = [];
  let i = 0;

  async function worker() {
    while (i < items.length) {
      const index = i++;
      results[index] = await fn(items[index]);
    }
  }

  await Promise.all(Array.from({ length: limit }, worker));
  return results;
}
```

### JS rules

- `Promise.all()` is great, but only for bounded batches.
- Use `AbortController` for cancellation.
- Do not mix CPU-heavy loops with latency-sensitive event-loop work.
- Worker threads are for CPU-heavy work, not normal async I/O.

## 14. Go Cheatsheet

### Good

```go
sem := make(chan struct{}, 20)

for _, item := range items {
    sem <- struct{}{}
    go func(item Item) {
        defer func() { <-sem }()
        process(item)
    }(item)
}
```

### Go rules

- Goroutines are cheap, but not free.
- Always think about cancellation with `context.Context`.
- Channels are great for ownership transfer and coordination.
- Use worker pools for high-cardinality workloads.

## 15. Locking Rules

1. Lock the smallest thing possible.
2. Hold locks for the shortest time possible.
3. Never await, sleep, or do network I/O while holding a lock.
4. If multiple locks are needed, acquire them in one global order.
5. Prefer read/write locks only when reads massively dominate and profiling proves it helps.

## 16. Practical Performance Rules

- Bigger batches reduce overhead, but increase latency.
- Too much concurrency causes contention and worse throughput.
- Concurrency level should usually be tuned, not guessed.
- Measure p50, p95, p99 latency and queue depth.
- Watch context switching, lock contention, memory growth, and retries.

## 17. Debugging Checklist

When concurrent code misbehaves, check:

1. Is something blocking the event loop?
2. Is shared state protected?
3. Is concurrency bounded?
4. Are tasks leaking or never awaited/joined?
5. Are timeouts and cancellation wired through?
6. Are retries amplifying load?
7. Are locks acquired in a consistent order?

## 18. Rule of Thumb Summary

| If you have... | Reach for... |
| --- | --- |
| Many waiting operations | Async |
| Heavy CPU work | Processes / parallel workers |
| Blocking legacy library | Threads |
| Complex shared state | Queue/channel/actor design |
| Load spikes | Bounded concurrency + backpressure |
| Fragile dependencies | Timeouts + retries + jitter + cancellation |

## 19. One-Line Heuristic

**Use async for waiting, threads for unavoidable blocking, processes for CPU, and queues/channels to keep state sane.**
