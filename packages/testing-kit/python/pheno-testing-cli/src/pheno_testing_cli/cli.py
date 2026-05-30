#!/usr/bin/env python3
"""
Pheno Testing CLI - Comprehensive testing toolkit for Python projects.

Commands:
    security    Run security testing (DAST, penetration, compliance)
    performance Run performance testing (load, stress, benchmark)
    generate    Generate test data scenarios
    enhance     Enhance test files with better coverage
    parallel    Run tests in parallel for faster execution
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Optional


def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser."""
    parser = argparse.ArgumentParser(
        prog="pheno-test",
        description="Pheno Testing CLI - Comprehensive testing toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pheno-test security . --scan-depth deep
  pheno-test performance . --benchmark
  pheno-test generate . --scenarios 50
  pheno-test enhance tests/test_example.py
  pheno-test parallel . --workers 8
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Security command
    security_parser = subparsers.add_parser(
        "security",
        help="Run security testing (DAST, penetration, compliance)",
    )
    security_parser.add_argument(
        "path",
        type=str,
        help="Project path to scan",
    )
    security_parser.add_argument(
        "--scan-depth",
        choices=["normal", "deep"],
        default="normal",
        help="Security scan depth (default: normal)",
    )
    security_parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Output report file",
    )
    security_parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON format",
    )
    security_parser.add_argument(
        "--base-url",
        type=str,
        default="http://localhost:8000",
        help="Base URL for DAST testing",
    )

    # Performance command
    performance_parser = subparsers.add_parser(
        "performance",
        help="Run performance testing (load, stress, benchmark)",
    )
    performance_parser.add_argument(
        "path",
        type=str,
        help="Project path",
    )
    performance_parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Run benchmark tests",
    )
    performance_parser.add_argument(
        "--load-test",
        type=str,
        help="Run specific load test (light_load, medium_load, heavy_load)",
    )
    performance_parser.add_argument(
        "--stress-test",
        action="store_true",
        help="Run stress test",
    )
    performance_parser.add_argument(
        "--memory-test",
        action="store_true",
        help="Run memory leak test",
    )
    performance_parser.add_argument(
        "--cpu-test",
        action="store_true",
        help="Run CPU intensive test",
    )
    performance_parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Output report file",
    )
    performance_parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON format",
    )

    # Generate command
    generate_parser = subparsers.add_parser(
        "generate",
        help="Generate test data scenarios",
    )
    generate_parser.add_argument(
        "path",
        type=str,
        help="Project path",
    )
    generate_parser.add_argument(
        "--scenarios",
        type=int,
        default=10,
        help="Number of scenarios to generate (default: 10)",
    )
    generate_parser.add_argument(
        "--output-dir",
        type=str,
        default="test_data",
        help="Output directory for generated scenarios",
    )
    generate_parser.add_argument(
        "--type",
        choices=["database", "api", "security", "performance", "all"],
        default="all",
        help="Type of scenarios to generate",
    )

    # Enhance command
    enhance_parser = subparsers.add_parser(
        "enhance",
        help="Enhance test files with better coverage",
    )
    enhance_parser.add_argument(
        "file",
        type=str,
        help="Test file to enhance",
    )
    enhance_parser.add_argument(
        "--templates",
        action="store_true",
        help="Generate test templates",
    )
    enhance_parser.add_argument(
        "--infrastructure",
        action="store_true",
        help="Enhance testing infrastructure",
    )
    enhance_parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Output directory for enhanced files",
    )

    # Parallel command
    parallel_parser = subparsers.add_parser(
        "parallel",
        help="Run tests in parallel for faster execution",
    )
    parallel_parser.add_argument(
        "path",
        type=str,
        help="Project path containing tests",
    )
    parallel_parser.add_argument(
        "--workers",
        "-w",
        type=int,
        default=4,
        help="Number of parallel workers (default: 4)",
    )
    parallel_parser.add_argument(
        "--tiers",
        nargs="+",
        choices=["database_tier", "api_tier", "external_tier", "unit_tier", "e2e_tier"],
        help="Specific test tiers to run",
    )
    parallel_parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Run benchmark comparison",
    )
    parallel_parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Output report file",
    )

    return parser


