# Security — SOTA (phenotype-python-sdk)

## Threat model

| Threat | Impact | Likelihood |
|--------|--------|------------|
| Secrets committed via template placeholders | high | med |
| Agents pushing to wrong GitHub account / org | high | med |
| Domain code smuggled outside charter scope | med | med |
| Dependency confusion / typosquat | high | low |
| Duplicate PyPI package name injection | med | low |

## Requirements

| Requirement | Weight |
|-------------|--------|
| Secret scan on every PR | must |
| Branch protection on default branch | must |
| Charter-enforced scope for agent merges | must |
| SBOM or dependency audit for runtime deps | should (if shipping artifacts) |

## Controls (chosen)

- [review.md](../../../review.md) org blocklist (non-`KooshaPari/*` remotes, force-push, amend-without-request)
- `trufflehog` / secret scan in CI workflows
- Charter blocks out-of-scope crates or services without review
- `uv sync` + pytest for affected packages; secret scan via org workflows

## Alternatives considered

| Approach | Pros | Cons | Verdict |
|----------|------|------|---------|
| Per-repo ad-hoc policy | flexible | fleet drift; agent confusion | rejected |
| Centralized SOC2 platform only | audit trail | overkill for git-native OSS org | rejected |
| No agent merge policy | fast | unbounded scope/security risk | rejected |
| **Kilo Code Stand + template scanners** | consistent; agent-readable | requires doc maintenance | **chosen** |

## Chosen strategy

Security is **policy-as-docs**: agents read `review.md` before merge. Technical controls come from phenotype-tooling reusable workflows where adopted.

## Evolution triggers

- New org-wide blocklist rule → update REVIEW_SPEC + all `review.md`
- Critical CVE in pinned dependency → update this file + alternatives index
- Compliance requirement (e.g. FR-LIB-001) → link AgilePlus spec in charter
