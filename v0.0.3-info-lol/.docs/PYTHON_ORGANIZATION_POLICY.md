# Python Organization Policy

**Effective Date**: 2026-04-10  
**Status**: Active  
**Authority**: Architecture Team

---

## Policy Statement

**No Python files in the main project root directory except `__main__.py`.**

All utility and library Python modules must be organized in the `utils/` directory.

---

## Rationale

### Why This Matters

1. **Clarity**: Root directory shows documentation structure, not code
2. **Organization**: All Python utilities in one discoverable location
3. **Imports**: Simpler import paths (`from utils import Config`)
4. **Scalability**: Easy to add more utilities without cluttering root
5. **Separation**: Code vs. documentation/configuration separation

### What It Prevents

❌ Root-level utility scripts scattered randomly  
❌ Import confusion (root vs. installed packages)  
❌ Difficulty finding utilities  
❌ Accidental execution of scripts from root  

### What It Enables

✅ Clean root directory (just docs and config)  
✅ All utilities in single, organized location  
✅ Consistent import paths  
✅ Easy package structure understanding  

---

## Rules

### ✅ Allowed in Main Root

| Type | Example | Notes |
|------|---------|-------|
| `__main__.py` | Application entry point | Single file, top-level runner |
| Configuration files | `development.cfg` | `.cfg`, `.env`, `.json` config files |
| Project metadata | `PROJECT_STRUCTURE.md` | Documentation about structure |
| Git files | `.gitignore`, `.gitattributes` | Version control |
| Build config | `pyproject.toml`, `setup.py` | If needed (future) |

### ❌ NOT Allowed in Main Root

| Type | Example | Action |
|------|---------|--------|
| Utility modules | `config_loader.py` | Move to `utils/` |
| Helper scripts | `task_parser.py` | Move to `utils/` |
| One-off scripts | `validate.py`, `migrate.py` | Move to `utils/` |
| Library code | Any shared module | Move to `utils/` |
| Standalone executables | `fetch_data.py` | Move to `utils/` OR make `__main__.py` |

---

## Directory Organization

### Root Level (Project Root)

```
C:\dev\league-of-legends\info-lol-v0.0.3\
├── __main__.py                    ← Application entry point (ONLY Python file allowed)
├── development.cfg                ← Configuration (not Python)
├── development.cfg.local.example  ← Configuration template
├── .gitignore
├── PROJECT_STRUCTURE.md           ← Documentation
├── .docs/                         ← All documentation
├── .claude/                       ← Claude Code configuration
├── packages/                      ← Specifications
└── utils/                         ← ALL Python utilities
```

### utils/ Directory

```
utils/
├── __init__.py                    ← Package exports
├── config_loader.py               ← Configuration management
├── task_parser.py                 ← Task display/parsing (if created)
├── validators.py                  ← Input validation (future)
├── formatters.py                  ← Output formatting (future)
├── logging.py                     ← Logging utilities (future)
└── decorators.py                  ← Common decorators (future)
```

**All Python code lives in `utils/`**

---

## Import Standards

### Correct Imports

```python
# ✅ Import from utils
from utils.config_loader import Config
from utils import Config, initialize_config

# ✅ From within utils (relative)
from .config_loader import Config

# ✅ Standard library
import os
import sys
from pathlib import Path
```

### Incorrect Imports

```python
# ❌ DO NOT do this
from config_loader import Config  # config_loader is not in root
import task_parser                # task_parser is not in root
```

---

## Implementation Checklist

### Current Status (2026-04-10)

- ✅ `config_loader.py` → moved to `utils/config_loader.py`
- ⏳ `task_parser.py` → should go to `utils/task_parser.py` (if created)
- ✅ `utils/__init__.py` → exports available
- ✅ `utils/` marked as protected directory

### Enforcement

| Check | Method | Enforced By |
|-------|--------|-------------|
| No .py files in root | Pre-commit hook | `.claude/settings.json` |
| All utilities in utils/ | Code review | Architecture team |
| Correct imports | Linting | mypy/pylint (future) |

---

## Future Organization

### As Project Grows

```
utils/
├── __init__.py
├── config/
│   ├── __init__.py
│   ├── loader.py
│   └── validators.py
├── parsing/
│   ├── __init__.py
│   ├── tasks.py
│   └── specs.py
├── logging/
│   ├── __init__.py
│   └── setup.py
└── common/
    ├── __init__.py
    └── decorators.py
```

