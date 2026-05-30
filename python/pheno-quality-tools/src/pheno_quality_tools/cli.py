#!/usr/bin/env python3
"""
pheno-quality-gates - CLI tool for quality analysis

Commands:
    check [path]      Run quality checks on a directory
    validate [config] Validate quality gates against thresholds
    atlas [path]      Run Atlas health analysis
    export [format]   Export quality report to various formats
    import [file]     Import quality report from file
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

# Add the package to path if running directly
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

from pheno_quality_tools.manager import quality_manager
from pheno_quality_tools.config import get_config, list_configs, create_custom_config
from pheno_quality_tools.core import QualityConfig
from pheno_quality_tools.importers import QualityReportImporter


def cmd_check(args: argparse.Namespace) -> int:
    """Run quality checks on a path."""
    path = Path(args.path) if args.path else Path(".")

    if not path.exists():
        print(f"Error: Path not found: {path}")
        return 1

    # Get configuration
    config = get_config(args.config) if args.config else QualityConfig()
    if args.tools:
        config.enabled_tools = args.tools

    quality_manager.config = config

    print(f"🔍 Running quality analysis on {path}...")
    print(f"Tools: {', '.join(config.enabled_tools) or 'default'}")

    # Run analysis
    if path.is_file():
        report = quality_manager.analyze_file(path, config.enabled_tools)
    else:
        report = quality_manager.analyze_project(
            path,
            config.enabled_tools,
            args.output,
        )

    # Generate and display summary
    summary = quality_manager.generate_summary(report)

    print(f"\n📊 Quality Analysis Results")
    print(f"Project: {summary['project_name']}")
    print(f"Quality Score: {summary['quality_score']:.1f}/100")
    print(f"Quality Status: {summary['quality_status']}")
    print(f"Total Issues: {summary['total_issues']}")
    print(f"Files Affected: {summary['files_affected']}")
    print(f"Analysis Duration: {summary['analysis_duration']:.2f}s")

    if summary["issues_by_severity"]:
        print("\nIssues by Severity:")
        for severity, count in summary["issues_by_severity"].items():
            print(f"  {severity}: {count}")

    if summary["recommendations"] and not args.quiet:
        print("\n🔧 Recommendations:")
        for rec in summary["recommendations"]:
            print(f"  • {rec}")

    # Output handling
    if args.output:
        print(f"\n📄 Report saved to: {args.output}")

    if args.json:
        print(json.dumps(summary, indent=2))

    # Return exit code based on quality score
    threshold = args.threshold or 70
    return 0 if summary["quality_score"] >= threshold else 1


def cmd_validate(args: argparse.Namespace) -> int:
    """Validate quality gates against thresholds."""
    print("🚀 Running Quality Gate Validation...")

    failures = []

    # Check for Ruff issues
    if os.path.exists("ruff_report.json"):
        try:
            with open("ruff_report.json") as f:
                data = json.load(f)
            issue_count = len(data)
            threshold = args.ruff_threshold or 50
            if issue_count > threshold:
                failures.append(f"Ruff issues ({issue_count}) exceed threshold ({threshold})")
            else:
                print(f"✅ Ruff issues ({issue_count}) within threshold")
        except Exception as e:
            failures.append(f"Failed to parse Ruff report: {e}")
    else:
        print("⚠️  Ruff report not found (ruff_report.json)")

    # Check for MyPy errors
    mypy_report = Path("mypy_report") / "report.json"
    if mypy_report.exists():
        try:
            with open(mypy_report) as f:
                data = json.load(f)
            error_count = len(data.get("errors", []))
            threshold = args.mypy_threshold or 20
            if error_count > threshold:
                failures.append(f"MyPy errors ({error_count}) exceed threshold ({threshold})")
            else:
                print(f"✅ MyPy errors ({error_count}) within threshold")
        except Exception as e:
            failures.append(f"Failed to parse MyPy report: {e}")
    else:
        print("⚠️  MyPy report not found (mypy_report/report.json)")

    # Check coverage
    if os.path.exists("coverage.xml"):
        try:
            import xml.etree.ElementTree as ET

            tree = ET.parse("coverage.xml")
            root = tree.getroot()
            coverage_elem = root if root.tag == "coverage" else root.find(".//coverage")
            if coverage_elem is not None:
                line_rate = float(coverage_elem.get("line-rate", 0))
                coverage_percent = line_rate * 100
                threshold = args.coverage_threshold or 65
                if coverage_percent < threshold:
                    failures.append(
                        f"Coverage ({coverage_percent:.1f}%) below threshold ({threshold}%)"
                    )
                else:
                    print(f"✅ Coverage ({coverage_percent:.1f}%) meets threshold")
        except Exception as e:
            failures.append(f"Failed to parse coverage: {e}")
    else:
        print("⚠️  Coverage report not found (coverage.xml)")

    # Run quality analysis if requested
    if args.run_analysis:
        path = Path(args.path) if args.path else Path(".")
        config = get_config(args.config) if args.config else QualityConfig()
        quality_manager.config = config
        report = quality_manager.analyze_project(path)
        summary = quality_manager.generate_summary(report)

        score_threshold = args.quality_threshold or 70
        if summary["quality_score"] < score_threshold:
            failures.append(
                f"Quality score ({summary['quality_score']:.1f}) below threshold ({score_threshold})"
            )
        else:
            print(f"✅ Quality score ({summary['quality_score']:.1f}) meets threshold")

    # Report results
    print("\n" + "=" * 50)
    print("QUALITY GATE RESULTS")
    print("=" * 50)

    if failures:
        print("❌ QUALITY GATES FAILED")
        print("\nFailures:")
        for failure in failures:
            print(f"  • {failure}")
        return 1

    print("✅ ALL QUALITY GATES PASSED")
    return 0


def cmd_atlas(args: argparse.Namespace) -> int:
    """Run Atlas health analysis."""
    from pheno_quality_tools.atlas_health import AtlasHealthAnalyzer

    path = Path(args.path) if args.path else Path(".")

    print(f"🔍 Running Atlas Health Analysis on {path}...")

    analyzer = AtlasHealthAnalyzer()
    issues = analyzer.analyze_directory(path)

    print(f"\n📊 Atlas Health Results")
    print(f"Total Issues: {len(issues)}")

    if issues:
        print("\nIssues by Category:")
        categories = {}
        for issue in issues:
            cat = issue.category or "General"
            categories[cat] = categories.get(cat, 0) + 1
        for cat, count in categories.items():
            print(f"  {cat}: {count}")

    if args.output:
        report_data = {
            "total_issues": len(issues),
            "issues": [issue.to_dict() for issue in issues],
        }
        with open(args.output, "w") as f:
            json.dump(report_data, f, indent=2)
        print(f"\n📄 Report saved to: {args.output}")

    return 0 if not issues else 1


def cmd_export(args: argparse.Namespace) -> int:
    """Export quality report to various formats."""
    importer = QualityReportImporter()

    if not args.input:
        print("Error: --input required for export")
        return 1

    report = importer.import_report(args.input)
    if not report:
        print(f"Error: Could not import report from {args.input}")
        return 1

    fmt = args.format or "json"
    output = args.output or f"quality_report.{fmt}"

    success = quality_manager.export_report(report, output, fmt)

    if success:
        print(f"✅ Report exported to: {output}")
        return 0
    else:
        print(f"❌ Failed to export report")
        return 1


def cmd_import(args: argparse.Namespace) -> int:
    """Import quality report from file."""
    if not args.file:
        print("Error: file required for import")
        return 1

    importer = QualityReportImporter()
    report = importer.import_report(args.file)

    if not report:
        print(f"Error: Could not import report from {args.file}")
        return 1

    summary = quality_manager.generate_summary(report)

    print(f"✅ Report imported from: {args.file}")
    print(f"\n📊 Report Summary")
    print(f"Project: {summary['project_name']}")
    print(f"Quality Score: {summary['quality_score']:.1f}/100")
    print(f"Total Issues: {summary['total_issues']}")

    if args.output:
        quality_manager.export_report(report, args.output)
        print(f"\n📄 Re-exported to: {args.output}")

    return 0


def cmd_list(args: argparse.Namespace) -> int:
    """List available tools and configurations."""
    if args.what == "tools":
        print("Available Quality Analysis Tools:")
        for tool in quality_manager.list_tools():
            info = quality_manager.get_tool_info(tool)
            desc = info.get("description", "No description") if info else "No description"
            print(f"  • {tool}: {desc}")

    elif args.what == "configs":
        print("Available Configuration Presets:")
        for cfg in list_configs():
            print(f"  • {cfg}")

    return 0


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="pheno-quality-gates",
        description="Quality analysis CLI for Python projects",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pheno-quality-gates check .                          # Check current directory
  pheno-quality-gates check src/ --output report.json  # Check with output
  pheno-quality-gates validate --run-analysis          # Validate with analysis
  pheno-quality-gates atlas .                          # Atlas health check
  pheno-quality-gates export --input report.json --format html
  pheno-quality-gates list tools                       # List available tools
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # check command
    check_parser = subparsers.add_parser("check", help="Run quality checks")
    check_parser.add_argument("path", nargs="?", default=".", help="Path to analyze")
    check_parser.add_argument("--tools", nargs="+", help="Specific tools to run")
    check_parser.add_argument("--config", help="Configuration preset")
    check_parser.add_argument("--output", "-o", help="Output path for report")
    check_parser.add_argument("--threshold", type=float, help="Quality score threshold")
    check_parser.add_argument("--json", action="store_true", help="Output JSON summary")
    check_parser.add_argument("--quiet", "-q", action="store_true", help="Quiet mode")
    check_parser.set_defaults(func=cmd_check)

    # validate command
    validate_parser = subparsers.add_parser("validate", help="Validate quality gates")
    validate_parser.add_argument("config", nargs="?", help="Configuration preset")
    validate_parser.add_argument("--ruff-threshold", type=int, help="Ruff issues threshold")
    validate_parser.add_argument("--mypy-threshold", type=int, help="MyPy errors threshold")
    validate_parser.add_argument("--coverage-threshold", type=float, help="Coverage threshold")
    validate_parser.add_argument("--quality-threshold", type=float, help="Quality score threshold")
    validate_parser.add_argument("--run-analysis", action="store_true", help="Run quality analysis")
    validate_parser.add_argument("--path", default=".", help="Path to analyze")
    validate_parser.set_defaults(func=cmd_validate)

    # atlas command
    atlas_parser = subparsers.add_parser("atlas", help="Run Atlas health analysis")
    atlas_parser.add_argument("path", nargs="?", default=".", help="Path to analyze")
    atlas_parser.add_argument("--output", "-o", help="Output path for report")
    atlas_parser.set_defaults(func=cmd_atlas)

    # export command
    export_parser = subparsers.add_parser("export", help="Export quality report")
    export_parser.add_argument("--input", "-i", required=True, help="Input report file")
    export_parser.add_argument(
        "--format", choices=["json", "html", "md", "csv", "xml"], help="Export format"
    )
    export_parser.add_argument("--output", "-o", help="Output path")
    export_parser.set_defaults(func=cmd_export)

    # import command
    import_parser = subparsers.add_parser("import", help="Import quality report")
    import_parser.add_argument("file", help="Report file to import")
    import_parser.add_argument("--output", "-o", help="Output path for re-export")
    import_parser.set_defaults(func=cmd_import)

    # list command
    list_parser = subparsers.add_parser("list", help="List tools or configs")
    list_parser.add_argument("what", choices=["tools", "configs"], help="What to list")
    list_parser.set_defaults(func=cmd_list)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
