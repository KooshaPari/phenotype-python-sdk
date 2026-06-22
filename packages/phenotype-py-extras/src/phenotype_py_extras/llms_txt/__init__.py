"""llms_txt: Generate llms.txt files for repositories.

Absorbed from KooshaPari/pheno-llms-txt (L5-114, 2026-06-20).
Public API: LlmConfig, render, load_config, write_llms_txt, init_llms, cli_main
"""

from .config import LlmConfig, load_config
from .renderer import render, write_llms_txt
from .validator import validate_config, init_llms, ConfigError
from .cli import cli_main

__all__ = [
    "LlmConfig",
    "render",
    "load_config",
    "write_llms_txt",
    "validate_config",
    "init_llms",
    "ConfigError",
    "cli_main",
]