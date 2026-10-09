# Governed Agent Improvement Loop

A reference process for improving an agent **without letting it silently rewrite its own production behavior**.

## Pipeline

```text
ingest event
  → run agent with versioned prompt + tools
  → record redacted trace + outcome
  → evaluate correctness, safety, task success, and cost
  → categorize failure
  → generate candidate memory / prompt / SOP change
  → run offline benchmark + adversarial regression suite
  → request human approval for consequential changes
  → deploy canary version
  → compare metrics and roll back on regression
```

## Evaluation dimensions

| Dimension | Example measure |
|---|---|
| Task success | Correct resolution / verified completion |
| Grounding | Claims supported by authorized source data |
| Tool correctness | Correct tool, arguments, permissions, idempotency |
| Memory quality | Precision@k, staleness, contradictions |
| Safety | Privacy leakage, unauthorized action, policy deviation |
| Operations | p95 latency, retry rate, cost per completed task |

## Release contract

Each proposed change should include:
- immutable candidate ID and source trace IDs
- old/new prompt or SOP diff
- reason and evidence, with uncertainty
- test dataset version and baseline comparison
- reviewer, decision, and approval timestamp
- canary cohort, rollback trigger, and rollback artifact

## Failure modes to test

- Prompt injection in memory and tool responses
- Cross-tenant memory leakage
- Incorrect identity or account linking
- Duplicate webhook delivery and replay
- Out-of-order events and partial tool failures
- Model-generated false facts promoted as durable memory
- Evaluation-set overfitting and reward hacking

**Key distinction:** storing a correction is not retraining a model. A memory update changes retrieved context; an SOP update changes rules; a prompt release changes instructions; fine-tuning changes model weights. Measure each separately.
