"""Minimal memory ranking example. Standard library only; not a vector database.

Run: python examples/memory_ranker.py
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from math import exp
import re

@dataclass(frozen=True)
class Memory:
    id: str
    tenant_id: str
    subject_id: str
    text: str
    confidence: float
    created_at: datetime
    approved: bool = True

def tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))

def rank_memories(query: str, memories: list[Memory], *,
                  tenant_id: str, subject_id: str,
                  now: datetime, limit: int = 3) -> list[tuple[Memory, float]]:
    """Enforce scope before scoring; rank with lexical overlap + confidence + decay."""
    q = tokens(query)
    if not q or limit <= 0:
        return []
    results = []
    for m in memories:
        if m.tenant_id != tenant_id or m.subject_id != subject_id or not m.approved:
            continue
        overlap = len(q & tokens(m.text)) / len(q)
        if overlap == 0:
            continue
        age_days = max(0.0, (now - m.created_at).total_seconds() / 86400)
        freshness = exp(-age_days / 90)
        confidence = min(1.0, max(0.0, m.confidence))
        score = 0.65 * overlap + 0.25 * confidence + 0.10 * freshness
        results.append((m, round(score, 4)))
    return sorted(results, key=lambda item: (-item[1], item[0].id))[:limit]

if __name__ == "__main__":
    now = datetime.now(timezone.utc)
    items = [
        Memory("m1", "demo", "alice", "Prefers technical summaries with citations", .9, now),
        Memory("m2", "demo", "bob", "Prefers technical summaries with citations", 1, now),
        Memory("m3", "demo", "alice", "Likes concise release notes", .8, now),
    ]
    found = rank_memories("technical summaries", items, tenant_id="demo",
                          subject_id="alice", now=now)
    assert [m.id for m, _ in found] == ["m1"], "scope/ranking regression"
    for memory, score in found:
        print(f"{memory.id}: {score:.4f} | {memory.text}")
