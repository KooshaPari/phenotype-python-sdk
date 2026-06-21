"""Click-based CLI: pheno-llms-txt --config <yaml> --out <llms.txt>

Absorbed from KooshaPari/pheno-llms-txt/src/pheno_llms_txt/cli.py:1-23 (L5-114, 2026-06-20).
"""

from __future__ import annotations

import click

from .config import load_config
from .renderer import write_llms_txt


@click.command()
@click.option("--config", "config_path", default=None, help="Path to YAML config.")
@click.option("--out", "out_path", default="llms.txt", help="Output llms.txt path.")
def cli_main(config_path: str | None, out_path: str) -> None:
    """Render llms.txt from a YAML config (or defaults if absent)."""
    cfg = load_config(config_path)
    written = write_llms_txt(cfg, out_path)
    click.echo(f"wrote {written}")


if __name__ == "__main__":
    cli_main()
