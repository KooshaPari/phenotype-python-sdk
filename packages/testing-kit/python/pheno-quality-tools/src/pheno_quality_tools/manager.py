"""
Standalone Quality Manager - Unified entry point for quality analysis tooling.
"""

from pathlib import Path
from typing import Any

from .core import QualityConfig, QualityReport
from .pattern_detector import PatternDetector
from .architectural_validator import ArchitecturalValidator
from .performance_detector import PerformanceDetector
from .security_scanner import SecurityScanner
from .code_smell_detector import CodeSmellDetector
from .integration_gates import IntegrationGates
from .atlas_health import AtlasHealthAnalyzer
from .registry import tool_registry
from .exporters import (
    JSONExporter,
    HTMLExporter,
    MarkdownExporter,
    CSVExporter,
    XMLExporter,
)


class QualityManager:
    """
    Unified manager for quality analysis operations.
    """

    def __init__(self, config: QualityConfig | None = None):
        self.config = config or QualityConfig()
        self._register_builtin_tools()

    def _register_builtin_tools(self):
        """Register all built-in quality analysis tools."""
        tools = [
            ("pattern_detector", PatternDetector),
            ("architectural_validator", ArchitecturalValidator),
            ("performance_detector", PerformanceDetector),
            ("security_scanner", SecurityScanner),
            ("code_smell_detector", CodeSmellDetector),
            ("integration_gates", IntegrationGates),
            ("atlas_health", AtlasHealthAnalyzer),
        ]
        for name, tool_class in tools:
            tool_registry.register_tool(name, tool_class)

    def analyze_project(
        self,
        project_path: str | Path,
        enabled_tools: list[str] | None = None,
        output_path: str | Path | None = None,
    ) -> QualityReport:
        """
        Analyze a project with enabled tools.

        Args:
            project_path: Path to the project directory
            enabled_tools: List of tool names to run (defaults to config.enabled_tools)
            output_path: Optional path to save the report

        Returns:
            QualityReport with all findings
        """
        project_path = Path(project_path)
        tools = (
            enabled_tools
            or self.config.enabled_tools
            or [
                "pattern_detector",
                "code_smell_detector",
            ]
        )

        report = QualityReport(project_name=project_path.name, config=self.config)

        for tool_name in tools:
            tool = tool_registry.create_tool(tool_name, self.config)
            if tool:
                issues = tool.analyze_directory(project_path)
                report.add_issues(issues)

        report.finalize()

        if output_path:
            self.export_report(report, output_path)

        return report

    def analyze_file(
        self,
        file_path: str | Path,
        enabled_tools: list[str] | None = None,
    ) -> QualityReport:
        """
        Analyze a single file with enabled tools.

        Args:
            file_path: Path to the file to analyze
            enabled_tools: List of tool names to run

        Returns:
            QualityReport with findings
        """
        file_path = Path(file_path)
        tools = enabled_tools or self.config.enabled_tools or ["pattern_detector"]

        report = QualityReport(project_name=file_path.name, config=self.config)

        for tool_name in tools:
            tool = tool_registry.create_tool(tool_name, self.config)
            if tool:
                issues = tool.analyze_file(file_path)
                report.add_issues(issues)

        report.finalize()
        return report

    def export_report(
        self,
        report: QualityReport,
        output_path: str | Path,
        format: str | None = None,
    ) -> bool:
        """
        Export a quality report to file.

        Args:
            report: The QualityReport to export
            output_path: Path for the output file
            format: Optional format override (json, html, md, csv, xml)

        Returns:
            True if export succeeded
        """
        output_path = Path(output_path)
        fmt = format or output_path.suffix.lstrip(".") or "json"

        exporters = {
            "json": JSONExporter(),
            "html": HTMLExporter(),
            "md": MarkdownExporter(),
            "markdown": MarkdownExporter(),
            "csv": CSVExporter(),
            "xml": XMLExporter(),
        }

        exporter = exporters.get(fmt)
        if not exporter:
            raise ValueError(f"Unsupported export format: {fmt}")

        return exporter.export(report, output_path)

    def generate_summary(self, report: QualityReport) -> dict[str, Any]:
        """
        Generate a summary from a quality report.

        Args:
            report: The QualityReport to summarize

        Returns:
            Dictionary with summary information
        """
        metrics = report.metrics

        # Determine quality status
        if metrics.quality_score >= 90:
            status = "excellent"
        elif metrics.quality_score >= 80:
            status = "good"
        elif metrics.quality_score >= 70:
            status = "acceptable"
        elif metrics.quality_score >= 60:
            status = "needs_improvement"
        else:
            status = "poor"

        # Generate recommendations
        recommendations = []
        if metrics.issues_by_severity.get("critical", 0) > 0:
            recommendations.append("Address critical issues immediately")
        if metrics.issues_by_severity.get("high", 0) > 10:
            recommendations.append("High severity issues need attention")
        if metrics.quality_score < 70:
            recommendations.append("Overall quality score needs improvement")
        if not recommendations:
            recommendations.append("Maintain current quality standards")

        return {
            "project_name": report.project_name,
            "quality_score": metrics.quality_score,
            "quality_status": status,
            "total_issues": metrics.total_issues,
            "files_affected": metrics.files_affected,
            "analysis_duration": metrics.analysis_duration,
            "issues_by_severity": metrics.issues_by_severity,
            "issues_by_type": metrics.issues_by_type,
            "issues_by_tool": metrics.issues_by_tool,
            "recommendations": recommendations,
        }

    def list_tools(self) -> list[str]:
        """List all available quality analysis tools."""
        return tool_registry.list_tools()

    def get_tool_info(self, tool_name: str) -> dict[str, Any] | None:
        """Get information about a specific tool."""
        return tool_registry.get_tool_info(tool_name)


# Global quality manager instance
quality_manager = QualityManager()

__all__ = ["QualityManager", "quality_manager"]
