# US-001: Directory Reorganization & Update Backlog Policy

**Date**: 2026-04-10  
**Author**: Architecture Team  
**Type**: refactor  
**Status**: implemented  
**Related**:
  - .docs/DEVELOPER_AGENT_QUALITY_MANDATE.md
  - update-backlog/README.md

---

## Summary

Reorganized project documentation and guides into purpose-specific directories for better information architecture. Introduced update-backlog system with version-controlled MD summaries using `US-NNN-context-a-context-b` naming scheme.

---

## What Changed

### New Directory Structure

#### 1. **system-guides/** (New)
Moved user-facing guides and documentation:
- `CONFIGURATION_GUIDE.md` – How to set up and use configuration system
- `DEVELOPMENT_PIPELINE_SUMMARY.md` – High-level system overview
- `QUICK_REFERENCE.md` – Printable developer reference card

**Purpose**: Single location for all developer onboarding and reference material

#### 2. **project-management/** (New)
Moved internal documentation and agent prompts:
- `[internal] SPEC_PACKAGING_AGENT_PROMPT.md` – Specification packaging rules
- `[internal] SPEC_TO_TASK_MARKDOWN_AGENT.txt` – Task extraction rules
- `[internal] STAKEHOLDER_BOARD_SCOPE_AGENT.txt` – Scope reduction rules
- `[internal] STAKEHOLDER_DEVELOPER_AGENT.txt` – Quality enforcement rules

**Purpose**: Centralized location for architectural directives and internal processes

#### 3. **update-backlog/** (New)
Version-controlled summaries of major updates:
- `README.md` – Update backlog policy and conventions
- `US-000-utils-migration.md` – Utils directory migration update
- `US-001-directory-reorganization.md` – This update

**Purpose**: Queryable, git-friendly log of project changes without heavyweight tools

### Updates to .docs/

