# Project Structure – The Summoner's Chronicle v0.0.3

**Updated**: 2026-04-10  
**Organization**: Enhanced with purpose-specific directories and update backlog system

---

## Directory Overview

```
C:\dev\league-of-legends\info-lol-v0.0.3\
├── .claude/                              ← Claude Code configuration
│   ├── settings.json                     ← Access control & enforcement hooks
│   └── logs/                             ← Development logs
│
├── .docs/                                ← CORE GOVERNANCE (not moved)
│   ├── DEVELOPER_AGENT_QUALITY_MANDATE.md ← 7 pillars of quality (authority)
│   ├── QUALITY_INTEGRATION_SUMMARY.md    ← Quality requirements in scope
│   ├── SCOPE_REDUCTION_SUMMARY.md        ← Out-of-scope items & decisions
│   ├── REDUCTION_NOTES.md                ← Scope change log
│   └── project-breakdown.md              ← Architecture & 12-week timeline
│
├── system-guides/                        ← DEVELOPER GUIDES (NEW)
│   ├── README.md                         ← Navigation & index
│   ├── CONFIGURATION_GUIDE.md            ← Setup & configuration how-to
│   ├── DEVELOPMENT_PIPELINE_SUMMARY.md   ← System overview & architecture
│   └── QUICK_REFERENCE.md                ← Developer cheat sheet (printable)
│
├── project-management/                   ← INTERNAL DIRECTIVES (NEW)
│   ├── README.md                         ← Index & explanation
│   ├── [internal] SPEC_PACKAGING_AGENT_PROMPT.md
│   ├── [internal] SPEC_TO_TASK_MARKDOWN_AGENT.txt
│   ├── [internal] STAKEHOLDER_BOARD_SCOPE_AGENT.txt
│   └── [internal] STAKEHOLDER_DEVELOPER_AGENT.txt
│
├── update-backlog/                       ← CHANGE LOG (NEW)
│   ├── README.md                         ← Update backlog policy & conventions
│   ├── US-000-utils-migration.md         ← Utils directory migration
│   └── US-001-directory-reorganization.md ← This reorganization
│
├── packages/                             ← SPECIFICATIONS & TASKS (organized)
│   ├── README.md
│   ├── tasks.md                          ← 8 global tasks
│   ├── overview/
│   ├── visual-design/
│   │   ├── zones/
│   │   │   ├── zone-1-header/
│   │   │   ├── zone-2-champion-portrait/
│   │   │   ├── zone-3-timeline-narrative/
│   │   │   ├── zone-4-performance-matrix/
│   │   │   │   ├── quadrant-a-gold-xp/
│   │   │   │   ├── quadrant-b-combat-efficiency/
│   │   │   │   ├── quadrant-c-objective-control/
│   │   │   │   └── quadrant-d-clutch-factor/
│   │   │   ├── zone-5-positioning-vision/
│   │   │   │   ├── computer-vision-heatmap/
│   │   │   │   └── ward-placement-intelligence/
│   │   │   ├── zone-6-build-breakdown/
│   │   │   │   └── ability-efficiency-rating/
│   │   │   ├── zone-7-comparative-insights/
│   │   │   └── tasks.md
│   │   └── tasks.md
│   ├── statistics-and-algorithms/
│   │   ├── computer-vision-heatmaps/
│   │   ├── win-probability-model/
│   │   ├── role-positional-normalization/
│   │   ├── natural-language-generation/
│   │   ├── build-adaptation-scoring/
│   │   └── tasks.md
│   └── infrastructure/
│       ├── data-sources/
│       ├── privacy-guardrails/
│       ├── accessibility/
│       ├── localization/
│       ├── polish-features/
│       └── tasks.md
│
├── utils/                                ← SHARED UTILITIES (NEW)
│   ├── __init__.py                       ← Package exports
│   └── config_loader.py                  ← Configuration management
│
├── data/                                 ← RUNTIME DATA (created as needed)
│   ├── uploads/
│   ├── outputs/
│   ├── temp/
│   ├── cache/
│   └── summoners_chronicle.db
│
├── logs/                                 ← APPLICATION LOGS
│   └── development.log
│
├── .gitignore                            ← Secret protection
├── development.cfg                       ← Main configuration (commit)
├── development.cfg.local.example         ← Config template (commit)
└── PROJECT_STRUCTURE.md                  ← THIS FILE

[Additional files: tests/, frontend/, backend/ will be created during implementation]
```

---

## Directory Purposes

