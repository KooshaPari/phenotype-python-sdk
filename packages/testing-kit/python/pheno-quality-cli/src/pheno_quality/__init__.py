"""
Pheno Quality - Code Quality Analysis Framework

A comprehensive quality analysis framework for Python projects.
Extracted from phenoSDK and formalized as a standalone CLI tool.
"""

from pheno_quality.manager import quality_manager
from pheno_quality.config import get_config, list_configs, create_custom_config
from pheno_quality.core import (
    QualityIssue,
    QualityMetrics,
    QualityConfig,
    QualityReport,
    QualityAnalyzer,
    SeverityLevel,
    ImpactLevel,
)

__version__ = "1.0.0"
__all__ = [
    "quality_manager",
    "get_config",
    "list_configs",
    "create_custom_config",
    "QualityIssue",
    "QualityMetrics",
    "QualityConfig",
    "QualityReport",
    "QualityAnalyzer",
    "SeverityLevel",
    "ImpactLevel",
]
