"""Pheno Analysis CLI - Unified code analysis suite."""

__version__ = "1.0.0"
__author__ = "Phenotype"
__description__ = "Comprehensive code analysis tools for Python projects"

# Expose main modules
from pheno_analysis_cli import (
    analyze_complexity,
    analyze_churn,
    analyze_duplication,
    analyze_dependencies,
    coverage_analysis,
    analyze_test_coverage,
    analyze_quality_coverage,
    analyze_response_times,
    code_smell_detector,
    advanced_pattern_detector,
    architectural_pattern_validator,
    detect_dead_code,
)

__all__ = [
    "analyze_complexity",
    "analyze_churn",
    "analyze_duplication",
    "analyze_dependencies",
    "coverage_analysis",
    "analyze_test_coverage",
    "analyze_quality_coverage",
    "analyze_response_times",
    "code_smell_detector",
    "advanced_pattern_detector",
    "architectural_pattern_validator",
    "detect_dead_code",
]
