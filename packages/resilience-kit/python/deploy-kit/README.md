# Pheno-Deploy-Kit

**Universal deployment toolkit with NVMS format support for modern platforms, cloud infrastructure, and pheno-sdk vendoring.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

### 🚀 Deployment Abstractions
- **Local Process Management**: Run and monitor local services with `LocalServiceManager`
- **NVMS Format**: Universal deployment configuration parsing (Node Version Manager Script)
- **Platform Clients**: Vercel, Fly.io, AWS, GCP, Azure support
- **Cloud Orchestration**: Docker, Kubernetes integration interfaces

### 📦 Pheno-SDK Vendoring
- **Auto-Detection**: Automatically detect which pheno-sdk packages your project uses
- **CLI & API**: Use via `pheno-vendor` command or Python API
- **Multi-Platform**: Generate configs for Vercel, Docker, Lambda, Railway, etc.
- **Validation**: Built-in validation and import testing
- **Cross-Platform**: Python-based (works on Windows, macOS, Linux)

### 🔧 Build Tools
- **Platform Detection**: Auto-detect deployment platform from project files
- **Hook Generation**: Generate platform-specific build hooks
- **Configuration**: Auto-generate deployment configs (vercel.json, Dockerfile, etc.)
- **Validation**: Deployment readiness checks
- **Git Integration**: Pre-push hooks for automatic vendoring

### 🏥 Health Checks
- **HTTP Health Checks**: Check service health via HTTP endpoints
- **TCP Port Checks**: Verify service availability on TCP ports
- **Extensible**: Create custom health check implementations

## Installation

```bash
# Install from source
pip install /path/to/ResilienceKit/python/deploy-kit

# Or install with extras
pip install "/path/to/ResilienceKit/python/deploy-kit[full]"  # All platform support
pip install "/path/to/ResilienceKit/python/deploy-kit[vercel,docker]"  # Specific platforms
```

## Quick Start

### Pheno-SDK Vendoring

Replace custom vendoring scripts with the unified toolkit:

```bash
# In your project directory
cd /path/to/your/project

# Vendor packages (auto-detect)
pheno-vendor setup

# Output:
# ✓ Detected 8 used packages
# ✓ Vendored 8/8 packages
# ✓ Created requirements-prod.txt
# ✓ Created sitecustomize.py
# ✓ All packages validated!
```

What gets created:
```
your-project/
├── pheno_vendor/           # Vendored packages
├── requirements-prod.txt   # Production requirements
└── sitecustomize.py        # Python path setup
```

### Deployment Configuration

```bash
# Generate platform-specific configs
pheno-vendor generate-hooks --platform vercel
pheno-vendor generate-hooks --platform docker --output build.sh
```

### Python API

```python
from pheno_deploy_kit import PhenoVendor

# Vendor packages
vendor = PhenoVendor(project_root=".")
vendor.vendor_all(auto_detect=True, validate=True)

# Generate configs
from pheno_deploy_kit import DeployConfig
config = DeployConfig(project_root=".")
config.save_configs()  # Creates vercel.json, Dockerfile, etc.
```

## CLI Commands

### `pheno-vendor setup`
Vendor pheno-sdk packages for production deployment.

```bash
pheno-vendor setup                    # Auto-detect packages
pheno-vendor setup --no-auto-detect   # Vendor all packages
pheno-vendor setup --no-validate      # Skip validation
```

### `pheno-vendor validate`
Validate vendored packages.

```bash
pheno-vendor validate                 # Basic validation
pheno-vendor validate --test-imports  # Include import tests
```

### `pheno-vendor info`
Show project and package information.

```bash
pheno-vendor info
```

### `pheno-vendor clean`
Remove vendored packages directory.

```bash
pheno-vendor clean
```

### `pheno-vendor generate-hooks`
Generate platform-specific build hooks.

```bash
pheno-vendor generate-hooks --platform vercel
pheno-vendor generate-hooks --platform docker --output build.sh
```

### `pheno-vendor install-hooks`
Install git pre-push hook for automatic vendoring.

```bash
pheno-vendor install-hooks
pheno-vendor install-hooks --force  # Overwrite existing
```

## NVMS Format Support

NVMS (Node Version Manager Script) is a universal deployment configuration format:

