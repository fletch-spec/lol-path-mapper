# League of Legends Data Analysis

A League of Legends post-game analysis and visualization toolkit. This project explores champion-centric data analysis and infographic generation from game replays.

**Status**: Experimental | **Active Development**: v0.0.3

---

## Project Structure

The repository is organized into distinct versions and experimental modules:

### `v0.0.3-info-lol/` – Current Active Project
The main development branch. "The Summoner's Chronicle" — a data visualization system for post-game champion analysis.

**What's implemented:**
- Markdown-based project planning and task management
- Python utility modules (config management, task parsing)
- Core governance documents and quality standards
- Complete specification and architecture documentation
- Automated testing framework with 80%+ coverage requirements

**Key directories:**
- `.docs/` — Core governance, quality mandates, scope decisions
- `system-guides/` — Developer onboarding and reference guides
- `packages/` — Detailed specifications and task definitions (~150 tasks)
- `utils/` — Reusable Python utilities
- `update-backlog/` — Version-controlled change summaries (US-* format)

### `champion_renders/` – Experimental Module
Standalone exploration of champion template rendering and visualization. Not integrated into the main project; used for experimenting with new rendering approaches.

### Development Versions (Reference)

#### `v0.0.1/` — Initial Commit
The baseline version. Represents the starting point of the project with original architecture and approach.

#### `v0.0.2/` — Testing Structure
Experimental version exploring test structure and function organization. Some modules are partial or incomplete. Kept as reference for architectural decisions.

---

## Getting Started

### Explore the Current Project

Start with the comprehensive documentation in `v0.0.3-info-lol/`:

```bash
# View project structure and architecture
cat v0.0.3-info-lol/PROJECT_STRUCTURE.md

# Start with configuration setup
cat v0.0.3-info-lol/.docs/system-guides/CONFIGURATION_GUIDE.md

# Check quality standards
cat v0.0.3-info-lol/.docs/DEVELOPER_AGENT_QUALITY_MANDATE.md
```

### Understand the Project

1. **For Architecture**: Read `v0.0.3-info-lol/.docs/system-guides/DEVELOPMENT_PIPELINE_SUMMARY.md`
2. **For Specifications**: Browse `v0.0.3-info-lol/packages/` directory
3. **For Recent Changes**: Check `v0.0.3-info-lol/update-backlog/`
4. **For Quick Reference**: Use `v0.0.3-info-lol/.docs/system-guides/QUICK_REFERENCE.md`

---

## Useful Links

### Developer Guides
- **[System Guides Index](v0.0.3-info-lol/.docs/system-guides/README.md)** — Developer resources and navigation
- **[Configuration Guide](v0.0.3-info-lol/.docs/system-guides/CONFIGURATION_GUIDE.md)** — Setup and configuration
- **[Development Pipeline](v0.0.3-info-lol/.docs/system-guides/DEVELOPMENT_PIPELINE_SUMMARY.md)** — System overview and architecture
- **[Quick Reference](v0.0.3-info-lol/.docs/system-guides/QUICK_REFERENCE.md)** — Developer cheat sheet

### Governance & Standards
- **[Quality Mandate](v0.0.3-info-lol/.docs/DEVELOPER_AGENT_QUALITY_MANDATE.md)** — 7 pillars of code quality
- **[Scope Summary](v0.0.3-info-lol/.docs/SCOPE_REDUCTION_SUMMARY.md)** — What's in/out of scope
- **[Python Organization](v0.0.3-info-lol/.docs/PYTHON_ORGANIZATION_POLICY.md)** — Code organization standards

### Specifications & Tasks
- **[Project Structure](v0.0.3-info-lol/PROJECT_STRUCTURE.md)** — Complete directory organization and file purposes
- **[Specifications](v0.0.3-info-lol/packages/)** — Detailed feature specs organized by domain
- **[Change History](v0.0.3-info-lol/update-backlog/)** — Version-controlled update summaries

### Documentation Hub
- **[Documentation Index](v0.0.3-info-lol/.docs/README.md)** — Navigation hub for all documentation

---

## Project Evolution

This repository represents an experimental journey through multiple implementation approaches:

- **v0.0.1**: Original architecture and approach (reference baseline)
- **v0.0.2**: Testing structure exploration and refinement
- **v0.0.3**: Current mature approach with robust governance, comprehensive documentation, and quality-first infrastructure
- **champion_renders**: Parallel experiments in visualization rendering

Each version serves as a learning checkpoint and architectural reference point. The project is actively developed in `v0.0.3-info-lol/`.

---

## Quick Stats

| Metric | Details |
|--------|---------|
| **Active Version** | 0.0.3 |
| **Governance Docs** | 6+ files |
| **System Guides** | 3 comprehensive guides |
| **Specifications** | 36+ specification files |
| **Tasks** | ~150 tracked tasks |
| **Code Coverage Target** | 80%+ |
| **Testing Framework** | Pytest + comprehensive suites |

---

## Development Notes

- All protected files require change summaries in the `update-backlog/` directory using the `US-NNN` format
- Quality enforcement via 7 Pillars: Docstrings, Error Handling, Test Coverage, Code Structure, Configuration, Logging, and Initialization Tests
- Python organization follows strict patterns defined in `PYTHON_ORGANIZATION_POLICY.md`
- Configuration is externalized through `development.cfg` with local overrides

---

**Last Updated**: 2026-04-10  
**Maintained By**: Fletcher  
**Current Branch**: package-lol-maps