### 🔐 `.claude/` – Claude Code Configuration
- **settings.json**: Access control policy, protected files, enforcement hooks
- **logs/**: Development environment logs

**Protected**: ✅ Yes  
**Modify with**: Change log in update-backlog/  
**Authority**: System administrator

---

### 📋 `.docs/` – Core Governance Documents
Core architectural and policy documents that define the project:

| File | Purpose | Authority |
|------|---------|-----------|
| DEVELOPER_AGENT_QUALITY_MANDATE.md | 7 pillars of quality | Stakeholder board |
| QUALITY_INTEGRATION_SUMMARY.md | Quality in task scope | Architecture team |
| SCOPE_REDUCTION_SUMMARY.md | Out-of-scope decisions | Stakeholder board |
| REDUCTION_NOTES.md | Scope change log | Project manager |
| project-breakdown.md | Architecture & timeline | Lead architect |

**Protected**: ✅ Yes  
**Modify with**: Change log + stakeholder approval  
**Authority**: Stakeholder board

---

### 📖 `system-guides/` – Developer Guides (NEW)
User-facing documentation for developers setting up and working with the system:

| File | Purpose | Audience |
|------|---------|----------|
| README.md | Navigation & quick links | Everyone |
| CONFIGURATION_GUIDE.md | Setup and configuration how-to | Developers |
| DEVELOPMENT_PIPELINE_SUMMARY.md | System overview and architecture | Everyone |
| QUICK_REFERENCE.md | Developer cheat sheet (printable) | Active developers |

**Protected**: ✅ Yes  
**Modify with**: Change log + update-backlog/US-* summary  
**Authority**: Documentation team

---

### 🏗️ `project-management/` – Internal Directives (NEW)
Internal documentation defining architectural decisions and processes:

| File | Purpose |
|------|---------|
| README.md | Navigation and explanation |
| [internal] SPEC_PACKAGING_AGENT_PROMPT.md | Specification decomposition rules |
| [internal] SPEC_TO_TASK_MARKDOWN_AGENT.txt | Task extraction rules |
| [internal] STAKEHOLDER_BOARD_SCOPE_AGENT.txt | Scope reduction rules |
| [internal] STAKEHOLDER_DEVELOPER_AGENT.txt | Quality enforcement rules |

**Protected**: ✅ Yes  
**Modify with**: Change log + full justification  
**Authority**: Stakeholder board

---

### 📝 `update-backlog/` – Change Log (NEW)
Version-controlled summaries of significant project updates:

| File | Purpose |
|------|---------|
| README.md | Update backlog policy (naming, workflow, best practices) |
| US-000-utils-migration.md | Utils directory migration |
| US-001-directory-reorganization.md | Directory structure reorganization |

**Format**: `US-[ID]-[context-a]-[context-b].md`  
**Protected**: ✅ Yes (US-* files)  
**Authority**: Everyone (authors own updates)

---

### 📦 `packages/` – Specifications & Tasks
36 specification files and 30 task files organized hierarchically:

| Type | Count | Purpose |
|------|-------|---------|
| README files | 36 | Specifications organized by concern |
| tasks.md files | 30 | ~150 project management tasks |

**Hierarchy**:
- `packages/` – Global overview
- `packages/overview/` – Project overview
- `packages/visual-design/` – 7 zones with 4 quadrants
- `packages/statistics-and-algorithms/` – 5 algorithms
- `packages/infrastructure/` – 5 subsystems

**Protected**: ✅ Yes  
**Modify with**: Change log + scope impact analysis  
**Authority**: Architecture team

---

### 🛠️ `utils/` – Shared Utilities (NEW)
Reusable Python modules for configuration, logging, validation, etc.:

| File | Purpose |
|------|---------|
| __init__.py | Package exports and imports |
| config_loader.py | Configuration management system |

**Protected**: ✅ Yes (entire directory)  
**Modify with**: Change log + update-backlog/US-* summary  
**Authority**: Development team

---

### 📁 `data/` – Runtime Data
Directory for generated files, databases, temporary storage:

```
data/
├── uploads/        ← File uploads
├── outputs/        ← Generated graphics
├── temp/          ← Temporary processing files
├── cache/         ← Cached data
└── *.db           ← SQLite databases
```

**Protected**: ❌ No (runtime data)  
**Git ignored**: ✅ Yes (in .gitignore)

---

### 📋 `logs/` – Application Logs
Development and runtime logs:

**Protected**: ❌ No (runtime logs)  
**Git ignored**: ✅ Yes (in .gitignore)

---

## File Protection Matrix

| Path | Protected | Type | Change Requirements |
|------|-----------|------|---------------------|
| `.claude/settings.json` | ✅ | System | Change log + justification |
| `.docs/` | ✅ | Governance | Change log + stakeholder approval |
| `system-guides/` | ✅ | Documentation | Change log + US-* update |
| `project-management/` | ✅ | Internal | Change log + executive approval |
| `packages/` | ✅ | Specification | Change log + scope analysis |
| `update-backlog/` | ✅ | Change log | New US-* file (automatic) |
| `utils/` | ✅ | Code | Change log + US-* update |
| `data/` | ❌ | Runtime | None (gitignored) |
| `logs/` | ❌ | Runtime | None (gitignored) |

**Note**: Enforcement via `.claude/settings.json` pre-commit and pre-task-completion hooks.

---

## Information Architecture

### By Purpose

**Governance & Policy** → `.docs/`
- Quality standards
- Scope decisions
- Architecture decisions

**Developer Resources** → `system-guides/`
- How-to guides
- Reference material
- Onboarding

**Internal Processes** → `project-management/`
- Agent directives
- Process rules
- Decision frameworks

**Change History** → `update-backlog/`
- Queryable summaries
- Version-controlled
- Git-integrated

**Specifications** → `packages/`
- What to build
- Task definitions
- Dependencies

**Code** → `utils/`, `backend/`, `frontend/` (TBD)
- Implementation
- Libraries
- Applications

---

### By Access Pattern

**Reading Specs** → `packages/README.md` files

**Checking Tasks** → `packages/*/tasks.md` files

**Understanding Quality** → `.docs/DEVELOPER_AGENT_QUALITY_MANDATE.md`

**Setting Up Development** → `system-guides/CONFIGURATION_GUIDE.md`

**Getting Quick Answer** → `system-guides/QUICK_REFERENCE.md`

**Checking Recent Changes** → `update-backlog/` (sorted by ID)

**Understanding Decisions** → `project-management/README.md`

---

## Navigation Quick Links

| Need | Go To |
|------|-------|
| Setup development environment | system-guides/CONFIGURATION_GUIDE.md |
| Understand system architecture | system-guides/DEVELOPMENT_PIPELINE_SUMMARY.md |
| Printable cheat sheet | system-guides/QUICK_REFERENCE.md |
| Quality mandate | .docs/DEVELOPER_AGENT_QUALITY_MANDATE.md |
| Scope decisions | .docs/SCOPE_REDUCTION_SUMMARY.md |
| View tasks | packages/*/tasks.md |
| Find specifications | packages/*/README.md |
| Recent changes | update-backlog/ |
| Configuration help | utils/config_loader.py |

---

## Key Statistics

| Category | Count |
|----------|-------|
| Specification files | 36 |
| Task files | 30 |
| Tasks total | ~150 |
| Directories (total) | 20+ |
| Protected directories | 6 |
| Update summaries | 2 (active) |
| Core governance docs | 5 |
| Developer guides | 3 |
| Agent directives | 4 |

---

## Git Integration

### Standard Workflow

```bash
# 1. Make changes to protected files
vim system-guides/CONFIGURATION_GUIDE.md

