# Quick Reference Card – The Summoner's Chronicle Development

**Print this card • Pin to your desk • Bookmark in your editor**

---

## ⚡ First-Time Setup (30 min)

```bash
cd C:\dev\league-of-legends\info-lol-v0.0.3
cp development.cfg.local.example development.cfg.local
# Edit development.cfg.local with your API keys
python config_loader.py  # Should show: ✓ Configuration validation passed!
```

---

## 📋 Essential Commands

| Task | Command |
|------|---------|
| **Validate config** | `python config_loader.py` |
| **View all tasks** | `python task_parser.py` |
| **See your task** | `less packages/infrastructure/data-sources/README.md` |
| **Check quality mandate** | `less .docs/DEVELOPER_AGENT_QUALITY_MANDATE.md` |
| **Check configuration** | `less .docs/CONFIGURATION_GUIDE.md` |
| **View architecture** | `less .docs/project-breakdown.md` |

---

## 🎯 Before You Code

- [ ] Read the task description in `packages/*/README.md`
- [ ] Read quality mandate (7 sections): `.docs/DEVELOPER_AGENT_QUALITY_MANDATE.md`
- [ ] Create a feature branch: `git checkout -b feature/your-feature`
- [ ] Check task dependencies in `packages/*/tasks.md`

---

## ✍️ While You Code

### 7 Pillars of Quality (REQUIRED for every task)

| Pillar | What | Minimum |
|--------|------|---------|
| **1. Docstrings** | Every function/module documented | Purpose + inputs + outputs |
| **2. Error Handling** | All external calls wrapped | Logging with severity |
| **3. Tests** | Unit + integration + initialization | 80% code, 90% critical paths |
| **4. Code Structure** | Functions ≤50 lines, modules ≤10 functions | Clear separation of concerns |
| **5. Configuration** | No hardcoded values | All env-specific in config |
| **6. Logging** | Major events logged | Timestamps + severity levels |
| **7. Init Tests** | Startup verification | Configuration validation |

---

## 📤 Before You Commit

### Code Checklist
```
[ ] All docstrings present
[ ] Error handling for all external calls
[ ] Tests written (unit + integration)
[ ] Test coverage ≥80% (verify with coverage tool)
[ ] Initialization test passes
[ ] No hardcoded values (all in development.cfg)
[ ] Comments explain "why", not "what"
[ ] Functions ≤50 lines
[ ] No circular dependencies
```

### Fill Out Quality Report
```markdown
# Quality Report: [Task Name]

**Task ID:** [from packages/*/tasks.md]
**Date:** [YYYY-MM-DD]

### Pillar Compliance

| Pillar | ✓ | Notes |
|--------|---|-------|
| 1. Docstrings | [ ] | [brief] |
| 2. Error Handling | [ ] | [brief] |
| 3. Test Suite | [ ] | Test count & coverage % |
| 4. Code Structure | [ ] | [brief] |
| 5. Configuration | [ ] | [brief] |
| 6. Logging | [ ] | [brief] |
| 7. Init Tests | [ ] | [brief] |

### Test Results
- Line Coverage: [XX%]
- Critical Path Coverage: [XX%]
- All Tests Passing: [ ] Yes [ ] No

### Sign-Off
I certify all 7 pillars are compliant.
```

### Commit Message Format
```
[TASK-ID] Brief description (50 chars)

- What changed
- Why it changed
- Quality considerations

[QR: quality-report-2026-04-10-task-name.md]
```

---

## 🐛 Configuration Issues?

```bash
# Validate everything
python config_loader.py

# Check if files exist
ls development.cfg
ls development.cfg.local

# Check if file has actual values (not placeholders)
grep RIOT_API_KEY development.cfg.local
grep SECRET_KEY development.cfg.local

# Environment variables override config
export RIOT_API_KEY=RGAPI-actual-key
python config_loader.py
```

---

## ❌ Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Hardcoded API key in code | Security risk + scope violation | Use `config.get('section', 'KEY')` |
| No error handling on API call | Crashes silently | Wrap in try-catch + log |
| Test coverage <80% | Task rejected | Write more tests |
| No docstrings | Quality gate fails | Add docstring to every function |
| Placeholder in config | Config validation fails | Update development.cfg.local |
| Forgot quality report | Can't mark complete | Fill out quality report template |
| Commit to main branch | Bypasses hooks | Use feature branch |

---

## 🔍 File Locations

