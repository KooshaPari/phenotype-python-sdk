"""
Quality analysis framework export/import functionality.

Provides utilities for exporting the quality framework for use in other projects
and importing exported frameworks.
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

from .config import CONFIG_REGISTRY


class QualityFrameworkExporter:
    """
    Export quality analysis framework for use in other projects.
    """

    def __init__(self, framework_path: str | Path):
        self.framework_path = Path(framework_path)

    def export_framework(
        self,
        output_path: str | Path,
        include_configs: bool = True,
    ) -> bool:
        """
        Export the quality analysis framework.
        """
        try:
            output_path = Path(output_path)
            output_path.mkdir(parents=True, exist_ok=True)

            # Copy the package
            pkg_src = self.framework_path
            pkg_dst = output_path / "pheno_quality_tools"
            if pkg_src.exists():
                shutil.copytree(pkg_src, pkg_dst, dirs_exist_ok=True)

            # Export configurations if requested
            if include_configs:
                self._export_configurations(output_path)

            # Create package manifest
            self._create_manifest(output_path)

            return True
        except Exception as e:
            print(f"Error exporting framework: {e}")
            return False

    def _export_configurations(self, output_path: Path):
        """Export configuration presets."""
        configs_dir = output_path / "configs"
        configs_dir.mkdir(exist_ok=True)

        for config_name, config in CONFIG_REGISTRY.items():
            config_file = configs_dir / f"{config_name}.json"
            config_file.write_text(json.dumps(config.to_dict(), indent=2))

    def _create_manifest(self, output_path: Path):
        """Create package manifest."""
        manifest = {
            "name": "pheno-quality-tools",
            "version": "1.0.0",
            "description": "Comprehensive quality analysis framework for Python projects",
            "author": "Phenotype Ecosystem",
            "created": datetime.now().isoformat(),
            "components": {
                "core": [
                    "core.py",
                    "manager.py",
                    "registry.py",
                    "plugins.py",
                    "config.py",
                    "utils.py",
                ],
                "tools": [
                    "pattern_detector.py",
                    "architectural_validator.py",
                    "performance_detector.py",
                    "security_scanner.py",
                    "code_smell_detector.py",
                    "integration_gates.py",
                    "atlas_health.py",
                ],
                "io": [
                    "exporters.py",
                    "importers.py",
                ],
                "configs": list(CONFIG_REGISTRY.keys()),
            },
        }

        manifest_file = output_path / "manifest.json"
        manifest_file.write_text(json.dumps(manifest, indent=2))


class QualityFrameworkImporter:
    """
    Import quality analysis framework from exported package.
    """

    def __init__(self, package_path: str | Path):
        self.package_path = Path(package_path)

    def import_framework(self, target_path: str | Path) -> bool:
        """
        Import the quality analysis framework.
        """
        try:
            target_path = Path(target_path)
            target_path.mkdir(parents=True, exist_ok=True)

            # Read manifest
            manifest_file = self.package_path / "manifest.json"
            if not manifest_file.exists():
                print("Error: No manifest.json found in package")
                return False

            # Copy package
            pkg_src = self.package_path / "pheno_quality_tools"
            pkg_dst = target_path / "pheno_quality_tools"
            if pkg_src.exists():
                shutil.copytree(pkg_src, pkg_dst, dirs_exist_ok=True)

            return True
        except Exception as e:
            print(f"Error importing framework: {e}")
            return False


def export_quality_framework(
    framework_path: str | Path,
    output_path: str | Path,
) -> bool:
    """
    Export quality analysis framework.
    """
    exporter = QualityFrameworkExporter(framework_path)
    return exporter.export_framework(output_path)


def import_quality_framework(package_path: str | Path, target_path: str | Path) -> bool:
    """
    Import quality analysis framework.
    """
    importer = QualityFrameworkImporter(package_path)
    return importer.import_framework(target_path)


__all__ = [
    "QualityFrameworkExporter",
    "QualityFrameworkImporter",
    "export_quality_framework",
    "import_quality_framework",
]
