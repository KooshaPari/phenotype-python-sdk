"""
Quality analysis report importers.

Supports importing quality reports from various formats:
- JSON
- CSV
- XML
"""

import csv
import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from .core import ImpactLevel, QualityConfig, QualityIssue, QualityReport, SeverityLevel


class QualityImporter(ABC):
    """
    Abstract base class for quality report importers.
    """

    @abstractmethod
    def import_report(self, file_path: str | Path) -> QualityReport | None:
        """Import a quality report from file."""

    @abstractmethod
    def can_import(self, file_path: str | Path) -> bool:
        """Check if this importer can handle the file."""


class JSONImporter(QualityImporter):
    """Import quality reports from JSON format."""

    def import_report(self, file_path: str | Path) -> QualityReport | None:
        try:
            file_path = Path(file_path)
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)
            return self._parse_json_data(data)
        except Exception:
            return None

    def can_import(self, file_path: str | Path) -> bool:
        return Path(file_path).suffix.lower() == ".json"

    def _parse_json_data(self, data: dict[str, Any]) -> QualityReport:
        project_name = data.get("project_name", "")
        config_data = data.get("config", {})
        config = QualityConfig.from_dict(config_data) if config_data else QualityConfig()

        report = QualityReport(project_name, config)

        # Parse issues
        for issue_data in data.get("issues", []):
            issue = self._parse_issue(issue_data)
            if issue:
                report.add_issue(issue)

        # Parse tool reports
        for tool_name, tool_data in data.get("tool_reports", {}).items():
            report.add_tool_report(tool_name, tool_data)

        report.metadata = data.get("metadata", {})
        report.analysis_start_time = data.get("analysis_start_time", 0)
        report.analysis_end_time = data.get("analysis_end_time", 0)
        report.finalize()

        return report

    def _parse_issue(self, issue_data: dict[str, Any]) -> QualityIssue | None:
        try:
            return QualityIssue(
                id=issue_data.get("id", ""),
                type=issue_data.get("type", ""),
                severity=SeverityLevel(issue_data.get("severity", "low")),
                file=issue_data.get("file", ""),
                line=issue_data.get("line", 0),
                column=issue_data.get("column", 0),
                message=issue_data.get("message", ""),
                suggestion=issue_data.get("suggestion", ""),
                confidence=issue_data.get("confidence", 0.0),
                impact=ImpactLevel(issue_data.get("impact", "Low")),
                tool=issue_data.get("tool", ""),
                category=issue_data.get("category", ""),
                tags=issue_data.get("tags", []),
                metadata=issue_data.get("metadata", {}),
            )
        except (ValueError, KeyError):
            return None


class CSVImporter(QualityImporter):
    """Import quality reports from CSV format."""

    def import_report(self, file_path: str | Path) -> QualityReport | None:
        try:
            file_path = Path(file_path)
            report = QualityReport()

            with open(file_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    issue = self._parse_csv_row(row)
                    if issue:
                        report.add_issue(issue)

            report.finalize()
            return report
        except Exception:
            return None

    def can_import(self, file_path: str | Path) -> bool:
        return Path(file_path).suffix.lower() == ".csv"

    def _parse_csv_row(self, row: dict[str, str]) -> QualityIssue | None:
        try:
            return QualityIssue(
                id=row.get("ID", ""),
                type=row.get("Type", ""),
                severity=SeverityLevel(row.get("Severity", "low")),
                file=row.get("File", ""),
                line=int(row.get("Line", 0)),
                column=int(row.get("Column", 0)),
                message=row.get("Message", ""),
                suggestion=row.get("Suggestion", ""),
                confidence=float(row.get("Confidence", 0.0)),
                impact=ImpactLevel(row.get("Impact", "Low")),
                tool=row.get("Tool", ""),
                category=row.get("Category", ""),
            )
        except (ValueError, KeyError):
            return None


class XMLImporter(QualityImporter):
    """Import quality reports from XML format."""

    def import_report(self, file_path: str | Path) -> QualityReport | None:
        try:
            file_path = Path(file_path)
            tree = ET.parse(file_path)
            root = tree.getroot()

            report = QualityReport()
            report.project_name = root.get("project", "")

            issues = root.find("issues")
            if issues is not None:
                for issue_elem in issues.findall("issue"):
                    issue = self._parse_xml_issue(issue_elem)
                    if issue:
                        report.add_issue(issue)

            report.finalize()
            return report
        except Exception:
            return None

    def can_import(self, file_path: str | Path) -> bool:
        return Path(file_path).suffix.lower() == ".xml"

    def _parse_xml_issue(self, issue_elem: ET.Element) -> QualityIssue | None:
        try:

            def get_text(element: ET.Element, tag: str, default: str = "") -> str:
                child = element.find(tag)
                return child.text if child is not None else default

            return QualityIssue(
                id=issue_elem.get("id", ""),
                type=issue_elem.get("type", ""),
                severity=SeverityLevel(issue_elem.get("severity", "low")),
                file=get_text(issue_elem, "file"),
                line=int(get_text(issue_elem, "line", "0")),
                column=0,
                message=get_text(issue_elem, "message"),
                suggestion=get_text(issue_elem, "suggestion"),
                confidence=float(get_text(issue_elem, "confidence", "0.0")),
                impact=ImpactLevel(get_text(issue_elem, "impact", "Low")),
                tool=get_text(issue_elem, "tool"),
                category=get_text(issue_elem, "category"),
            )
        except (ValueError, KeyError):
            return None


class QualityReportImporter:
    """
    Main importer that can handle multiple formats.
    """

    def __init__(self):
        self.importers = [JSONImporter(), CSVImporter(), XMLImporter()]

    def import_report(self, file_path: str | Path) -> QualityReport | None:
        """Import report using appropriate importer."""
        file_path = Path(file_path)
        for importer in self.importers:
            if importer.can_import(file_path):
                return importer.import_report(file_path)
        return None

    def get_supported_formats(self) -> list[str]:
        """Get list of supported file formats."""
        return [".json", ".csv", ".xml"]


__all__ = [
    "QualityImporter",
    "JSONImporter",
    "CSVImporter",
    "XMLImporter",
    "QualityReportImporter",
]