def run_security_command(args: argparse.Namespace) -> int:
    """Run security testing command."""
    try:
        from .security_testing import (
            ComplianceChecker,
            DynamicApplicationSecurityTester,
            PenetrationTester,
            SecurityTestResult,
        )

        print(f"🔒 Running security tests on: {args.path}")
        print(f"   Scan depth: {args.scan_depth}")

        results: dict[str, Any] = {}

        # Run DAST scan
        print("\n🔍 Running Dynamic Application Security Testing (DAST)...")
        dast_tester = DynamicApplicationSecurityTester(base_url=args.base_url)
        endpoints = ["/", "/api/v1/health", "/api/v1/users", "/api/v1/data"]
        dast_result = dast_tester.run_dast_scan(endpoints)
        results["dast"] = {
            "status": dast_result.status,
            "risk_score": dast_result.risk_score,
            "vulnerabilities_found": len(dast_result.vulnerabilities),
            "scan_duration": dast_result.scan_duration,
        }

        # Run penetration test (only in deep mode)
        if args.scan_depth == "deep":
            print("\n🎯 Running Penetration Testing...")
            pen_tester = PenetrationTester(
                target_host="localhost",
                target_port=8000,
            )
            pen_result = pen_tester.run_penetration_test()
            results["penetration"] = {
                "status": pen_result.status,
                "risk_score": pen_result.risk_score,
                "vulnerabilities_found": len(pen_result.vulnerabilities),
                "scan_duration": pen_result.scan_duration,
            }

        # Run compliance checks
        print("\n📋 Running Compliance Checks...")
        compliance_checker = ComplianceChecker()
        compliance_results = compliance_checker.run_compliance_checks()
        results["compliance"] = {
            "checks_run": len(compliance_results),
            "passed": len([c for c in compliance_results if c.status == "pass"]),
            "failed": len([c for c in compliance_results if c.status == "fail"]),
        }

        # Output results
        if args.json:
            output = json.dumps(results, indent=2)
        else:
            output = f"""
🔒 SECURITY TEST RESULTS
{"=" * 50}
DAST Scan:
  Status: {results["dast"]["status"]}
  Risk Score: {results["dast"]["risk_score"]:.1f}/100
  Vulnerabilities: {results["dast"]["vulnerabilities_found"]}
  Duration: {results["dast"]["scan_duration"]:.1f}s
"""
            if "penetration" in results:
                output += f"""
Penetration Test:
  Status: {results["penetration"]["status"]}
  Risk Score: {results["penetration"]["risk_score"]:.1f}/100
  Vulnerabilities: {results["penetration"]["vulnerabilities_found"]}
  Duration: {results["penetration"]["scan_duration"]:.1f}s
"""
            output += f"""
Compliance Checks:
  Total: {results["compliance"]["checks_run"]}
  Passed: {results["compliance"]["passed"]}
  Failed: {results["compliance"]["failed"]}
"""

        if args.output:
            with open(args.output, "w") as f:
                f.write(output)
            print(f"\n📄 Report saved to: {args.output}")
        else:
            print(output)

        # Return non-zero if critical vulnerabilities found
        total_vulns = results["dast"]["vulnerabilities_found"]
        if "penetration" in results:
            total_vulns += results["penetration"]["vulnerabilities_found"]

        return 1 if total_vulns > 0 else 0

    except Exception as e:
        print(f"❌ Security testing failed: {e}")
        return 1


def run_performance_command(args: argparse.Namespace) -> int:
    """Run performance testing command."""
    try:
        from .performance_testing import PerformanceTestingFramework

        print(f"⚡ Running performance tests on: {args.path}")

        framework = PerformanceTestingFramework(args.path)

        # Run specific test or comprehensive
        if args.load_test:
            print(f"\n📊 Running load test: {args.load_test}")
            report = framework.run_comprehensive_tests()
        elif args.stress_test:
            print("\n💪 Running stress test...")
            report = framework.run_comprehensive_tests()
        elif args.memory_test:
            print("\n🧠 Running memory leak test...")
            report = framework.run_comprehensive_tests()
        elif args.cpu_test:
            print("\n🔥 Running CPU intensive test...")
            report = framework.run_comprehensive_tests()
        else:
            print("\n🚀 Running comprehensive performance tests...")
            report = framework.run_comprehensive_tests()

        # Output results
        if args.json:
            output = json.dumps(report, indent=2)
        else:
            summary = report.get("summary", {})
            output = f"""
⚡ PERFORMANCE TEST RESULTS
{"=" * 50}
Total Tests: {summary.get("total_tests", 0)}
Passed: {summary.get("passed", 0)}
Failed: {summary.get("failed", 0)}
Warnings: {summary.get("warnings", 0)}
Score: {summary.get("score", 0)}/100

Recommendations:
"""
            for rec in report.get("recommendations", []):
                output += f"  • {rec}\n"

        if args.output:
            with open(args.output, "w") as f:
                f.write(output)
            print(f"\n📄 Report saved to: {args.output}")
        else:
            print(output)

        return 0 if report.get("summary", {}).get("failed", 0) == 0 else 1

    except Exception as e:
        print(f"❌ Performance testing failed: {e}")
        return 1


