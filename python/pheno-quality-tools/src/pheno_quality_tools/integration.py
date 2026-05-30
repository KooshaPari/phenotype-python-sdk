"""
Quality analysis framework integration and setup utilities.

This module provides integration helpers for setting up the quality framework
in other projects, including:
- Project-specific configuration generation
- Integration script creation (Makefile, CI/CD)
- Framework export/import utilities
"""

import shutil
from pathlib import Path
from typing import Any

from .config import get_config
from .manager import quality_manager


class QualityFrameworkIntegration:
    """
    Integration class for quality analysis framework.
    """

    def __init__(self, project_type: str = "default"):
        self.project_type = project_type
        self.config = get_config(project_type)
        self.manager = quality_manager
        self.manager.config = self.config

    def setup_for_project(self, project_path: str | Path) -> bool:
        """
        Setup quality framework for a specific project.
        """
        try:
            project_path = Path(project_path)

            # Create quality directory in project
            quality_dir = project_path / "quality"
            quality_dir.mkdir(exist_ok=True)

            # Create project-specific configuration
            self._create_project_config(quality_dir)

            # Create integration scripts
            self._create_integration_scripts(quality_dir, project_path)

            return True
        except Exception as e:
            print(f"Error setting up quality framework: {e}")
            return False

    def _create_project_config(self, quality_dir: Path):
        """
        Create project-specific configuration.
        """
        config_file = quality_dir / "project_config.py"

        config_content = f'''"""
Project-specific quality analysis configuration for {self.project_type}
"""

from pheno_quality_tools.config import create_custom_config

# Project-specific configuration
PROJECT_CONFIG = create_custom_config(
    '{self.project_type}',
    enabled_tools={self.config.enabled_tools},
    thresholds={self.config.thresholds},
    filters={self.config.filters},
    output_format='{self.config.output_format}',
    output_path='reports',
    parallel_analysis={self.config.parallel_analysis},
    max_workers={self.config.max_workers},
    timeout_seconds={self.config.timeout_seconds}
)
'''
        config_file.write_text(config_content)

    def _create_integration_scripts(self, quality_dir: Path, project_path: Path):
        """
        Create integration scripts for the project.
        """
        # Create main quality analysis script
        main_script = quality_dir / "analyze.py"
        main_script.write_text(self._get_main_analysis_script())
        main_script.chmod(0o755)

        # Create Makefile integration
        makefile_integration = quality_dir / "Makefile.integration"
        makefile_integration.write_text(self._get_makefile_integration())

    def _get_main_analysis_script(self) -> str:
        """
        Get main analysis script content.
        """
        return '''#!/usr/bin/env python3
"""
Quality analysis script for {self.project_type}
"""

import sys
import argparse
from pathlib import Path

# Import pheno_quality_tools
from pheno_quality_tools.manager import quality_manager
from pheno_quality_tools.config import get_config

def main():
    parser = argparse.ArgumentParser(description='Quality Analysis')
    parser.add_argument('path', nargs='?', default='.', help='Path to analyze')
    parser.add_argument('--tools', nargs='+', help='Specific tools to run')
    parser.add_argument('--output', '-o', help='Output path for report')
    parser.add_argument('--config', help='Configuration preset to use')
    parser.add_argument('--summary', action='store_true', help='Show summary only')

    args = parser.parse_args()

    # Get configuration
    config = get_config(args.config) if args.config else None
    if config:
        quality_manager.config = config

    # Run analysis
    print(f"🔍 Running quality analysis on {{args.path}}...")
    report = quality_manager.analyze_project(
        project_path=args.path,
        enabled_tools=args.tools,
        output_path=args.output
    )

    # Generate summary
    summary = quality_manager.generate_summary(report)

    if args.summary:
        print(f"\\nQuality Score: {{summary['quality_score']:.1f}}/100")
        print(f"Total Issues: {{summary['total_issues']}}")
    else:
        print(f"\\n📊 Quality Analysis Results")
        print(f"Quality Score: {{summary['quality_score']:.1f}}/100")
        print(f"Total Issues: {{summary['total_issues']}}")
        print(f"Files Affected: {{summary['files_affected']}}")

    return 0 if summary['quality_score'] >= 70 else 1

if __name__ == "__main__":
    sys.exit(main())
'''

    def _get_makefile_integration(self) -> str:
        """
        Get Makefile integration content.
        """
        return """# Quality Analysis Integration
# Add these targets to your Makefile

.PHONY: quality quality-full quality-report quality-clean

quality: ## Run basic quality analysis
	@echo "🔍 Running quality analysis..."
	python quality/analyze.py . --summary

quality-full: ## Run comprehensive quality analysis
	@echo "🔍 Running comprehensive quality analysis..."
	python quality/analyze.py . --output reports/quality_report.json

quality-report: ## Generate quality report in multiple formats
	@echo "📊 Generating quality reports..."
	python quality/analyze.py . --output reports/quality_report.json

quality-clean: ## Clean quality analysis reports
	@echo "🧹 Cleaning quality reports..."
	rm -rf reports/quality_*
"""


def integrate_quality_framework(
    project_path: str | Path,
    project_type: str = "default",
) -> bool:
    """
    Integrate quality framework into a project.
    """
    integration = QualityFrameworkIntegration(project_type)
    return integration.setup_for_project(project_path)


__all__ = ["QualityFrameworkIntegration", "integrate_quality_framework"]
