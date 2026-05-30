"""
Pheno Quality Tools - Comprehensive Quality Analysis Framework

A standalone quality analysis framework for Python projects, extracted from phenoSDK.
Provides pattern detection, architectural validation, security scanning, code smell
detection, and integration quality gates.

Basic Usage:
    >>> from pheno_quality_tools import quality_manager
    >>> report = quality_manager.analyze_project("./src")
    >>> print(f"Quality Score: {report.metrics.quality_score:.1f}/100")

CLI Usage:
    $ pheno-quality-gates check .                      # Check current directory
    $ pheno-quality-gates validate --run-analysis      # Validate quality gates
    $ pheno-quality-gates atlas .                      # Atlas health check

Available Tools:
    - pattern_detector: Detect code patterns and anti-patterns
    - architectural_validator: Validate architectural patterns
    - performance_detector: Detect performance issues
    - security_scanner: Scan for security vulnerabilities
    - code_smell_detector: Detect code smells
    - integration_gates: Validate integration quality
    - atlas_health: Analyze project health metrics
"""

__version__ = "1.0.0"
__author__ = "Phenotype Ecosystem"

# Core components
from .core import (
    QualityAnalyzer,
    QualityConfig,
    QualityIssue,
    QualityMetrics,
    QualityReport,
    SeverityLevel,
    ImpactLevel,
)

# Tools
from .pattern_detector import PatternDetector, PatternDetectorPlugin
from .architectural_validator import ArchitecturalValidator, ArchitecturalValidatorPlugin
from .performance_detector import PerformanceDetector, PerformanceDetectorPlugin
from .security_scanner import SecurityScanner, SecurityScannerPlugin
from .code_smell_detector import CodeSmellDetector, CodeSmellDetectorPlugin
from .integration_gates import IntegrationGates, IntegrationGatesPlugin
from .atlas_health import AtlasHealthAnalyzer, AtlasHealthPlugin

# Management
from .manager import QualityManager, quality_manager
from .registry import QualityToolRegistry, tool_registry
from .plugins import QualityPlugin, PluginRegistry, plugin_registry

# Configuration
from .config import (
    get_config,
    list_configs,
    create_custom_config,
    DEFAULT_CONFIG,
    STRICT_CONFIG,
    LENIENT_CONFIG,
)

# Import/Export
from .exporters import (
    QualityExporter,
    JSONExporter,
    HTMLExporter,
    MarkdownExporter,
    CSVExporter,
    XMLExporter,
)
from .importers import (
    QualityImporter,
    JSONImporter,
    CSVImporter,
    XMLImporter,
    QualityReportImporter,
)

# Utilities
from .utils import QualityUtils

# Integration
from .integration import QualityFrameworkIntegration, integrate_quality_framework

__all__ = [
    # Version
    "__version__",
    "__author__",
    # Core
    "QualityAnalyzer",
    "QualityConfig",
    "QualityIssue",
    "QualityMetrics",
    "QualityReport",
    "SeverityLevel",
    "ImpactLevel",
    # Tools
    "PatternDetector",
    "PatternDetectorPlugin",
    "ArchitecturalValidator",
    "ArchitecturalValidatorPlugin",
    "PerformanceDetector",
    "PerformanceDetectorPlugin",
    "SecurityScanner",
    "SecurityScannerPlugin",
    "CodeSmellDetector",
    "CodeSmellDetectorPlugin",
    "IntegrationGates",
    "IntegrationGatesPlugin",
    "AtlasHealthAnalyzer",
    "AtlasHealthPlugin",
    # Management
    "QualityManager",
    "quality_manager",
    "QualityToolRegistry",
    "tool_registry",
    "QualityPlugin",
    "PluginRegistry",
    "plugin_registry",
    # Configuration
    "get_config",
    "list_configs",
    "create_custom_config",
    "DEFAULT_CONFIG",
    "STRICT_CONFIG",
    "LENIENT_CONFIG",
    # Exporters
    "QualityExporter",
    "JSONExporter",
    "HTMLExporter",
    "MarkdownExporter",
    "CSVExporter",
    "XMLExporter",
    # Importers
    "QualityImporter",
    "JSONImporter",
    "CSVImporter",
    "XMLImporter",
    "QualityReportImporter",
    # Utilities
    "QualityUtils",
    # Integration
    "QualityFrameworkIntegration",
    "integrate_quality_framework",
]
