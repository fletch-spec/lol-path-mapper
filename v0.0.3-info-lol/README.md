# The Summoner's Chronicle (info-lol)

**A Post-Game Champion-Centric Analysis Infographic for League of Legends**

---

## Project Overview

**Repository:** info-lol  
**Current Version:** 0.0.3  
**Status:** Active Development — Core Infrastructure Phase  
**Release Date:** 2026-04-10

The Summoner's Chronicle is a data visualization system that transforms League of Legends post-game statistics into narrative-driven, visually compelling stories. The project focuses on champion-centric analysis with seven integrated information zones.

---

## Quick Start

### Prerequisites
- Python 3.13+
- Git
- Development configuration (see `development.cfg`)

### Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/info-lol.git
cd info-lol

# Create local configuration (optional)
cp development.cfg.local.example development.cfg.local

# Run tests
python -m pytest utils/tests/ --cov=utils --cov-fail-under=80

# View available utilities
python -m utils.task_parser    # Show tasks with Rich formatting
python -m utils.task_walk      # Walk entire project and list all tasks
```

---

## Project Structure

```
info-lol/
├── spec.md                     # Complete product specification
├── PROJECT_STRUCTURE.md        # Architecture and organization guide
├── development.cfg             # Configuration template
├── development.cfg.local       # Local overrides (not committed)
├── VERSION                     # Current version: 0.0.3
│
├── .docs/                      # Governance and system documentation
│   ├── DEVELOPER_AGENT_QUALITY_MANDATE.md
│   ├── PYTHON_ORGANIZATION_POLICY.md
│   ├── VERSION_POLICY.md       # Release and versioning process
│   ├── system-guides/          # Developer guides
│   ├── project-management/     # Agent directives and specs
│   └── update-backlog/         # Version-controlled change log
│
├── packages/                   # Product specifications and task definitions
│   ├── tasks.md                # Global project tasks (8 tasks)
│   ├── infrastructure/         # Core infrastructure packages
│   ├── visual-design/          # UI/UX zones (7 zones)
│   ├── statistics-and-algorithms/  # Data processing
│   └── overview/               # System overview
│
└── utils/                      # Python utilities and infrastructure
    ├── config_loader.py        # Configuration management
    ├── markdown_printer.py      # Rich markdown viewer
    ├── task_parser.py           # Task display utility
    ├── task_walk.py             # Project-wide task discovery
    └── tests/                   # Comprehensive test suites
        ├── test_config_loader.py
        ├── test_markdown_printer.py
        ├── test_task_parser.py
        └── test_task_walk.py
```

---

## Key Utilities

### Task Parser
Display project tasks with Rich formatting:

```bash
python -m utils.task_parser
```

Shows all 8 global tasks organized by role, with effort estimates and quality mandate status.

### Task Walk
Discover and display all tasks throughout the project:

```bash
python -m utils.task_walk
```

Recursively finds all tasks.md files across packages/ and organizes them by role, department, or milestone. Displays 144+ tasks with verbose details.

### Markdown Printer
View .md files with Rich formatting and syntax highlighting:

```bash
python -m utils.markdown_printer spec.md
```

### Config Loader
Load and manage configuration with environment variable overrides:

```python
from utils.config_loader import Config
config = Config("development.cfg")
version = config.get("PROJECT_VERSION")
```

---

## Version Information

**Current Version:** 0.0.3  
**Versioning Scheme:** RELEASE.VERSION.PATCH (Semantic Versioning 2.0.0)

- **RELEASE (0):** Major product release cycle
- **VERSION (0):** Feature-complete milestone
- **PATCH (3):** Incremental improvements and bug fixes

For detailed versioning policy, see [.docs/VERSION_POLICY.md](.docs/VERSION_POLICY.md)

### Planned Releases

- **0.0.4**: Task state tracking utility
- **0.0.5**: Build system and CI/CD setup
- **0.1.0**: MVP feature freeze (first feature-complete version)
- **1.0.0**: First major production release

---

## Quality Standards

This project enforces **Seven Pillars of Code Quality**:

1. **Docstrings & Comments** — All modules, functions, classes documented
2. **Error Handling** — Explicit handling for all external operations
3. **Test Coverage** — Minimum 80% code coverage, 90% critical paths
4. **Code Structure** — Functions ≤50 lines, modules ≤10 functions
5. **Configuration** — No hardcoded values, externalize all settings
6. **Logging & Diagnostics** — Comprehensive logging and error reporting
7. **Initialization Tests** — Verify imports and component instantiation

For details, see [.docs/DEVELOPER_AGENT_QUALITY_MANDATE.md](.docs/DEVELOPER_AGENT_QUALITY_MANDATE.md)

---

## Development Workflow

### Before Committing

```bash
# Run all tests
python -m pytest utils/tests/ -v

# Check coverage
python -m pytest utils/tests/ --cov=utils

# View project tasks
python -m utils.task_parser      # Global tasks
python -m utils.task_walk        # All project tasks
```

### Commit Message Format

```
type: brief description (max 50 chars)

Detailed explanation:
- What changed
- Why it changed
- Any implications
```

Types: `chore`, `feat`, `fix`, `docs`, `refactor`, `test`

### Pushing Changes

Protected branch policies require:
- All tests passing (80%+ coverage)
- No hardcoded configuration values
- Proper commit message format
- No stray temporary files

---

## Documentation

### For Developers
- [CONFIGURATION_GUIDE.md](.docs/system-guides/CONFIGURATION_GUIDE.md) — Config system
- [DEVELOPMENT_PIPELINE_SUMMARY.md](.docs/system-guides/DEVELOPMENT_PIPELINE_SUMMARY.md) — Development process
- [QUICK_REFERENCE.md](.docs/system-guides/QUICK_REFERENCE.md) — Common commands

### For Product Managers
- [spec.md](spec.md) — Complete feature specification
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) — Architecture overview
- [.docs/project-breakdown.md](.docs/project-breakdown.md) — Detailed scope breakdown

### For Quality Assurance
- [DEVELOPER_AGENT_QUALITY_MANDATE.md](.docs/DEVELOPER_AGENT_QUALITY_MANDATE.md) — Quality standards
- [VERSION_POLICY.md](.docs/VERSION_POLICY.md) — Release and versioning
- [PYTHON_ORGANIZATION_POLICY.md](.docs/PYTHON_ORGANIZATION_POLICY.md) — Code organization

---

## Contributing

To contribute to this project:

1. Follow [PYTHON_ORGANIZATION_POLICY.md](.docs/PYTHON_ORGANIZATION_POLICY.md)
2. Ensure code meets [DEVELOPER_AGENT_QUALITY_MANDATE.md](.docs/DEVELOPER_AGENT_QUALITY_MANDATE.md)
3. Write tests for all new code (80%+ coverage)
4. Document public APIs with docstrings
5. Update [.docs/update-backlog/](.docs/update-backlog/) with change summary (US-NNN format)

---

## License

[Your License Here]

---

## Contact

**Project Lead:** [Your Name]  
**Questions?** See [.docs/](.docs/) directory for governance and development guidance.

---

**Last Updated:** 2026-04-10  
**Status:** ✅ Core infrastructure ready for initial commit
