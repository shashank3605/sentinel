# Sentinel — Latency Benchmarks

## Phase 0 — Baseline (stub scoring, no Redis/Kafka)

**Date:** 2026-09-04
**Setup:** Single-node, sequential requests, same machine as server (no network latency), stub rule-only scoring logic (amount threshold check only)
**Requests:** 100
**Command:** `python scripts/benchmark.py`

| Metric | Value   |
| ------ | ------- |
| Min    | 1.41 ms |
| p50    | 1.82 ms |
| p95    | 2.85 ms |
| p99    | 7.01 ms |
| Max    | 7.01 ms |
| Mean   | 1.93 ms |

**Notes:** This measures raw FastAPI + Pydantic validation overhead only — no Redis feature lookups, no Kafka, no real ML inference, no concurrent load. Establishes the floor latency before Phase 1 adds the streaming backbone and real scoring logic. Target remains <100ms p95 once those pieces are in the path.
