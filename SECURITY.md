# Security Policy

## Supported Versions

Security updates are applied to the latest released version of each kit and to
the current `main` branch. Older versions receive fixes at the maintainers'
discretion.

## Reporting a Vulnerability

**Please do not open a public GitHub issue for security problems.**

Report privately via one of:

- GitHub Security Advisories: <https://github.com/KooshaPari/phenotype-python-sdk/security/advisories/new>
- Email: <security@kooshapari.com> (PGP key on request)

Include:

1. A clear description of the vulnerability and its impact.
2. A minimal reproducer (code, command, or configuration).
3. Affected versions / commits.
4. Any known mitigations.

We acknowledge new reports within 3 business days and aim to ship a fix or
mitigation within 30 days, coordinated with the reporter.

## Scope

This SDK ships authentication, transport, and resilience utilities. Vulnerabilities
in those surfaces (token handling, request signing, retry/backoff logic, dependency
loading) are in scope. Third-party dependencies should be reported upstream.
