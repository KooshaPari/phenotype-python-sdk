# Codex Model Routing Policy - 2026-04-26

## Purpose

Prevent agentic scope creep and cost blowups while keeping work shippable.

The default operating model is **satisfy the task with the cheapest reliable
model and smallest complete patch**, then escalate only with evidence.

## Policy

### 0. Manager Role: Keep The Org DAG Alive

Codex in the Phenotype shelf is an org manager, not only a project-local
implementer.

When a task changes direction, do not abandon the previous lane. Preserve it as
an explicit WBS item with owner, state, and next validation command. If
subagents are available, leave a bounded read-only or implementation sidecar on
the previous lane while the manager handles the new coordination need.

Required queue behavior:

- Keep one active implementation lane.
- Keep one active governance/planning lane only when it directly improves the
  current or next implementation lane.
- Convert every interruption into either a merged patch, a blocked item with
  evidence, or a dated WBS entry.
- Close or hand off subagents explicitly; never let background work become
  invisible state.

### 0.1. Mandatory Size-Control Task

Every non-trivial lane must carry a size-control task in its existing WBS or
session notes. This is not a separate project; it is attached to the lane that
created the risk.

Use this shape:

```text
SIZE-NNN: Keep <lane> finishable
- Cap: <max PR/files/services/repos for this lane>
- Current size: <files touched, repos touched, open PRs>
- Stop rule: <validation or merge event that ends the lane>
- Spillover: <next WBS item instead of expanding this patch>
```

Examples:

- A dependency-remediation lane gets `SIZE-DEP`: one ecosystem per PR unless
  alerts share the same lockfile.
- A recovery lane gets `SIZE-RECOVERY`: cherry-pick reviewed value only; no
  wholesale branch promotion.
- An MVP lane gets `SIZE-MVP`: ship the narrow production-shaped loop; defer
  platformization to an explicit later WBS item.

### 1. Default to Low/Medium Effort

Use low or medium reasoning for most implementation, validation, PR triage,
documentation, dependency bumps, and targeted refactors.

Escalate to high/xhigh only when at least one of these is true:

- The task has unresolved architecture ambiguity after reading specs/code/tests.
- The change spans multiple repos with non-obvious ownership conflicts.
- Security, data-loss, auth, cryptography, or production migration risk is
  material.
- A cheaper model has already failed with a specific, reproducible drift or
  correctness issue.
- The user explicitly requests a frontier/high-reasoning pass.

### 2. Prefer Spark/Small Sidecars For Bounded Work

When subagents are requested or useful, use the cheapest capable sidecar first:

1. Spark-style subagents for read-only audits, inventory, PR triage, and
   narrow implementation slices.
2. `gpt-5.4-mini` low/medium for routine coding and integration after a good
   plan exists.
3. `gpt-5.4` medium/high for codebase-spanning implementation where mini drift
   is likely.
4. `gpt-5.5` only for hard synthesis, ambiguous architecture, high-stakes
   review, or recovery work where a wrong decision is expensive.

Do not spawn high-reasoning agents by habit. Make each subagent task bounded,
read-only unless it owns a disjoint write set, and close agents at turn end.

### 3. Reuse Existing High-Quality Plans

If a prior strong model pass, Kimi/Minimax plan, Claude Code plan, Forge/Droid
analysis, or human-authored governance doc already resolves the architecture,
then execution should usually run on cheaper models.

Treat those plans as inputs, not authority:

- Verify current repo state before editing.
- Keep only actionable, still-current steps.
- Drop scope expansions that are not necessary for the current acceptance
  criteria.
- Convert broad plans into small PR-sized batches before implementation.

### 4. Define Satisfiability Before Starting

Every non-trivial task needs a local satisfiability target:

- **Done means:** exact files/PRs/checks that prove completion.
- **Not included:** adjacent ideas that can become later tickets.
- **Validation:** the smallest command set that exercises the changed surface.
- **Stop rule:** after the target is met, stop or move to the next queued item;
  do not turn the task into a platform rewrite.

If an MVP is requested, implement a **strong MVP**:

- Production-shaped, testable, and documented enough to survive handoff.
- No placeholder architecture or fake integrations.
- No opportunistic multi-system expansion unless required by the acceptance
  criteria.

### 5. Escalation Ladder

Use this ladder before spending frontier reasoning:

1. Search the repo and canonical governance docs.
2. Ask a cheap read-only sidecar for specific missing facts.
3. Run targeted validation to prove the suspected failure.
4. Use a stronger model only for the unresolved decision.
5. Return to cheaper execution once the decision is made.

### 6. Anti-Creep Guardrails

Avoid the failure mode where a small project becomes unfinishable:

- Prefer one small merged PR over one perfect mega-branch.
- Do not mix governance, dependency, runtime, and feature work in one PR.
- Do not add new services, frameworks, or shared abstractions unless reuse is
  already proven by at least two consumers.
- Do not rescue stale branches wholesale; cherry-pick reviewed value.
- Archive/generated dependency snapshots are not application dependency
  manifests; quarantine or remove their manifest files instead of chasing
  fake app upgrades.

## Current OpenAI Reference Points

OpenAI docs currently describe `gpt-5.5` as the frontier model for complex
reasoning/coding and recommend smaller variants such as `gpt-5.4-mini` or
`gpt-5.4-nano` when optimizing for latency and cost. Codex-specific docs also
state that Codex can use any model available in the Responses API, and the
Codex rate card notes that credit usage varies by task size, model choice, and
reasoning requirements.

Because model availability and pricing change, agents must verify current
model/rate details from official OpenAI docs before making a durable cost
claim.

## Operational Defaults

For this org:

- **Default manager model:** medium reasoning, unless the user asks otherwise.
- **Default worker/subagent:** Spark-style or mini low/medium.
- **Default PR shape:** one concern, one repo, one validation surface.
- **Default answer when scope expands:** write a WBS item, do not silently grow
  the current patch.
- **Default after a high-quality research pass:** execute with cheaper models.
- **Default org-manager behavior:** keep the prior implementation lane visible
  while adding governance updates; do not switch scope fully unless the previous
  lane is merged, blocked with evidence, or delegated.

## Review Cadence

Refresh this policy when:

- Codex exposes new model routing controls.
- OpenAI updates Codex rate cards or default model behavior.
- A postmortem shows model under-selection caused bad code.
- A postmortem shows over-selection caused slow/costly overbuilding.
