"""
Tests for Pheno Quality CLI.
"""

import pytest
from pathlib import Path
from pheno_quality.core import (
    QualityIssue,
    QualityMetrics,
    QualityConfig,
    QualityReport,
    SeverityLevel,
    ImpactLevel,
)
from pheno_quality.manager import QualityAnalysisManager
from pheno_quality.config import get_config, list_configs, create_custom_config


class TestCoreClasses:
    """Test core quality analysis classes."""

    def test_quality_issue_creation(self):
        """Test creating a QualityIssue."""
        issue = QualityIssue(
            id="test-123",
            type="test_type",
            severity=SeverityLevel.HIGH,
            file="test.py",
            line=10,
            column=5,
            message="Test message",
            suggestion="Test suggestion",
            confidence=0.8,
            impact=ImpactLevel.HIGH,
            tool="test_tool",
        )
        assert issue.id == "test-123"
        assert issue.severity == SeverityLevel.HIGH
        assert issue.to_dict()["severity"] == "high"

    def test_quality_metrics_creation(self):
        """Test creating QualityMetrics."""
        metrics = QualityMetrics(
            total_issues=10,
            quality_score=85.0,
            files_affected=5,
        )
        assert metrics.total_issues == 10
        assert metrics.quality_score == 85.0

    def test_quality_config_creation(self):
        """Test creating QualityConfig."""
        config = QualityConfig(
            enabled_tools=["tool1", "tool2"],
            output_format="json",
        )
        assert config.enabled_tools == ["tool1", "tool2"]
        assert config.output_format == "json"

    def test_quality_config_serialization(self):
        """Test QualityConfig serialization."""
        config = QualityConfig(
            enabled_tools=["tool1"],
            thresholds={"max_issues": 100},
        )
        config_dict = config.to_dict()
        assert config_dict["enabled_tools"] == ["tool1"]

        # Test deserialization
        config2 = QualityConfig.from_dict(config_dict)
        assert config2.enabled_tools == ["tool1"]

    def test_quality_report_creation(self):
        """Test creating a QualityReport."""
        report = QualityReport(project_name="test_project")
        assert report.project_name == "test_project"
        assert len(report.issues) == 0

    def test_quality_report_add_issue(self):
        """Test adding issues to a report."""
        report = QualityReport()
        issue = QualityIssue(
            id="test-1",
            type="test",
            severity=SeverityLevel.LOW,
            file="test.py",
            line=1,
            column=0,
            message="Test",
            suggestion="Fix it",
            confidence=0.5,
            impact=ImpactLevel.LOW,
            tool="test",
        )
        report.add_issue(issue)
        assert len(report.issues) == 1

    def test_quality_report_finalize(self):
        """Test finalizing a report."""
        report = QualityReport()
        issue = QualityIssue(
            id="test-1",
            type="test",
            severity=SeverityLevel.HIGH,
            file="test.py",
            line=1,
            column=0,
            message="Test",
            suggestion="Fix it",
            confidence=0.9,
            impact=ImpactLevel.HIGH,
            tool="test",
        )
        report.add_issue(issue)
        report.finalize()

        assert report.metrics.total_issues == 1
        assert report.metrics.quality_score == 95.0  # 100 - 5 for HIGH


class TestConfiguration:
    """Test configuration functionality."""

    def test_list_configs(self):
        """Test listing available configs."""
        configs = list_configs()
        assert "default" in configs
        assert "pheno-sdk" in configs
        assert "strict" in configs
        assert "lenient" in configs

    def test_get_config(self):
        """Test getting a config."""
        config = get_config("default")
        assert isinstance(config, QualityConfig)

        strict_config = get_config("strict")
        assert strict_config.thresholds.get("quality_score_threshold", 0) >= 90

    def test_create_custom_config(self):
        """Test creating custom config."""
        base = get_config("default")
        custom = create_custom_config("default", max_workers=8)
        assert custom.max_workers == 8


class TestManager:
    """Test QualityAnalysisManager."""

    def test_manager_creation(self):
        """Test creating a manager."""
        manager = QualityAnalysisManager()
        assert manager is not None
        assert "json" in manager.exporters

    def test_get_available_tools(self):
        """Test getting available tools."""
        manager = QualityAnalysisManager()
        tools = manager.get_available_tools()
        assert isinstance(tools, list)
        # Should have tools registered
        assert len(tools) > 0

    def test_get_supported_formats(self):
        """Test getting supported formats."""
        manager = QualityAnalysisManager()
        formats = manager.get_supported_formats()
        assert "json" in formats
        assert "html" in formats
        assert "csv" in formats


class TestCLI:
    """Test CLI functionality."""

    def test_cli_import(self):
        """Test CLI module imports."""
        from pheno_quality.cli import app

        assert app is not None

    def test_cli_main_import(self):
        """Test main CLI imports."""
        from pheno_quality.cli.main import (
            quality_check,
            quality_report,
            quality_export,
            quality_import,
        )

        assert callable(quality_check)
        assert callable(quality_report)
        assert callable(quality_export)
        assert callable(quality_import)


class TestExporters:
    """Test exporter functionality."""

    def test_json_exporter(self):
        """Test JSON exporter."""
        from pheno_quality.exporters import JSONExporter

        exporter = JSONExporter()
        assert exporter.get_file_extension() == ".json"

    def test_html_exporter(self):
        """Test HTML exporter."""
        from pheno_quality.exporters import HTMLExporter

        exporter = HTMLExporter()
        assert exporter.get_file_extension() == ".html"

    def test_csv_exporter(self):
        """Test CSV exporter."""
        from pheno_quality.exporters import CSVExporter

        exporter = CSVExporter()
        assert exporter.get_file_extension() == ".csv"


class TestImporters:
    """Test importer functionality."""

    def test_json_importer(self):
        """Test JSON importer."""
        from pheno_quality.importers import JSONImporter

        importer = JSONImporter()
        assert importer.can_import("test.json")
        assert not importer.can_import("test.csv")

    def test_csv_importer(self):
        """Test CSV importer."""
        from pheno_quality.importers import CSVImporter

        importer = CSVImporter()
        assert importer.can_import("test.csv")
        assert not importer.can_import("test.json")

    def test_xml_importer(self):
        """Test XML importer."""
        from pheno_quality.importers import XMLImporter

        importer = XMLImporter()
        assert importer.can_import("test.xml")
        assert not importer.can_import("test.json")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
