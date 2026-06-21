"""Quickstart: scaffold llms.txt for a fresh repo.

Run: python examples/llms_txt/quickstart.py
"""

from __future__ import annotations

from pathlib import Path

from phenotype_py_extras.llms_txt import init_llms, render


def main() -> None:
    # 1. Scaffold a starter config + llms.txt in ./demo_repo/
    target = Path(__file__).parent / "demo_repo"
    result = init_llms(
        target,
        repo_name="phenotype-py-extras-demo",
        tagline="Demonstrates llms_txt generation.",
    )
    print("Scaffolded:", result)

    # 2. Re-render in-memory (no disk write)
    from phenotype_py_extras.llms_txt.config import LlmConfig

    cfg = LlmConfig(
        repo_name="phenotype-py-extras-demo",
        tagline="Demonstrates llms_txt generation.",
        install="pip install phenotype-py-extras",
        usage="from phenotype_py_extras.llms_txt import LlmConfig",
        public_api="render, write_llms_txt, init_llms",
    )
    print("--- llms.txt ---")
    print(render(cfg))


if __name__ == "__main__":
    main()