```python
from pheno_deploy_kit import NVMSParser

# Parse .nvms file
parser = NVMSParser(Path(".nvms"))
versions = parser.parse()

# Get specific versions
node_version = parser.get_node_version()
npm_version = parser.get_node_version()
```

Example `.nvms` file:
```
node=18.17.0
npm=9.6.7
python=3.10.12
```

## Platform Support

### Vercel
```json
// Auto-generated vercel.json
{
  "version": 2,
  "builds": [
    {
      "src": "server.py",
      "use": "@vercel/python"
    }
  ],
  "env": {
    "PYTHONPATH": "pheno_vendor"
  }
}
```

### Docker
```dockerfile
# Auto-generated Dockerfile
FROM python:3.10-slim
WORKDIR /app

RUN pip install pheno-deploy-kit
COPY . /app/
RUN pheno-vendor setup --no-validate
RUN pip install -r requirements-prod.txt

ENV PYTHONPATH=/app/pheno_vendor
CMD ["python", "server.py"]
```

### AWS Lambda
```bash
# Auto-generated build script
pip install pheno-deploy-kit -t package/
pheno-vendor setup --project-root package/
zip -r deployment.zip package/
```

## API Reference

### PhenoVendor

Main class for vendoring pheno-sdk packages.

```python
from pheno_deploy_kit import PhenoVendor

vendor = PhenoVendor(
    project_root=Path.cwd(),
    pheno_sdk_root=None,  # Auto-detect
    vendor_dir="pheno_vendor"
)

# Detect used packages
used = vendor.detect_used_packages()

# Vendor packages
results = vendor.vendor_packages(
    packages=None,  # None = auto-detect
    auto_detect=True,
    clean=True
)

# Validate
validation = vendor.validate_vendored()
import_tests = vendor.test_imports()

# All-in-one
vendor.vendor_all(auto_detect=True, validate=True)
```

### DeployConfig

Configuration management for deployment platforms.

```python
from pheno_deploy_kit import DeployConfig

config = DeployConfig(project_root=".")

# Auto-detected properties
config.python_version  # "3.10"
config.entry_point     # "server.py"
config.pheno_packages  # Set of pheno-sdk packages
config.external_deps   # Set of external dependencies

# Generate platform configs
vercel_config = config.to_vercel_config()
dockerfile = config.to_docker_config()
lambda_config = config.to_lambda_config()
railway_config = config.to_railway_config()

# Save all configs
config.save_configs()  # Creates vercel.json, Dockerfile, etc.
```

### PlatformDetector

Auto-detect deployment platform.

```python
from pheno_deploy_kit import PlatformDetector

detector = PlatformDetector(project_root=".")

# Detect primary platform
platform = detector.detect()  # "vercel", "docker", etc.

# Get all detected platforms
platforms = detector.detect_all()
for p in platforms:
    print(f"{p.name}: {p.confidence:.0%}")
```

### BuildHookGenerator

Generate platform-specific build hooks.

```python
from pheno_deploy_kit import BuildHookGenerator

generator = BuildHookGenerator(project_root=".")

# Generate hooks for platform
hooks = generator.generate("vercel")
print(hooks)

# Save to file
(Path.cwd() / "build.sh").write_text(hooks)
```

### DeploymentValidator

Validate deployment readiness.

```python
from pheno_deploy_kit import DeploymentValidator

validator = DeploymentValidator(project_root=".")

# Validate configuration
success, errors = validator.validate()
if not success:
    for error in errors:
        print(f"Error: {error}")

# Test imports
success, errors = validator.check_imports()
```

### Health Checks

```python
from pheno_deploy_kit import HTTPHealthCheck, PortHealthCheck, HealthChecker

# HTTP health check
http_check = HTTPHealthCheck(
    url="http://localhost:8000/health",
    expected_status=200,
    timeout=5.0
)
result = await http_check.run()

# TCP port health check
tcp_check = PortHealthCheck(
    host="localhost",
    port=5432,
    timeout=3.0
)
result = await tcp_check.run()

# Health checker manager
checker = HealthChecker()
checker.add_check(http_check)
checker.add_check(tcp_check)
results = await checker.run_all()
```

### Local Service Management