**Remains in .docs/** (Core Governance):
- `DEVELOPER_AGENT_QUALITY_MANDATE.md` – 7 pillars of quality (core standard)
- `QUALITY_INTEGRATION_SUMMARY.md` – Quality integration documentation
- `SCOPE_REDUCTION_SUMMARY.md` – Scope reduction decisions
- `REDUCTION_NOTES.md` – Scope change log
- `project-breakdown.md` – Architecture and implementation guide

**Removed from .docs/** (Moved to system-guides/):
- ~~CONFIGURATION_GUIDE.md~~ → system-guides/
- ~~DEVELOPMENT_PIPELINE_SUMMARY.md~~ → system-guides/
- ~~QUICK_REFERENCE.md~~ → system-guides/

**Removed from .docs/** (Moved to project-management/):
- ~~[internal] *.md~~ → project-management/

**Moved from .docs/** (To update-backlog/):
- ~~UTILS_MIGRATION_GUIDE.md~~ → update-backlog/US-000-utils-migration.md

---

## Why

### Information Architecture

**Separation of Concerns**:
- **Core Governance (.docs/)**: Quality mandate, scope decisions, architecture
- **System Guides (system-guides/)**: How-to guides, onboarding, reference
- **Project Management (project-management/)**: Internal processes, agent directives
- **Update Backlog (update-backlog/)**: Change history, version control

**Benefits**:
- Developers find guides in one place
- Architects find policies in one place
- Changes are trackable and queryable
- Git history becomes meaningful documentation

### Update Backlog Policy

**Purpose**: Track significant changes without heavyweight version control tools

**Advantages**:
- Simple MD files, easy to read and grep
- Sequential IDs make chronological tracking easy
- Git commits directly reference changes
- Queryable by context (utils, quality, config, etc.)
- Future-proof: works with any VCS

---

## Impact

### For Developers

✅ **Improved Navigation**:
- System guides in one place (system-guides/)
- Quick reference card available (system-guides/QUICK_REFERENCE.md)
- Configuration help readily available

⚠️ **Import Changes** (if applicable):
- No direct impact on code imports
- Documentation URLs change (see File Mapping below)

### For Architects

✅ **Organized Processes**:
- Internal directives in project-management/
- Change log in update-backlog/
- Easy to audit decisions and processes

✅ **Version Control**:
- Each update is a single commit
- Git log shows change history
- Queryable by file or context

### For System

✅ **Settings Protection**:
- All new directories are protected
- Modifications require change logs
- Access control enforced by .claude/settings.json

---

## Implementation

### File Mapping

| Old Path | New Path | Type |
|----------|----------|------|
| .docs/CONFIGURATION_GUIDE.md | system-guides/CONFIGURATION_GUIDE.md | Move |
| .docs/DEVELOPMENT_PIPELINE_SUMMARY.md | system-guides/DEVELOPMENT_PIPELINE_SUMMARY.md | Move |
| .docs/QUICK_REFERENCE.md | system-guides/QUICK_REFERENCE.md | Move |
| .docs/[internal] *.md | project-management/ | Move |
| .docs/UTILS_MIGRATION_GUIDE.md | update-backlog/US-000-utils-migration.md | Move + Rename |
| .docs/DEVELOPER_AGENT_QUALITY_MANDATE.md | .docs/ | Stays |
| .docs/project-breakdown.md | .docs/ | Stays |
| .docs/SCOPE_REDUCTION_SUMMARY.md | .docs/ | Stays |

### Directory Creation

```bash
mkdir -p system-guides/
mkdir -p project-management/
mkdir -p update-backlog/
```

### File Moves

```bash
# Copy guides to system-guides/
cp .docs/CONFIGURATION_GUIDE.md system-guides/
cp .docs/DEVELOPMENT_PIPELINE_SUMMARY.md system-guides/
cp .docs/QUICK_REFERENCE.md system-guides/

# Copy internal docs to project-management/
cp .docs/[internal]*.md project-management/
cp .docs/[internal]*.txt project-management/

# Move utils migration to update-backlog with new name
cp .docs/UTILS_MIGRATION_GUIDE.md update-backlog/US-000-utils-migration.md
```

### Update References

Update documentation links:
- References to CONFIGURATION_GUIDE → system-guides/CONFIGURATION_GUIDE.md
- References to DEVELOPMENT_PIPELINE_SUMMARY → system-guides/DEVELOPMENT_PIPELINE_SUMMARY.md
- References to QUICK_REFERENCE → system-guides/QUICK_REFERENCE.md

---

## Files Affected

### Moved Files
- system-guides/CONFIGURATION_GUIDE.md (moved from .docs/)
- system-guides/DEVELOPMENT_PIPELINE_SUMMARY.md (moved from .docs/)
- system-guides/QUICK_REFERENCE.md (moved from .docs/)
- project-management/[internal] *.md (moved from .docs/)
- project-management/[internal] *.txt (moved from .docs/)
- update-backlog/US-000-utils-migration.md (moved from .docs/UTILS_MIGRATION_GUIDE.md)

### New Files
- update-backlog/README.md (update backlog policy)
- update-backlog/US-001-directory-reorganization.md (this document)

### Modified Files
- .claude/settings.json (updated protected paths)

### Reference Updates Needed
- Any internal links to moved files should be updated
- Documentation referencing old paths should point to new locations

---

## Verification

### Directory Structure

```bash
# Verify directories exist
ls -d system-guides/
ls -d project-management/
ls -d update-backlog/

# Verify files moved
ls system-guides/*.md
ls project-management/
ls update-backlog/US-*.md
```

### Settings Protection

```bash
# Verify settings.json is valid
python -c "import json; json.load(open('.claude/settings.json')); print('✓ Valid')"

# Verify protected paths
grep -A5 '"protected"' .claude/settings.json
```

### Documentation Links

```bash
# Check for broken references
grep -r "CONFIGURATION_GUIDE" .
grep -r "QUICK_REFERENCE" .

# Should all point to system-guides/ now
```

---

## Update Backlog Policy

### Naming Convention

New update summaries use: `US-NNN-context-a-context-b.md`

**Pattern**: Update Summary ID (3 digits) + Context A (primary) + Context B (secondary)

**Examples**:
- US-001-directory-reorganization.md
- US-002-quality-enforcement.md
- US-003-config-expansion.md

### Usage

Each significant change gets a summary:

```bash
# Create
touch update-backlog/US-NNN-[context-a]-[context-b].md

# Fill with template (see update-backlog/README.md)

# Commit
git add update-backlog/
git commit -m "US-NNN: [Brief title]

[Bullet points of changes]

See update-backlog/US-NNN-[context].md for full details."
```

### Current Status

| ID | Title | Status |
|----|-------|--------|
| 000 | Utils Migration | implemented |
| 001 | Directory Reorganization | implemented |
| 002+ | [Next updates...] | pending |

---

## References

- Update Backlog Policy: update-backlog/README.md
- Previous: US-000-utils-migration.md
- Quality Mandate: .docs/DEVELOPER_AGENT_QUALITY_MANDATE.md
- Settings Policy: .claude/settings.json

---

## Related Changes

This update pairs with:
- **US-000**: Utils directory migration
- **Settings.json**: Now protects 6 directories and 4 patterns
- **Access Control**: All directories require change logs for modifications

---

**Status**: ✅ Implemented  
**Date**: 2026-04-10  
**Author**: Architecture Team
