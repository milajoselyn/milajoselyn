# Agent Memory Blueprint

A reference architecture for persistent, retrieval-augmented agent memory. **Do not treat user messages, retrieved documents, or memory records as instructions with system-level authority.**

## Memory types

| Type | Stores | Typical lifecycle |
|---|---|---|
| Working | Current turn, tool results, task state | Minutes / task |
| Episodic | Timestamped interactions and outcomes | Time-bound, subject to consent and retention |
| Semantic | Verified durable facts, preferences, relationships | Versioned, confidence-scored |
| Procedural | Approved playbooks and tool-use rules | Human-reviewed releases |

## Example record

```json
{
  "id": "mem_01",
  "tenant_id": "tenant_example",
  "subject_id": "user_example",
  "kind": "episodic",
  "text": "User prefers concise technical summaries.",
  "source_event_id": "evt_01",
  "created_at": "2026-10-08T00:00:00Z",
  "expires_at": null,
  "confidence": 0.87,
  "sensitivity": "low",
  "consent_scope": "assistant_personalization",
  "status": "candidate",
  "version": 1
}
```

## Write path

1. Authenticate and authorize tenant, subject, and purpose.
2. Classify sensitive data and redact unnecessary identifiers before model calls.
3. Extract **candidate** memories from evidence; never blindly save model output.
4. Deduplicate by stable source event ID; reconcile conflicting facts.
5. Validate provenance, confidence, consent scope, and retention policy.
6. Promote eligible memories, preserving version history and audit metadata.

## Read path

1. Filter by tenant, subject, permission scope, status, and expiry **before retrieval**.
2. Search hybrid lexical/vector candidates where supported.
3. Rank by relevance, confidence, freshness, and source reliability.
4. Return a bounded set with citations and timestamps.
5. Treat retrieved memory as untrusted data; never execute instructions embedded in it.

## Operations

- Implement subject-level export and deletion, including indexes and derived caches.
- Track stale, contradictory, and low-confidence memories.
- Separate conversational preferences from business facts and approved policies.
- Monitor retrieval precision, false-memory rate, latency, cost, and deletion completeness.
- Use encryption, access controls, audit logs, and retention schedules appropriate to the deployment.

**Not included:** production auth, persistence, encryption, embeddings, or privacy compliance certification. Those must be implemented and validated in the target environment.