```python
from pheno_deploy_kit import LocalServiceManager, LocalProcessConfig, ReadyProbe

# Configure service
config = LocalProcessConfig(
    command=["python", "app.py"],
    cwd=Path("./myapp"),
    env={"DEBUG": "false"},
    name="api-server",
    ready_probe=ReadyProbe(
        check=lambda: check_port_open(8000)
    )
)

# Start service
manager = LocalServiceManager()
await manager.start([config])

# Stream logs
manager.stream_logs(prefix=True)

# Stop service
await manager.stop()
```

## Use Cases

### 1. Production Deployment (Vercel)

```bash
# Setup
pheno-vendor setup

# Deploy
vercel deploy
```

### 2. Docker Containerization

```bash
# Generate Dockerfile
python -c "from pheno_deploy_kit import DeployConfig; \
           print(DeployConfig('.').to_docker_config())" > Dockerfile

# Build
docker build -t myapp .
docker run myapp
```

### 3. AWS Lambda Package

```bash
# Vendor and package
pheno-vendor setup
pip install -r requirements-prod.txt -t package/
cd package && zip -r ../deployment.zip .
```

### 4. CI/CD Integration

```yaml
# .github/workflows/deploy.yml
jobs:
  deploy:
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
      - name: Vendor packages
        run: |
          pip install pheno-deploy-kit
          pheno-vendor setup
      - name: Deploy
        run: vercel deploy --prod
```

### 5. Multi-Platform Build

```python
from pheno_deploy_kit import DeployConfig

config = DeployConfig(".")

# Generate for all platforms
config.save_configs()  # Creates vercel.json, Dockerfile, railway.json, etc.
```

## Architecture

```
pheno-deploy-kit/
├── src/pheno_deploy_kit/
│   ├── __init__.py          # Package exports and health check classes
│   ├── vendor.py            # PhenoVendor - Vendoring engine
│   ├── config.py            # DeployConfig - Configuration management
│   ├── utils.py             # Platform detection, hooks, validation
│   ├── cli.py               # CLI interface (pheno-vendor)
│   ├── checks.py            # Vendor freshness checking
│   ├── hooks.py             # Git hook logic
│   ├── install_hooks.py     # Git hook installation
│   ├── startup.py           # Startup checks
│   ├── local/               # Local process management
│   │   ├── __init__.py
│   │   └── manager.py
│   ├── nvms/                # NVMS format support
│   │   ├── __init__.py
│   │   └── parser.py
│   ├── platforms/           # Platform clients
│   │   ├── vercel/
│   │   ├── fly/
│   │   ├── cloud/
│   │   └── modern/
│   ├── cloud/               # Cloud provider interfaces
│   │   ├── types.py
│   │   ├── interfaces.py
│   │   ├── registry.py
│   │   └── errors.py
│   └── docker/              # Docker integration
│       └── __init__.py
├── pyproject.toml
└── README.md
```

## Requirements

- Python >= 3.10
- Dependencies:
  - `httpx` - HTTP client
  - `pydantic` - Data validation
  - `pyyaml` - YAML support
  - `rich` - Terminal UI
  - `click` - CLI framework

Optional dependencies:
- `boto3` - AWS support
- `docker` - Docker integration
- `kubernetes` - K8s support
- Platform-specific SDKs (see pyproject.toml)

## Development

```bash
# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/

# Format code
ruff format src/
ruff check src/

# Type check
mypy src/
```

## Troubleshooting

### Package Not Found
```bash
# Specify pheno-sdk location
export PHENO_SDK_ROOT=/path/to/pheno-sdk
pheno-vendor setup
```

### Import Errors
```bash
# Validate vendored packages
pheno-vendor validate --test-imports

# Check Python path
export PYTHONPATH=pheno_vendor
```

### Build Issues
```bash
# Skip validation for faster builds
pheno-vendor setup --no-validate

# Clean and retry
pheno-vendor clean
pheno-vendor setup
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - See LICENSE for details

## Support

- **Documentation**: This README and source docstrings
- **CLI Help**: `pheno-vendor --help`
- **Issues**: GitHub Issues

## Roadmap

- [ ] PyPI package publication
- [ ] More platform integrations (Cloudflare Workers, Netlify, etc.)
- [ ] Dependency optimization (tree-shaking)
- [ ] Cache optimization for CI/CD
- [ ] GUI for configuration
- [ ] Integration with cloud provider APIs

---

**Extracted from phenoSDK** - Now a standalone package in ResilienceKit