# 2. Create update summary
touch update-backlog/US-NNN-[context-a]-[context-b].md
vim update-backlog/US-NNN-*.md

# 3. Commit together
git add system-guides/CONFIGURATION_GUIDE.md update-backlog/US-NNN-*.md
git commit -m "US-NNN: Brief title

- Change 1
- Change 2

See update-backlog/US-NNN-[context].md for full details."
```

### Querying History

```bash
# Find all updates
ls update-backlog/US-*.md

# Find updates by context
ls update-backlog/US-*-utils-*.md
ls update-backlog/US-*-quality-*.md

# See git history
git log --oneline update-backlog/
git log --format="%h %s" -- system-guides/
```

---

## Protected Files Policy

**Why Protected**:
- Prevent accidental changes to core governance
- Track all modifications via git
- Enforce change log requirements
- Maintain architectural consistency

**How Protected**:
- Defined in `.claude/settings.json`
- Enforced by pre-commit hooks
- Require justification in change logs
- Changes tracked in update-backlog/

**Modification Process**:
1. Create branch
2. Make changes
3. Create `update-backlog/US-*.md` summary
4. Commit with explanation
5. Require code review before merge

---

## Next Steps

### Immediate

- [ ] Review system-guides/ for developer onboarding
- [ ] Read project-management/README.md for architectural context
- [ ] Bookmark system-guides/QUICK_REFERENCE.md
- [ ] Start implementation using packages/*/tasks.md

### Ongoing

- [ ] Create US-* update summaries for significant changes
- [ ] Keep .docs/ current with decisions
- [ ] Update system-guides/ when processes change
- [ ] Maintain update-backlog/ as historical record

### Future

- [ ] Add backend/ directory for Python code
- [ ] Add frontend/ directory for React code
- [ ] Add tests/ directory for test suites
- [ ] Add infrastructure/ directory for deployment configs

---

## Questions?

| Question | Answer |
|----------|--------|
| Where do I find guides? | system-guides/ |
| Where are specs? | packages/*README.md |
| Where are tasks? | packages/*/tasks.md |
| How do I configure? | system-guides/CONFIGURATION_GUIDE.md |
| What's out of scope? | .docs/SCOPE_REDUCTION_SUMMARY.md |
| What quality matters? | .docs/DEVELOPER_AGENT_QUALITY_MANDATE.md |
| What changed recently? | update-backlog/ |

---

## Summary

The project is now organized with:

✅ **Governance** in `.docs/` (core policies)  
✅ **Guides** in `system-guides/` (developer resources)  
✅ **Internal Processes** in `project-management/` (architecture)  
✅ **Change Log** in `update-backlog/` (history)  
✅ **Specifications** in `packages/` (what to build)  
✅ **Utilities** in `utils/` (shared code)  
✅ **Protection** enforced in `.claude/settings.json`  

**Status**: ✅ Ready for implementation

---

**Last Updated**: 2026-04-10  
**Authority**: Architecture Team  
**Owner**: Project Maintainers