**As utilities grow, create subpackages within `utils/`**

---

## Special Cases

### `__main__.py` - The Exception

If the project needs a command-line entry point:

```python
# C:\dev\league-of-legends\info-lol-v0.0.3\__main__.py
"""
The Summoner's Chronicle - Main Entry Point

Usage:
    python .
    python -m info_lol
"""

if __name__ == "__main__":
    from utils.config_loader import initialize_config
    from utils.task_parser import TaskParser
    
    config = initialize_config()
    parser = TaskParser()
    parser.run()
```

**This is the ONLY Python file allowed in root.**

### CLI Scripts

If you need command-line utilities:

```python
# C:\dev\league-of-legends\info-lol-v0.0.3\utils\cli.py
"""Command-line interface utilities"""

def main():
    """Main CLI entry point"""
    pass

if __name__ == "__main__":
    main()
```

Run with: `python -m utils.cli`

---

## Benefits

### For Developers

| Benefit | Impact |
|---------|--------|
| **Clear structure** | Easy to find utilities |
| **Simple imports** | `from utils import X` works everywhere |
| **No pollution** | Root stays clean and focused |
| **Scalable** | Easy to add new utilities |

### For Architecture

| Benefit | Impact |
|---------|--------|
| **Consistent** | All utilities in one place |
| **Maintainable** | Single package to manage |
| **Protectable** | Can protect entire `utils/` directory |
| **Versionable** | Easy to version utilities |

### For Documentation

| Benefit | Impact |
|---------|--------|
| **Separation** | Docs vs. code clearly separated |
| **Navigation** | Developers know where to look |
| **Organization** | Logical file structure |

---

## Enforcement Mechanism

### In `.claude/settings.json`

```json
{
  "fileProtection": {
    "protected": ["utils/"],
    "protectedPatterns": [
      "*.py"  // No Python files in root
    ]
  },
  "hooks": {
    "pre-commit": {
      "checks": [
        {
          "name": "python-root-files-check",
          "description": "Prevent Python files in root except __main__.py",
          "required": true,
          "failMessage": "Python files only allowed in utils/ or __main__.py in root"
        }
      ]
    }
  }
}
```

---

## Migration Path

### For Existing Files

| File | Current | Target | Action |
|------|---------|--------|--------|
| config_loader.py | utils/ ✅ | utils/ | Already done |
| task_parser.py | (N/A) | utils/ | Move if created |

### For Future Files

| Scenario | Action | Location |
|----------|--------|----------|
| New utility needed | Create in utils/ | `utils/new_utility.py` |
| New CLI command | Create in utils/ | `utils/cli_command.py` |
| Shared helper | Create in utils/ | `utils/helpers.py` |

---

## Q&A

### Q: Can I have Python files in `backend/` or `frontend/`?

**A**: Yes. This policy applies only to the main project root. Subdirectories (backend/, frontend/, tests/) can have their own Python file organization.

### Q: What about `setup.py` or `pyproject.toml`?

**A**: Those are configuration files, not Python code files. They're allowed in root.

### Q: What if I need a quick script to test something?

**A**: Put it in `utils/` even if temporary. Use `.gitignore` if you don't want it committed.

### Q: Can I create `__init__.py` in root?

**A**: No. The entire project is not a package, only `utils/` is. Keep `__init__.py` only in `utils/`.

---

## Policy Review

**Created**: 2026-04-10  
**Last Updated**: 2026-04-10  
**Next Review**: Upon adding new utilities (or quarterly)

**Approved By**: Architecture Team  
**Enforced By**: Pre-commit hooks (settings.json)  
**Related Policies**: 
- DEVELOPER_AGENT_QUALITY_MANDATE.md (Pillar 4: Code Structure)
- PROJECT_STRUCTURE.md (File organization)

---

## Summary

✅ **One rule**: No Python files in root except `__main__.py`  
✅ **One location**: All utilities in `utils/`  
✅ **One import path**: `from utils import X`  
✅ **Clear structure**: Root = docs/config, utils/ = code  

**This keeps the project organized as it grows.**

---

**Status**: ✅ Active Policy  
**Authority**: Architecture Team  
**Enforcement**: Automated via hooks
