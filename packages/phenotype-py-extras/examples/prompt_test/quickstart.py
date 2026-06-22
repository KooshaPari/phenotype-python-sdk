"""Quickstart: prompt_test assertions + pytest plugin.

Run directly: python examples/prompt_test/quickstart.py
"""

from __future__ import annotations

from phenotype_py_extras.prompt_test import (
    assert_prompt_contains,
    assert_prompt_json,
    assert_prompt_match,
)


def main() -> None:
    # 1. Exact-match assertion
    assert_prompt_match("Hello, world!", "Hello, world!")
    print("assert_prompt_match: OK")

    # 2. Substring assertion (case-insensitive)
    assert_prompt_contains("The quick brown fox", "QUICK", ignore_case=True)
    print("assert_prompt_contains: OK")

    # 3. Regex assertion
    assert_prompt_contains("order-12345 here", r"order-\d+", as_regex=True)
    print("assert_prompt_contains (regex): OK")

    # 4. JSON-shape assertion
    assert_prompt_json('{"a": 1, "b": "x"}', {"a": 1, "b": "x"})
    print("assert_prompt_json: OK")

    print("\nAll prompt_test assertions pass.")


if __name__ == "__main__":
    main()