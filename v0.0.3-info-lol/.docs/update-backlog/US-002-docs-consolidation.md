# US-002: Documentation Consolidation & Python Organization Policy

**Date**: 2026-04-10  
**Author**: Architecture Team  
**Type**: refactor  
**Status**: implemented  
**Related**:
  - .docs/PYTHON_ORGANIZATION_POLICY.md
  - .claude/settings.json
  - PROJECT_STRUCTURE.md

---

## Summary

Consolidated all documentation into `.docs/` directory by moving project-management/, system-guides/, and update-backlog/ subdirectories into `.docs/`. Established Python organization policy: no Python files in main root except `__main__.py`, all utilities in `utils/`. Updated access control policy accordingly.

---

## What Changed

### Directory Reorganization

#### Moved Into .docs/

```
.docs/
├── project-management/          ← Moved from root
│   ├── README.md
│   └── [internal] *.txt/*.md
├── system-guides/               ← Moved from root
│   ├── README.md
│   ├── CONFIGURATION_GUIDE.md
│   ├── DEVELOPMENT_PIPELINE_SUMMARY.md
│   └── QUICK_REFERENCE.md
└── update-backlog/              ← Moved from root
    ├── README.md
    ├── US-000-utils-migration.md
    └── US-001-directory-reorganization.md
```

#### Remains in .docs/

```
.docs/
├── DEVELOPER_AGENT_QUALITY_MANDATE.md
├── QUALITY_INTEGRATION_SUMMARY.md
├── SCOPE_REDUCTION_SUMMARY.md
├── REDUCTION_NOTES.md
├── project-breakdown.md
└── PYTHON_ORGANIZATION_POLICY.md (NEW)
```

### Root Directory After

```
C:\dev\league-of-legends\info-lol-v0.0.3\
├── .claude/
├── .docs/                       ← All documentation consolidated
├── packages/
├── utils/                       ← All Python utilities
├── development.cfg
├── PROJECT_STRUCTURE.md
└── [supporting files]
```

### New Policy: Python Organization

**Policy Document**: `.docs/PYTHON_ORGANIZATION_POLICY.md`

**Core Rule**: No Python files in main root directory except `__main__.py`

**Location**: All utility Python files go in `utils/`

**Enforcement**: 
- Pre-commit hook in settings.json
- Prevents *.py files in root (except __main__.py)
- All utilities must be in utils/

---

## Why

### Documentation Consolidation

**Benefits**:
- **Single location** for all docs (`.docs/`)
- **Clearer structure** – no scattered directories
- **Easier navigation** – one place to look for anything
- **Better organization** – core vs. guides vs. history clearly separated
- **Simpler paths** for references

### Python Organization Policy

**Benefits**:
- **Clean root** – only config, docs, and entry point
- **Clear imports** – all utilities from `utils/`
- **Scalable** – easy to add utilities without clutter
- **Maintainable** – single package to manage
- **Professional** – matches common Python project structure

---

## Impact

### For Developers

✅ **Simpler navigation**:
- All docs in `.docs/`
- All code in `utils/`
- One place to look for guides

✅ **Clearer imports**:
```python
from utils.config_loader import Config
from utils import initialize_config
```

### For Architecture

✅ **Better organization**:
- Root directory shows structure (docs + config only)
- Python code isolated in utils/
- Protected directories clear and minimal

✅ **Enforced standards**:
- Pre-commit hook prevents root Python files
- Settings.json protects `.docs/` and `utils/`
- Policy document explains why

### For File System

```
Before (scattered):
├── .docs/
├── system-guides/      ← Guide files here
├── project-management/ ← Internal docs here
├── update-backlog/     ← Change log here
└── config_loader.py    ← Python file in root (violates policy)

After (consolidated):
├── .docs/
│   ├── system-guides/
│   ├── project-management/
│   ├── update-backlog/
│   └── [core governance docs]
├── utils/
│   └── config_loader.py ← Python organized properly
```

---

## Implementation

### File Moves