| File | Purpose | Location |
|------|---------|----------|
| Quality Mandate | 7 pillars & checklists | `.docs/DEVELOPER_AGENT_QUALITY_MANDATE.md` |
| Config Guide | How to use config | `.docs/CONFIGURATION_GUIDE.md` |
| Task List | All tasks | `packages/*/tasks.md` |
| Specifications | What to build | `packages/*/README.md` |
| Config Main | Development settings | `development.cfg` |
| Config Local | Your secrets (gitignored) | `development.cfg.local` |
| Config Loader | Access config in code | `config_loader.py` |
| Project Breakdown | Architecture & timeline | `.docs/project-breakdown.md` |
| Scope Summary | What's in/out | `.docs/SCOPE_REDUCTION_SUMMARY.md` |
| Settings | Access control policy | `.claude/settings.json` |

---

## 💻 Python Configuration Usage

```python
from config_loader import Config

config = Config()

# String
api_key = config.get('api_integration', 'RIOT_API_KEY')

# Boolean
debug = config.get_bool('project', 'DEBUG_MODE')

# Integer
port = config.get_int('frontend', 'FRONTEND_PORT')

# List
origins = config.get_list('backend', 'CORS_ORIGINS')

# All items in section
backend = config.section_items('backend')

# With fallback
log_level = config.get('logging', 'LOG_LEVEL', fallback='INFO')
```

---

## 📊 Key Numbers

| Metric | Value |
|--------|-------|
| **Test Coverage Minimum** | 80% lines, 90% critical |
| **Max Function Length** | 50 lines |
| **Max Functions/Module** | 10 |
| **Session Timeout** | 3600 seconds |
| **API Timeout** | 10 seconds |
| **Estimated Total Effort** | 300-350 hours |
| **MVP Timeline** | 12-16 weeks |
| **Effort per Task** | S=6-8h, M=12-16h, L=20-30h, XL=40-80h |

---

## 🚨 NEVER DO

❌ Commit `development.cfg.local` to git  
❌ Hardcode API keys in code  
❌ Skip error handling on external calls  
❌ Merge to main without quality report  
❌ Use placeholder config values in production  
❌ Modify protected files without change log  
❌ Commit without task reference `[TASK-ID]`  
❌ Mark task complete without quality verification  

---

## ✅ DO DO

✅ Use feature branches  
✅ Write tests as you code  
✅ Fill out quality reports  
✅ Externalize all configuration  
✅ Log errors with severity  
✅ Add docstrings everywhere  
✅ Keep functions short  
✅ Reference quality mandate  

---

## 📞 Help & Documentation

| Need | See |
|------|-----|
| Quality rules | `.docs/DEVELOPER_AGENT_QUALITY_MANDATE.md` |
| Config setup | `.docs/CONFIGURATION_GUIDE.md` |
| Full overview | `.docs/DEVELOPMENT_PIPELINE_SUMMARY.md` |
| Architecture | `.docs/project-breakdown.md` |
| Scope decisions | `.docs/SCOPE_REDUCTION_SUMMARY.md` |
| Task details | `packages/*/tasks.md` |
| Specifications | `packages/*/README.md` |

---

## 🔐 Secret Setup

```bash
# Generate SECRET_KEY
python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))"

# Generate JWT_SECRET
python -c "import secrets; print('JWT_SECRET=' + secrets.token_hex(32))"

# Get RIOT_API_KEY from https://developer.riotgames.com/

# Add to development.cfg.local:
[security]
SECRET_KEY=<your-generated-key>
JWT_SECRET=<your-generated-key>

[api_integration]
RIOT_API_KEY=RGAPI-<your-key>
```

---

## 🎯 One-Task Workflow

1. **Pick Task** from `packages/tasks.md`
2. **Create Branch** `git checkout -b feature/task-name`
3. **Read Spec** from `packages/*/README.md` (source in task)
4. **Code** following 7 pillars + quality mandate
5. **Test** until 80%+ coverage
6. **Log** all major events
7. **Document** with docstrings
8. **Write Quality Report** from template
9. **Commit** with `[TASK-ID] [QR: report-name]`
10. **Merge** to main after verification

---

## ⏱️ Effort Estimates

| Size | Hours | Examples |
|------|-------|----------|
| **XS** | 2–4 | Small utility, one function |
| **S** | 6–8 | Documentation, smoke tests |
| **M** | 12–16 | One algorithm, basic API |
| **L** | 20–30 | Two algorithms, zone rendering |
| **XL** | 40–80 | Complex feature, full integration |

---

## 🔄 Current Phase

**Phase**: Setup + Foundation  
**Status**: ✓ Governance complete, ready for development  
**Current Focus**: First task = "Set up Riot API integration and data pipeline"  
**Next**: Implement algorithms (Phase 2)

---

**Last Updated**: 2026-04-10  
**Print & Pin This Card** 📌
