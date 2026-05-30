# CLAUDE.md — phenotype-python-sdk

## Overview

- **Repo**: `KooshaPari/phenotype-python-sdk` — consolidated Phenotype Python/polyglot kits.
- **Kits**: `mcp-kit`, `testing-kit`, `auth-kit`, `resilience-kit` under `packages/`.
- **Owner**: Phenotype org / KooshaPari.

## Layout

Edit only the kit (and language subtree) relevant to your task. Kits retain their own `.github/workflows` from absorption; root CI is a lightweight lint/smoke gate.

## Conventions

- Prefer existing per-kit Poetry/setuptools patterns; do not restructure without request.
- Additive changes only unless explicitly requested.
- Python 3.11+ unless a package pins otherwise.
