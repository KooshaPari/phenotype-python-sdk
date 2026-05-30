#!/usr/bin/env python3
"""Allow running as module: python -m pheno_testing_cli"""

from .cli import main
import sys

if __name__ == "__main__":
    sys.exit(main())