```bash
# Moved into .docs/
cp -r project-management/ .docs/
cp -r system-guides/ .docs/
cp -r update-backlog/ .docs/

# Removed from root
rm -rf project-management/
rm -rf system-guides/
rm -rf update-backlog/
```

### Policy Created

- New file: `.docs/PYTHON_ORGANIZATION_POLICY.md`
- Explains: No Python files in root except __main__.py
- Defines: All utilities in utils/
- Enforces: Via settings.json hooks

### Settings Updated

- Protected `.docs/` (entire directory)
- Protected `*.py` in root (except __main__.py via hook)
- Simplified protectedPatterns (now unified under .docs/)
- Added Python file check in pre-commit hooks

---

## Files Affected

### Moved
- project-management/ → .docs/project-management/
- system-guides/ → .docs/system-guides/
- update-backlog/ → .docs/update-backlog/

### Created
- .docs/PYTHON_ORGANIZATION_POLICY.md (new policy)
- .docs/update-backlog/US-002-docs-consolidation.md (this update)

### Modified
- .claude/settings.json (updated protected paths)
- PROJECT_STRUCTURE.md (updated after previous update)

### Unchanged
- .docs/DEVELOPER_AGENT_QUALITY_MANDATE.md
- .docs/SCOPE_REDUCTION_SUMMARY.md
- .docs/project-breakdown.md
- packages/
- utils/

---

## Verification

### Directory Structure

```bash
# Verify consolidated structure
ls -la .docs/ | grep "^d"
# Should show: project-management/, system-guides/, update-backlog/

# Verify no scattered directories in root
ls -d project-management/ system-guides/ update-backlog/
# Should show: No such file or directory

# Verify utils/ is unchanged
ls utils/
# Should show: __init__.py, config_loader.py
```

### Settings Validation

```bash
# Validate settings.json
python -c "import json; json.load(open('.claude/settings.json')); print('✓ Valid')"

# Check protected patterns
grep -A5 '"protectedPatterns"' .claude/settings.json
```

### Python Policy Compliance

```bash
# Should show no Python files in root (except __main__.py if it exists)
find . -maxdepth 1 -name "*.py" -not -name "__main__.py"
# Should output nothing (or only __main__.py)
```

---

## Navigation Changes

### Old Paths (now invalid)

```
system-guides/CONFIGURATION_GUIDE.md           ❌
project-management/README.md                   ❌
update-backlog/README.md                       ❌
update-backlog/US-000-utils-migration.md       ❌
```

### New Paths (correct)

```
.docs/system-guides/CONFIGURATION_GUIDE.md           ✅
.docs/project-management/README.md                   ✅
.docs/update-backlog/README.md                       ✅
.docs/update-backlog/US-000-utils-migration.md       ✅
.docs/update-backlog/US-002-docs-consolidation.md   ✅
```

### Links to Update

If any documentation references old paths, update them:

```markdown
# Old reference
See system-guides/QUICK_REFERENCE.md

# New reference
See .docs/system-guides/QUICK_REFERENCE.md
```

---

## New Project Structure

```
C:\dev\league-of-legends\info-lol-v0.0.3\
├── .claude/
│   └── settings.json                      ← Updated ✓
├── .docs/                                 ← Consolidated
│   ├── DEVELOPER_AGENT_QUALITY_MANDATE.md
│   ├── QUALITY_INTEGRATION_SUMMARY.md
│   ├── SCOPE_REDUCTION_SUMMARY.md
│   ├── REDUCTION_NOTES.md
│   ├── project-breakdown.md
│   ├── PYTHON_ORGANIZATION_POLICY.md      ← NEW ✓
│   ├── system-guides/                     ← Moved ✓
│   │   ├── README.md
│   │   ├── CONFIGURATION_GUIDE.md
│   │   ├── DEVELOPMENT_PIPELINE_SUMMARY.md
│   │   └── QUICK_REFERENCE.md
│   ├── project-management/                ← Moved ✓
│   │   ├── README.md
│   │   └── [internal] *.txt/*.md
│   └── update-backlog/                    ← Moved ✓
│       ├── README.md
│       ├── US-000-utils-migration.md
│       ├── US-001-directory-reorganization.md
│       └── US-002-docs-consolidation.md
├── packages/
├── utils/
│   ├── __init__.py
│   └── config_loader.py
├── development.cfg
├── development.cfg.local.example
├── PROJECT_STRUCTURE.md
└── [others...]
```

