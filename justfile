# justfile for phenotype-python-sdk
# Standard recipes for the Hygiene bundle (2026-06-08).
# https://github.com/casey/just

set dotenv-load := true
set shell := ["bash", "-uc"]
set positional-arguments := true

# Default: list available recipes.
_default:
	@just --list

# Install all workspace packages (per-kit tool).
install:
	uv sync

# Run lint across the workspace.
lint:
	uv run ruff check .
	uv run ruff format --check .

# Auto-format the workspace.
format:
	uv run ruff format .
	uv run ruff check --fix .

# Run the test suite.
test:
	uv run pytest

# Type-check.
typecheck:
	uv run mypy .

# Build dist artifacts.
build:
	uv build

# Clean caches and build artifacts.
clean:
	rm -rf .pytest_cache .mypy_cache dist build *.egg-info
	find . -type d -name __pycache__ -prune -exec rm -rf {} +

# CI target: lint + typecheck + test.
ci: lint typecheck test