def run_generate_command(args: argparse.Namespace) -> int:
    """Run test data generation command."""
    try:
        from .test_data_generator import TestDataEnhancementSystem

        print(f"🎲 Generating test scenarios for: {args.path}")
        print(f"   Scenarios: {args.scenarios}")
        print(f"   Type: {args.type}")

        system = TestDataEnhancementSystem(args.path)

        # Generate scenarios
        scenarios = system.generate_test_data_scenarios()
        templates = system.create_test_data_templates()

        # Create output directory
        output_dir = Path(args.path) / args.output_dir
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save scenarios
        if args.type in ["database", "all"]:
            db_scenarios = scenarios.get("database_test_scenarios", {})
            with open(output_dir / "database_scenarios.json", "w") as f:
                json.dump(db_scenarios, f, indent=2)
            print(f"   💾 Database scenarios: {len(db_scenarios)} categories")

        if args.type in ["api", "all"]:
            api_scenarios = scenarios.get("api_test_scenarios", {})
            with open(output_dir / "api_scenarios.json", "w") as f:
                json.dump(api_scenarios, f, indent=2)
            print(f"   💾 API scenarios: {len(api_scenarios)} categories")

        if args.type in ["security", "all"]:
            security_scenarios = scenarios.get("security_test_scenarios", {})
            with open(output_dir / "security_scenarios.json", "w") as f:
                json.dump(security_scenarios, f, indent=2)
            print(f"   💾 Security scenarios: {len(security_scenarios)} categories")

        if args.type in ["performance", "all"]:
            perf_scenarios = scenarios.get("performance_test_scenarios", {})
            with open(output_dir / "performance_scenarios.json", "w") as f:
                json.dump(perf_scenarios, f, indent=2)
            print(f"   💾 Performance scenarios: {len(perf_scenarios)} categories")

        # Save templates
        with open(output_dir / "templates.json", "w") as f:
            json.dump(templates, f, indent=2)

        print(f"\n✅ Generated test scenarios saved to: {output_dir}")
        return 0

    except Exception as e:
        print(f"❌ Test generation failed: {e}")
        return 1


def run_enhance_command(args: argparse.Namespace) -> int:
    """Run test enhancement command."""
    try:
        from .test_enhancer import TestingInfrastructureEnhancer

        print(f"✨ Enhancing test file: {args.file}")

        # Get project root from file path
        file_path = Path(args.file)
        project_root = file_path.parent
        while project_root and not (project_root / "pyproject.toml").exists():
            project_root = project_root.parent
            if project_root == project_root.parent:
                project_root = file_path.parent
                break

        enhancer = TestingInfrastructureEnhancer(str(project_root))

        if args.templates:
            print("\n📋 Generating test templates...")
            enhancer._generate_test_templates()
            print("   ✅ Test templates generated")

        if args.infrastructure:
            print("\n🏗️  Enhancing testing infrastructure...")
            results = enhancer.enhance_testing_infrastructure()
            print(f"   ✅ Applied {len(results.get('enhancements', []))} enhancements")

        print("\n✅ Test enhancement complete!")
        return 0

    except Exception as e:
        print(f"❌ Test enhancement failed: {e}")
        return 1


def run_parallel_command(args: argparse.Namespace) -> int:
    """Run parallel test execution command."""
    try:
        from .parallel_runner import LocalParallelTestRunner

        print(f"🚀 Running tests in parallel on: {args.path}")
        print(f"   Workers: {args.workers}")

        runner = LocalParallelTestRunner(args.path)

        if args.benchmark:
            print("\n📊 Running benchmark comparison...")
            import time

            # Sequential execution
            print("🐌 Sequential execution...")
            start = time.time()
            import subprocess

            subprocess.run(
                ["python", "-m", "pytest", args.path, "-v"],
                capture_output=True,
            )
            sequential_time = time.time() - start

            # Parallel execution
            print("⚡ Parallel execution...")
            start = time.time()
            results = runner.run_parallel_tests(args.tiers, args.workers)
            parallel_time = time.time() - start

            speedup = sequential_time / parallel_time if parallel_time > 0 else 1.0

            print(f"\n{'=' * 50}")
            print(f"📊 BENCHMARK RESULTS")
            print(f"{'=' * 50}")
            print(f"Sequential: {sequential_time:.2f}s")
            print(f"Parallel:   {parallel_time:.2f}s")
            print(f"Speedup:    {speedup:.2f}x")
        else:
            results = runner.run_parallel_tests(args.tiers, args.workers)

            # Generate summary
            total_success = sum(1 for r in results.values() if r["success"])
            total_tiers = len(results)

            print(f"\n{'=' * 50}")
            print(f"🎯 PARALLEL TEST SUMMARY")
            print(f"{'=' * 50}")
            print(f"Workers: {args.workers}")
            print(f"Success: {total_success}/{total_tiers}")

            for tier, result in results.items():
                status = "✅ PASS" if result["success"] else "❌ FAIL"
                print(f"{tier:20s} {status}")

        if args.output:
            with open(args.output, "w") as f:
                json.dump(results, f, indent=2, default=str)
            print(f"\n📄 Report saved to: {args.output}")

        return 0

    except Exception as e:
        print(f"❌ Parallel test execution failed: {e}")
        return 1


def main(argv: Optional[list[str]] = None) -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 1

    # Dispatch to appropriate command handler
    commands = {
        "security": run_security_command,
        "performance": run_performance_command,
        "generate": run_generate_command,
        "enhance": run_enhance_command,
        "parallel": run_parallel_command,
    }

    handler = commands.get(args.command)
    if handler:
        return handler(args)
    else:
        print(f"❌ Unknown command: {args.command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
