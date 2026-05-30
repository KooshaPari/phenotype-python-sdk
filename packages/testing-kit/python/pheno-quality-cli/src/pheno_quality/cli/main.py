"""
Pheno Quality CLI - CLI entry points for quality analysis.
"""

import sys
from pathlib import Path
from typing import Optional

import typer
from typing_extensions import Annotated

from pheno_quality.config import get_config, list_configs
from pheno_quality.manager import quality_manager

app = typer.Typer(help="Pheno Quality CLI - Code quality analysis tool")

# Default configuration
DEFAULT_CONFIG = get_config("default")


@app.command(name="check")
def quality_check(
    path: Annotated[Path, typer.Argument(help="Path to analyze")] = Path("."),
    format: Annotated[
        str, typer.Option("--format", "-f", help="Output format (json|html|markdown|csv)")
    ] = "json",
    output: Annotated[
        Optional[Path], typer.Option("--output", "-o", help="Output file path")
    ] = None,
    tools: Annotated[
        Optional[str], typer.Option("--tools", "-t", help="Comma-separated list of tools to run")
    ] = None,
    config: Annotated[
        str, typer.Option("--config", "-c", help="Configuration preset to use")
    ] = "default",
    severity: Annotated[
        Optional[str],
        typer.Option("--severity", "-s", help="Filter by severity (low|medium|high|critical)"),
    ] = None,
    summary: Annotated[bool, typer.Option("--summary", help="Show summary only")] = False,
):
    """
    Run quality analysis on a path.

    Examples:
        pheno-quality-check .
        pheno-quality-check ./src --format html --output report.html
        pheno-quality-check . --tools pattern_detector,security_scanner
        pheno-quality-check . --config strict --severity high
    """
    # Load configuration
    config_obj = get_config(config)
    quality_manager.config = config_obj

    # Parse tools
    enabled_tools = None
    if tools:
        enabled_tools = [t.strip() for t in tools.split(",")]

    # Determine output path
    if output is None:
        output = Path(f"quality_report.{format}")

    typer.echo(f"🔍 Running quality analysis on {path}...")

    # Run analysis
    report = quality_manager.analyze_project(
        project_path=path,
        enabled_tools=enabled_tools,
        output_path=output,
    )

    # Generate summary
    result_summary = quality_manager.generate_summary(report)

    if summary:
        # Show summary only
        typer.echo(f"\n📊 Quality Analysis Summary")
        typer.echo(f"Project: {result_summary['project_name']}")
        typer.echo(f"Quality Score: {result_summary['quality_score']:.1f}/100")
        typer.echo(f"Total Issues: {result_summary['total_issues']}")
        typer.echo(f"Files Affected: {result_summary['files_affected']}")
        typer.echo(f"Quality Status: {result_summary['quality_status']}")

        if result_summary["recommendations"]:
            typer.echo("\n🔧 Recommendations:")
            for rec in result_summary["recommendations"]:
                typer.echo(f"  {rec}")
    else:
        # Show detailed results
        typer.echo(f"\n📊 Quality Analysis Results")
        typer.echo(f"Quality Score: {result_summary['quality_score']:.1f}/100")
        typer.echo(f"Total Issues: {result_summary['total_issues']}")

        typer.echo("\nIssues by Severity:")
        for sev, count in result_summary["issues_by_severity"].items():
            typer.echo(f"  {sev}: {count}")

        typer.echo(f"\nReport exported to: {output}")

    # Exit with appropriate code
    if result_summary["quality_score"] < 70:
        raise typer.Exit(code=1)


@app.command(name="report")
def quality_report(
    path: Annotated[Path, typer.Argument(help="Path to analyze")] = Path("."),
    output: Annotated[Path, typer.Option("--output", "-o", help="Output file path")] = Path(
        "quality_report.json"
    ),
    config: Annotated[str, typer.Option("--config", "-c", help="Configuration preset")] = "default",
):
    """
    Generate a quality report for a path.

    Examples:
        pheno-quality-report . --output report.json
        pheno-quality-report ./src --config strict --output report.html
    """
    # Load configuration
    config_obj = get_config(config)
    quality_manager.config = config_obj

    typer.echo(f"📊 Generating quality report for {path}...")

    # Run analysis
    report = quality_manager.analyze_project(
        project_path=path,
        output_path=output,
    )

    # Generate summary
    result_summary = quality_manager.generate_summary(report)

    typer.echo(f"✅ Report saved to: {output}")
    typer.echo(f"Quality Score: {result_summary['quality_score']:.1f}/100")
    typer.echo(f"Total Issues: {result_summary['total_issues']}")


@app.command(name="export")
def quality_export(
    format: Annotated[
        str, typer.Argument(help="Export format (json|html|markdown|csv|xml)")
    ] = "json",
    output: Annotated[Path, typer.Option("--output", "-o", help="Output file path")] = Path(
        "quality_export.json"
    ),
    input_report: Annotated[
        Optional[Path], typer.Option("--input", "-i", help="Input report to convert")
    ] = None,
):
    """
    Export a quality report in different formats.

    Examples:
        pheno-quality-export json --output report.json
        pheno-quality-export html --input report.json --output report.html
        pheno-quality-export csv --output report.csv
    """
    if input_report:
        # Convert existing report
        typer.echo(f"📤 Converting {input_report} to {format}...")
        report = quality_manager.import_report(input_report)
        if report:
            quality_manager.export_report(report, output)
            typer.echo(f"✅ Report exported to: {output}")
        else:
            typer.echo(f"❌ Failed to import report from {input_report}")
            raise typer.Exit(code=1)
    else:
        typer.echo(f"📤 Export format: {format}")
        typer.echo(f"Output: {output}")
        typer.echo("Use 'pheno-quality-check' to generate a report first, then export it.")


@app.command(name="import")
def quality_import(
    file: Annotated[Path, typer.Argument(help="File to import")],
    format: Annotated[
        str, typer.Option("--format", "-f", help="Input format (json|csv|xml)")
    ] = "json",
):
    """
    Import a quality report from various formats.

    Examples:
        pheno-quality-import report.json
        pheno-quality-import report.csv --format csv
        pheno-quality-import report.xml --format xml
    """
    typer.echo(f"📥 Importing report from {file}...")

    report = quality_manager.import_report(file)
    if report:
        typer.echo(f"✅ Report imported successfully")
        typer.echo(f"Project: {report.project_name}")
        typer.echo(f"Total Issues: {report.metrics.total_issues}")
        typer.echo(f"Quality Score: {report.metrics.quality_score:.1f}/100")
    else:
        typer.echo(f"❌ Failed to import report from {file}")
        raise typer.Exit(code=1)


def main_check():
    """Entry point for pheno-quality-check command."""
    app()


def main_report():
    """Entry point for pheno-quality-report command."""
    app()


def main_export():
    """Entry point for pheno-quality-export command."""
    app()


def main_import():
    """Entry point for pheno-quality-import command."""
    app()


if __name__ == "__main__":
    app()