---

## Python Organization Policy Details

### The Rule

> **No Python files in the main project root directory except `__main__.py`**

### Why

- **Clarity**: Root shows docs/config structure, not code
- **Organization**: All utilities discoverable in one place
- **Scalability**: Easy to add utilities without clutter
- **Imports**: Consistent `from utils import X` pattern

### Allowed in Root

✅ `__main__.py` – Application entry point (only Python file)  
✅ `development.cfg` – Configuration files  
✅ `.gitignore` – Git configuration  
✅ `PROJECT_STRUCTURE.md` – Documentation  

### Enforcement

- Pre-commit hook prevents `*.py` in root (except __main__.py)
- Settings.json enforces via `fileProtection`
- Policy document in `.docs/PYTHON_ORGANIZATION_POLICY.md`

---

## Future Organization

### As project grows:

```
utils/
├── __init__.py
├── config_loader.py       ← Current
├── task_parser.py         ← If created
├── validators.py          ← Future
├── formatters.py          ← Future
└── logging.py             ← Future
```

### Or with subpackages:

```
utils/
├── config/
│   ├── loader.py
│   └── validators.py
├── parsing/
│   ├── tasks.py
│   └── specs.py
└── logging/
    └── setup.py
```

**Key principle**: All Python code in `utils/`, all docs in `.docs/`

---

## Access Control Update

### Settings.json Changes

**Before**:
```json
"protected": [
  "packages/",
  ".docs/",
  "utils/",
  "system-guides/",
  "project-management/",
  "update-backlog/"
],
"protectedPatterns": [
  "packages/**/tasks.md",
  ".docs/DEVELOPER_AGENT_QUALITY_MANDATE.md",
  "system-guides/**/*.md",
  "project-management/**/*",
  "update-backlog/US-*.md"
]
```

**After**:
```json
"protected": [
  "packages/",
  ".docs/",
  "utils/"
],
"protectedPatterns": [
  "packages/**/tasks.md",
  ".docs/**/*.md",
  ".docs/**/README.md",
  ".docs/**/*",
  "*.py"
]
```

**Benefits**:
- Simpler patterns (unified under `.docs/`)
- Python file rule explicit (`*.py` in root)
- Less code, more coverage

---

## Related Documentation

- **PYTHON_ORGANIZATION_POLICY.md**: Full policy document
- **.claude/settings.json**: Enforcement configuration
- **PROJECT_STRUCTURE.md**: Overall file organization (may need update)
- **.docs/system-guides/README.md**: Navigation help
- **.docs/project-management/README.md**: Internal processes

---

## Q&A

**Q: Can I put Python files in `backend/` or `frontend/`?**  
A: Yes. This policy applies only to the main project root. Subdirectories have their own organization.

**Q: What about `setup.py` or `pyproject.toml` in future?**  
A: Those are configuration files, allowed in root. Only `.py` executable files are forbidden.

**Q: What if I need a quick test script?**  
A: Put it in `utils/` (e.g., `utils/test_thing.py`), even if temporary.

**Q: Can I have `__init__.py` in root?**  
A: No. Only `__main__.py`. The project is not a root-level package.

---

## Status

✅ **Documentation consolidated** into `.docs/`  
✅ **Python policy created** and documented  
✅ **Settings updated** with new protection rules  
✅ **Directory structure cleaned** (no scattered dirs in root)  
✅ **Enforcement enabled** via pre-commit hooks  

---

**Status**: ✅ Implemented  
**Date**: 2026-04-10  
**Authority**: Architecture Team  
**Related**: US-000, US-001 (prior updates)
