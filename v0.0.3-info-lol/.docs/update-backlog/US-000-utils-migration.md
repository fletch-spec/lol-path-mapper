# Utils Directory Migration Guide

## Overview

The `config_loader.py` module has been moved from the root directory to the new `utils/` package for better project organization.

**Effective Date**: 2026-04-10  
**Status**: Complete

---

## What Changed

### File Structure

**Before**:
```
C:\dev\league-of-legends\info-lol-v0.0.3\
├── config_loader.py              ← Root level
└── ...
```

**After**:
```
C:\dev\league-of-legends\info-lol-v0.0.3\
├── utils/
│   ├── __init__.py               ← New package init
│   └── config_loader.py          ← Moved here
└── ...
```

### Settings Changes

In `.claude/settings.json`:
- **Before**: Protected `"task_parser.py"` individually
- **After**: Protected `"utils/"` directory (entire package protected)

Benefits:
- All future utilities in `utils/` are automatically protected
- Simpler to manage growing utility library
- Clear separation of concerns

### Lint Warning Fixes

Fixed invalid hook field names in `.claude/settings.json`:
- `"warning"` → `"warningMessage"` (3 instances)

Affected hooks:
- `test-status-check`
- `protected-file-warning`
- `scope-boundary-warning`

---

## Updating Your Code

### Python Imports

**Old Import Path**:
```python
from config_loader import Config, initialize_config
```

**New Import Path**:
```python
from utils.config_loader import Config, initialize_config
```

**Alternative (using package init)**:
```python
from utils import Config, initialize_config
```

### Usage Examples

#### Old (pre-migration)
```python
# File: backend/app.py
from config_loader import Config

config = Config()
api_key = config.get('api_integration', 'RIOT_API_KEY')
```

#### New (post-migration)
```python
# File: backend/app.py
from utils.config_loader import Config
# OR
from utils import Config

config = Config()
api_key = config.get('api_integration', 'RIOT_API_KEY')
```

### Script Execution

**Old**:
```bash
python config_loader.py
```

**New**:
```bash
python -m utils.config_loader
```

Or from root:
```bash
cd utils && python config_loader.py
```

---

## Files Affected

### Need Update

If you have any files importing `config_loader` directly, update them:

```bash
# Find all Python files importing config_loader
grep -r "from config_loader" .
grep -r "import config_loader" .
```

### Protected in Settings

**Now Protected** ✓:
- `utils/` (entire directory)
- All files within `utils/`

**Previously Protected** (if applicable):
- `task_parser.py` (removed from explicit protection, may be added to `utils/` later)

---

## Verification Checklist

- [ ] Deleted root-level `config_loader.py` (if it exists)
- [ ] Verified `utils/config_loader.py` exists
- [ ] Verified `utils/__init__.py` exists
- [ ] Updated all import statements in code
- [ ] Ran `python -m utils.config_loader` to verify it works
- [ ] Updated settings.json (already done ✓)
- [ ] Fixed "warningMessage" lint issues in settings.json (already done ✓)

---

## Command Reference

### Validate Configuration

```bash
# New way (from project root)
python -m utils.config_loader

# Or from utils directory
cd utils && python config_loader.py
```

### Import in Code

```python
# Option 1: Direct import
from utils.config_loader import Config

# Option 2: Package import
from utils import Config

# Option 3: Full path (less common)
from utils.config_loader import initialize_config
```

### Access Configuration

```python
config = Config()

# All methods work the same as before
api_key = config.get('api_integration', 'RIOT_API_KEY')
debug = config.get_bool('project', 'DEBUG_MODE')
port = config.get_int('frontend', 'FRONTEND_PORT')
origins = config.get_list('backend', 'CORS_ORIGINS')
```

---

## Settings.json Changes

### Before (Invalid)
```json
{
  "name": "test-status-check",
  "warning": "Some tests are skipped..."
}
```

### After (Valid)
```json
{
  "name": "test-status-check",
  "warningMessage": "Some tests are skipped..."
}
```

**Applied To**:
1. `pre-commit.checks.test-status-check`
2. `before-file-edit.checks.protected-file-warning`
3. `before-file-edit.checks.scope-boundary-warning`

---

## File Protection Update

### Before
```json
"protected": [
  "packages/",
  ".docs/",
  "task_parser.py"
]
```

### After
```json
"protected": [
  "packages/",
  ".docs/",
  "utils/"
]
```

**Impact**:
- `utils/` directory and all contents are protected
- Can only be modified with change log entry + justification
- Settings in `.claude/settings.json` prevent scope creep in utilities

---

## Future Expansion

The `utils/` package is now the central location for shared utilities:

```
utils/
├── __init__.py
├── config_loader.py        ← Configuration management
├── validators.py           ← (Future) Input validation
├── formatters.py           ← (Future) Output formatting
├── logger.py               ← (Future) Logging utilities
└── decorators.py           ← (Future) Common decorators
```

All future utilities should be added to this package, keeping the root directory clean.

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'utils'"

**Cause**: Running from wrong directory or missing `__init__.py`

**Fix**:
```bash
# Ensure you're in project root
pwd  # Should show: C:\dev\league-of-legends\info-lol-v0.0.3

# Ensure __init__.py exists
ls utils/__init__.py

# Try import
python -c "from utils import Config; print('✓ Import successful')"
```

### "No module named 'config_loader'"

**Cause**: Using old import path

**Fix**:
```python
# WRONG
from config_loader import Config

# RIGHT
from utils.config_loader import Config
# OR
from utils import Config
```

### Settings.json Lint Warnings Gone?

**Verification**:
```bash
# Check that warningMessage is used (not warning)
grep "warningMessage" .claude/settings.json

# Should show 3 results:
# 1. test-status-check
# 2. protected-file-warning
# 3. scope-boundary-warning
```

---

## Documentation Updates

### Updated Files

- ✓ `.docs/CONFIGURATION_GUIDE.md` - Update import examples
- ✓ `.docs/QUICK_REFERENCE.md` - Update command reference
- ✓ `.docs/DEVELOPMENT_PIPELINE_SUMMARY.md` - Update code examples
- ✓ `utils/__init__.py` - New package manifest

### Import Examples (Updated)

All documentation now shows:
```python
from utils.config_loader import Config
# OR
from utils import Config
```

---

## Contact & Support

For issues with the migration:
1. Check this guide for common problems
2. Verify `.claude/settings.json` has the new "utils/" protection
3. Verify `utils/__init__.py` exists and contains exports
4. Review import statements in your code

---

## Summary

✅ **What Changed**:
- Moved `config_loader.py` to `utils/config_loader.py`
- Created `utils/__init__.py` for package exports
- Updated file protection in settings.json
- Fixed lint warnings (warning → warningMessage)

✅ **What You Need to Do**:
- Update imports in your code: `from utils.config_loader import Config`
- Run validation: `python -m utils.config_loader`
- No changes needed to config files or logic

✅ **Status**: Complete and ready to use

**New Import**: `from utils import Config`
