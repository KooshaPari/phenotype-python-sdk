#!/usr/bin/env python3
"""
Pheno Analysis CLI - Unified code analysis suite.

A comprehensive CLI tool for analyzing Python codebases with multiple
analysis modules: complexity, churn, duplication, dependencies, coverage,
patterns, and code smells.
"""

import argparse
import sys
from pathlib import Path

# Import analysis modules
from pheno_analysis_cli import (
    analyze_complexity,
    analyze_churn,
    analyze_duplication,
    analyze_dependencies,
    coverage_analysis,
    analyze_test_coverage,
    code_smell_detector,
    advanced_pattern_detector,
    architectural_pattern_validator,
)


def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser with subcommands."""
    parser = argparse.ArgumentParser(
        prog="pheno-analyze",
        description="Pheno Analysis Suite - Comprehensive code analysis tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pheno-analyze complexity src/
  pheno-analyze churn . --days 30
  pheno-analyze duplication src/
  pheno-analyze dependencies .
  pheno-analyze coverage .
  pheno-analyze patterns src/
  pheno-analyze smells src/

For more help on a specific subcommand:
  pheno-analyze <command> --help
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available analysis commands")

    # Complexity subcommand
    complexity_parser = subparsers.add_parser(
        "complexity",
        help="Analyze code complexity (cyclomatic, maintainability, Halstead)",
    )
    complexity_parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to analyze (default: current directory)",
    )
    complexity_parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON format",
    )
    complexity_parser.add_argument(
        "--report",
        action="store_true",
        help="Generate detailed report",
    )

    # Churn subcommand
    churn_parser = subparsers.add_parser(
        "churn",
        help="Analyze git churn (code change frequency)",
    )
    churn_parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to analyze (default: current directory)",
    )
    churn_parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="Number of days to analyze (default: 30)",
    )
    churn_parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON format",
    )
    churn_parser.add_argument(
        "--output",
        type=Path,
        help="Output file for JSON report",
    )

    # Duplication subcommand
    duplication_parser = subparsers.add_parser(
        "duplication",
        help="Analyze code duplication",
    )
    duplication_parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to analyze (default: current directory)",
    )
    duplication_parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON format",
    )
    duplication_parser.add_argument(
        "--report",
        action="store_true",
        help="Generate detailed report",
    )

    # Dependencies subcommand
    dependencies_parser = subparsers.add_parser(
        "dependencies",
        help="Analyze project dependencies",
    )
    dependencies_parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to analyze (default: current directory)",
    )
    dependencies_parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON format",
    )
    dependencies_parser.add_argument(
        "--report",
        action="store_true",
        help="Generate detailed report",
    )

    # Coverage subcommand
    coverage_parser = subparsers.add_parser(
        "coverage",
        help="Run test coverage analysis",
    )
    coverage_parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to analyze (default: current directory)",
    )
    coverage_parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON format",
    )
    coverage_parser.add_argument(
        "--report",
        action="store_true",
        help="Generate detailed report",
    )
    coverage_parser.add_argument(
        "--gaps",
        action="store_true",
        help="Analyze test coverage gaps (mock analysis)",
    )

    # Patterns subcommand
    patterns_parser = subparsers.add_parser(
        "patterns",
        help="Detect architectural patterns and anti-patterns",
    )
    patterns_parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to analyze (default: current directory)",
    )
    patterns_parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON format",
    )
    patterns_parser.add_argument(
        "--category",
        choices=["anti-pattern", "vibe-pattern", "code-smell", "architectural"],
        help="Filter by category",
    )
    patterns_parser.add_argument(
        "--severity",
        choices=["critical", "high", "medium", "low", "info"],
        help="Filter by severity",
    )
    patterns_parser.add_argument(
        "--output",
        type=Path,
        help="Output file for report",
    )

    # Smells subcommand
    smells_parser = subparsers.add_parser(
        "smells",
        help="Detect code smells",
    )
    smells_parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to analyze (default: current directory)",
    )
    smells_parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON format",
    )
    smells_parser.add_argument(
        "--severity",
        choices=["low", "medium", "high"],
        help="Filter by severity",
    )
    smells_parser.add_argument(
        "--type",
        help="Filter by smell type",
    )

    # Version
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0",
    )

    return parser


def handle_complexity(args: argparse.Namespace) -> int:
    """Handle complexity analysis subcommand."""
    if args.report:
        report = analyze_complexity.generate_complexity_report()
        print(report)
        return 0

    analysis = analyze_complexity.run_complexity_analysis()

    if args.json:
        import json

        print(json.dumps(analysis, indent=2))
    else:
        print("Code Complexity Analysis Results:")
        overall = analysis.get("overall_complexity_score", {})
        print(f"  Overall Score: {overall.get('score', 0)}/100 ({overall.get('grade', 'N/A')})")

        cc_stats = analysis.get("cyclomatic_complexity", {}).get("stats", {})
        if cc_stats:
            print(f"  High Complexity Functions: {cc_stats.get('high_complexity_count', 0)}")

        mi_stats = analysis.get("maintainability_index", {}).get("stats", {})
        if mi_stats:
            print(f"  Low Maintainability Files: {mi_stats.get('low_maintainability_count', 0)}")

    return analysis.get("returncode", 1)


def handle_churn(args: argparse.Namespace) -> int:
    """Handle churn analysis subcommand."""
    since = f"{args.days} days ago" if args.days else None

    try:
        raw_log = analyze_churn._run_git_log(
            since=since,
            until=None,
            include=[args.path] if args.path else None,
        )
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    commits = analyze_churn._parse_git_log(raw_log)
    summary = analyze_churn.calculate_churn(commits)

    if args.json or args.output:
        import json

        payload = json.dumps(summary, indent=2)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(payload)
        if args.json:
            print(payload)
    else:
        print(analyze_churn.summarise_churn(summary, limit=10))

    return 0


def handle_duplication(args: argparse.Namespace) -> int:
    """Handle duplication analysis subcommand."""
    if args.report:
        report = analyze_duplication.generate_duplication_report()
        print(report)
        return 0

    analysis = analyze_duplication.run_duplication_analysis()

    if args.json:
        import json

        print(json.dumps(analysis, indent=2))
    else:
        print("Code Duplication Analysis Results:")
        stats = analysis.get("duplication_stats", {})
        print(f"  Duplicate Blocks: {stats.get('total_duplicate_blocks', 0)}")
        print(f"  Duplication %: {stats.get('duplication_percentage', 0):.2f}%")

        similar_groups = stats.get("similar_groups", [])
        print(f"  Similar Groups: {len(similar_groups)}")

    return analysis.get("returncode", 1)


def handle_dependencies(args: argparse.Namespace) -> int:
    """Handle dependencies analysis subcommand."""
    if args.report:
        report = analyze_dependencies.generate_dependency_report()
        print(report)
        return 0

    analysis = analyze_dependencies.run_dependency_analysis()

    if args.json:
        import json

        print(json.dumps(analysis, indent=2))
    else:
        print("Dependency Analysis Results:")
        stats = analysis.get("dependency_stats", {})
        print(f"  Total Packages: {stats.get('total_packages', 0)}")
        print(f"  Direct Dependencies: {stats.get('direct_dependencies', 0)}")
        print(f"  Outdated Packages: {len(stats.get('outdated_packages', []))}")
        print(f"  Security Issues: {len(stats.get('security_issues', []))}")

    return analysis.get("returncode", 1)


def handle_coverage(args: argparse.Namespace) -> int:
    """Handle coverage analysis subcommand."""
    if args.gaps:
        # Use the test coverage gaps analyzer
        analyzer = analyze_test_coverage.TestingCoverageAnalyzer(args.path)
        results = analyzer.run_comprehensive_analysis()

        if args.json:
            import json

            print(json.dumps(results, indent=2))
        else:
            report = analyzer.generate_test_coverage_report(results)
            print(report)

        return 0

    if args.report:
        report = coverage_analysis.generate_coverage_report()
        print(report)
        return 0

    analysis = coverage_analysis.run_coverage_analysis()

    if args.json:
        import json

        print(json.dumps(analysis, indent=2))
    else:
        print("Coverage Analysis Results:")
        print(f"  Status: {'PASSED' if analysis['returncode'] == 0 else 'FAILED'}")
        print(f"  HTML Report: {analysis.get('html_report', False)}")
        print(f"  XML Report: {analysis.get('xml_report', False)}")
        print(f"  JSON Report: {analysis.get('json_report', False)}")

    return analysis.get("returncode", 1)


def handle_patterns(args: argparse.Namespace) -> int:
    """Handle pattern detection subcommand."""
    root_path = Path(args.path)
    detector = advanced_pattern_detector.AdvancedPatternDetector(root_path)

    print(f"🔍 Scanning {args.path} for patterns...")
    detector.scan_directory(root_path)

    if args.json:
        import json

        output = {
            "summary": detector.results.summary(),
            "findings": [f.to_dict() for f in detector.results.findings],
        }

        if args.category:
            output["findings"] = [
                f for f in output["findings"] if f.get("category") == args.category
            ]

        if args.severity:
            output["findings"] = [
                f for f in output["findings"] if f.get("severity") == args.severity
            ]

        json_output = json.dumps(output, indent=2)

        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json_output)
        else:
            print(json_output)
    else:
        report = detector.generate_report()

        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(report)
        else:
            print(report)

    return 0


def handle_smells(args: argparse.Namespace) -> int:
    """Handle code smell detection subcommand."""
    detector = code_smell_detector.CodeSmellDetector()

    path = Path(args.path)
    files = [path] if path.is_file() else list(path.rglob("*.py"))

    print(f"🔍 Analyzing {len(files)} files for code smells...")

    for file_path in files:
        detector.analyze_file(file_path)

    report = detector.generate_report()

    # Filter results if requested
    if args.severity or args.type:
        filtered_smells = []
        for smell in report["smells"]:
            if args.severity and smell["severity"] != args.severity:
                continue
            if args.type and smell["type"] != args.type:
                continue
            filtered_smells.append(smell)
        report["smells"] = filtered_smells
        report["summary"]["total_smells"] = len(filtered_smells)

    if args.json:
        import json

        print(json.dumps(report, indent=2))
    else:
        print("\n🔍 CODE SMELL DETECTION REPORT")
        print("=" * 50)
        print(f"Total smells found: {report['summary']['total_smells']}")
        print(f"Files affected: {report['summary']['files_affected']}")
        print()

        print("Severity breakdown:")
        for severity, count in report["summary"]["severity_counts"].items():
            print(f"  {severity}: {count}")
        print()

        print("Smell types:")
        for smell_type, count in report["summary"]["smell_types"].items():
            print(f"  {smell_type}: {count}")
        print()

        if report["smells"]:
            print("Detailed findings (top 10):")
            for smell in report["smells"][:10]:
                print(
                    f"  {smell['severity'].upper()}: {smell['type']} in {smell['file']}:{smell['line']}",
                )
                print(f"    {smell['message']}")
                if smell.get("suggestion"):
                    print(f"    Suggestion: {smell['suggestion']}")
                print()

    return 0


def main(argv: list[str] | None = None) -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 1

    command_handlers = {
        "complexity": handle_complexity,
        "churn": handle_churn,
        "duplication": handle_duplication,
        "dependencies": handle_dependencies,
        "coverage": handle_coverage,
        "patterns": handle_patterns,
        "smells": handle_smells,
    }

    handler = command_handlers.get(args.command)
    if handler:
        return handler(args)

    print(f"Unknown command: {args.command}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
