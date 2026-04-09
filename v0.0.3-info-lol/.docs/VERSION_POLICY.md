# Version Policy — The Summoner's Chronicle

**Current Release:** `0.0.3`  
**Last Updated:** 2026-04-10

---

## Versioning Scheme

The Summoner's Chronicle follows **Semantic Versioning 2.0.0** with three version components:

```
RELEASE.VERSION.PATCH
  ↓        ↓       ↓
  0.0.3 (current development)
```

### Component Definitions

- **RELEASE** (0): Major product release cycle
  - Increments on significant architectural changes or product overhaul
  - Example: Release 1.x.x would represent a second major iteration
  - Current: `0` (pre-release/alpha state)

- **VERSION** (0): Feature-complete milestone within a release
  - Increments when substantial new features ship
  - Example: 0.1.0 would be the first feature-complete version
  - Current: `0` (still in core feature development)

- **PATCH** (3): Incremental improvements, bug fixes, refinements
  - Increments for polish, optimization, and corrections
  - Example: 0.0.4 adds task_walk utility, improves performance, etc.
  - Current: `3` (three patches into core development)

---

## Version Lifecycle

### Current State: 0.0.3 (Development)

**Status:** Active Development  
**Phase:** Core Infrastructure & Utilities

**What's Included:**
- Product specification (spec.md)
- 144 documented project tasks
- 4 Python utilities (config_loader, markdown_printer, task_parser, task_walk)
- Comprehensive governance and quality policies
- Development configuration system
- Claude Code integration and settings

**What's Planned:**
- 0.0.4: Task state tracking utility
- 0.0.5: Build system and CI/CD setup
- 0.1.0: MVP feature freeze (first feature-complete version)

---

## Release Process

### Patch Release (0.0.x → 0.0.x+1)

**Trigger:** When ready to commit improvements and utilities

**Steps:**
1. Run full test suite: `pytest utils/tests/ --cov=utils --cov-fail-under=80`
2. Update PATCH number in:
   - `.docs/VERSION_POLICY.md` (this file)
   - `development.cfg` (PROJECT_VERSION setting)
   - `spec.md` (version reference)
3. Create git tag: `git tag -a v0.0.x -m "Release version 0.0.x"`
4. Push: `git push origin master && git push origin --tags`

### Minor Release (0.x → 0.x+1)

**Trigger:** When first complete feature set ships

**Steps:**
1. Feature freeze: no new features accepted
2. Run full test suite and documentation check
3. Update VERSION number in all files above
4. Create release branch: `git checkout -b release/0.1.0`
5. Final testing and bug fixes
6. Merge to master with tag: `git tag -a v0.1.0`
7. Announce: Update status in project documentation

### Major Release (x → x+1)

**Trigger:** Architectural overhaul or product redesign

**Steps:** Same as Minor Release, plus:
- Update RELEASE number (currently 0)
- Reset VERSION to 0
- Reset PATCH to 0
- Result: e.g., v1.0.0

---

## Version File Management

### Configuration Files

**Location:** `development.cfg`

```ini
[metadata]
PROJECT_VERSION = 0.0.3
VERSION_DATE = 2026-04-10
VERSION_STAGE = development
```

Update this after each release.

### Documentation References

The following files should always reference the current version:

- `.docs/VERSION_POLICY.md` — This file (update "Current Release")
- `spec.md` — Product specification header
- `.docs/QUALITY_INTEGRATION_SUMMARY.md` — Project summary
- `.docs/system-guides/*.md` — Configuration and pipeline docs

### Automated Version Checking

In future releases, implement version checking in utilities:

```python
# utils/__init__.py
__version__ = "0.0.3"
__release_date__ = "2026-04-10"

# Load from config
from utils.config_loader import Config
config = Config("development.cfg")
current_version = config.get("PROJECT_VERSION")
```

---

## Branching Strategy for Releases

### Development Branch

- **Branch:** `master` (default)
- **Purpose:** Active development, new utilities, fixes
- **Version State:** Always 0.0.x (patch versions only)
- **Policy:** All commits must pass quality checks

### Release Branches

- **Branch:** `release/0.1.0` (created per minor version)
- **Purpose:** Final testing, bug fixes, release preparation
- **Version State:** Frozen (e.g., 0.1.0)
- **Policy:** Only critical fixes accepted

### Tags

Create annotated tags for all releases:

```bash
git tag -a v0.0.3 -m "Release version 0.0.3: Core infrastructure and utilities"
git tag -a v0.1.0 -m "Release version 0.1.0: MVP feature freeze"
git tag -a v1.0.0 -m "Release version 1.0.0: First major release"
```

---

## Milestone Alignment

Project milestones map to version numbers:

| Milestone | Version | Status | Notes |
|-----------|---------|--------|-------|
| Infrastructure | 0.0.x | Current | Core utilities, config, quality policies |
| MVP (Phase 1) | 0.1.0 | Planned | First feature-complete version |
| Polish (Phase 2) | 0.2.0 | Planned | Refinement and optimization |
| Compliance | 0.3.0 | Planned | Security and accessibility hardening |
| Production | 1.0.0 | Future | First major release to production |

---

## Breaking Changes Policy

**Breaking Changes** (warrant VERSION increment to 0.x.0):

- Removing public utilities or changing their API
- Changing configuration file format in incompatible way
- Modifying core governance policies in ways that require workflow updates
- Database schema changes (when applicable)

**Non-Breaking Changes** (warrant PATCH increment to 0.0.x):

- Adding new utilities without modifying existing ones
- Enhancing configuration with new optional settings
- Bug fixes and performance improvements
- Documentation updates
- Adding new tests or improving test coverage

---

## Version Communication

### In Code

Always include current version in module docstrings:

```python
"""Task parser utility for displaying project tasks with Rich formatting.

Version: 0.0.3
Status: Development
"""
```

### In Documentation

Include version in headers:

```markdown
# Configuration Guide

**Project:** The Summoner's Chronicle  
**Version:** 0.0.3  
**Last Updated:** 2026-04-10
```

### In Git

Use semantic version tags:

```bash
git tag -l
v0.0.3
v0.0.4
v0.1.0
v1.0.0
```

---

## Next Steps

**For Patch Release (0.0.4):**

1. ✅ Complete any pending utilities
2. ✅ Ensure all tests pass (80%+ coverage)
3. ⬜ Update PATCH to 0.0.4 in all files
4. ⬜ Create commit: `chore: bump version to 0.0.4`
5. ⬜ Tag: `git tag -a v0.0.4 -m "Release version 0.0.4"`
6. ⬜ Push to remote

**For Minor Release (0.1.0):**

1. ⬜ Feature freeze: no new features after this point
2. ⬜ Update VERSION to 0.1.0 in all files
3. ⬜ Create release branch: `git checkout -b release/0.1.0`
4. ⬜ Final test pass and bug fixes
5. ⬜ Merge back to master with tag

---

## Policy Enforcement

This version policy is enforced via:

- **Git Hooks:** Pre-push checks verify version consistency
- **CI/CD:** Release pipeline validates version numbers match
- **Manual Review:** Maintainers verify version bumps follow this policy

Questions about versioning? Refer to this document or contact the project maintainers.
