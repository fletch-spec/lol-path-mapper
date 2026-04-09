# .docs – Project Documentation Hub

**Central repository for all documentation, policies, guides, and change logs.**

---

## 📋 Quick Navigation

### 🎯 I want to...

| Goal | Go To |
|------|-------|
| **Get started developing** | system-guides/CONFIGURATION_GUIDE.md |
| **Understand the system** | system-guides/DEVELOPMENT_PIPELINE_SUMMARY.md |
| **Quick reference while coding** | system-guides/QUICK_REFERENCE.md |
| **Learn quality standards** | DEVELOPER_AGENT_QUALITY_MANDATE.md |
| **Understand scope decisions** | SCOPE_REDUCTION_SUMMARY.md |
| **See recent changes** | update-backlog/ |
| **Understand architecture** | project-breakdown.md |
| **Review Python organization** | PYTHON_ORGANIZATION_POLICY.md |
| **Find internal directives** | project-management/ |

---

## 📁 Directory Structure

```
.docs/
├── README.md (you are here)
│
├── CORE GOVERNANCE (authority documents)
│   ├── DEVELOPER_AGENT_QUALITY_MANDATE.md    (7 pillars of quality)
│   ├── QUALITY_INTEGRATION_SUMMARY.md        (quality in scope)
│   ├── SCOPE_REDUCTION_SUMMARY.md            (scope decisions)
│   ├── REDUCTION_NOTES.md                    (scope changelog)
│   ├── project-breakdown.md                  (architecture + timeline)
│   └── PYTHON_ORGANIZATION_POLICY.md         (Python organization rules)
│
├── system-guides/ (developer resources)
│   ├── README.md
│   ├── CONFIGURATION_GUIDE.md                (setup and how-to)
│   ├── DEVELOPMENT_PIPELINE_SUMMARY.md       (overview + architecture)
│   └── QUICK_REFERENCE.md                    (cheat sheet)
│
├── project-management/ (internal directives)
│   ├── README.md
│   └── [internal] SPEC_*.txt/*.md            (agent prompts)
│
└── update-backlog/ (change history)
    ├── README.md
    ├── US-000-utils-migration.md
    ├── US-001-directory-reorganization.md
    └── US-002-docs-consolidation.md
```

---

## 📚 Documentation Categories

### 1️⃣ Core Governance

**Authority documents that define project standards and decisions**

| File | Purpose | Audience |
|------|---------|----------|
| **DEVELOPER_AGENT_QUALITY_MANDATE.md** | 7 pillars of code quality with checklists | Developers, reviewers |
| **QUALITY_INTEGRATION_SUMMARY.md** | How quality is integrated into tasks | Architects |
| **SCOPE_REDUCTION_SUMMARY.md** | What's in/out of scope with rationale | PMs, stakeholders |
| **REDUCTION_NOTES.md** | Detailed scope reduction changelog | Architects |
| **project-breakdown.md** | Architecture, timeline, and strategy (3000+ lines) | Everyone |
| **PYTHON_ORGANIZATION_POLICY.md** | Python file organization rules | Developers |

**Authority**: Stakeholder Board  
**Modify With**: Change log + executive approval + update-backlog/US-* summary

---

### 2️⃣ System Guides

**User-facing guides for developers and operators**

Located in: `system-guides/`

| File | Purpose | When to Use |
|------|---------|------------|
| **CONFIGURATION_GUIDE.md** | Complete setup instructions | New developers setting up |
| **DEVELOPMENT_PIPELINE_SUMMARY.md** | System overview and architecture | Understanding the project |
| **QUICK_REFERENCE.md** | Developer cheat sheet (printable) | Daily development work |

**Authority**: Documentation Team  
**Modify With**: Change log + update-backlog/US-* summary

**Read system-guides/README.md for navigation within guides**

---

### 3️⃣ Project Management

**Internal architectural directives and decision frameworks**

Located in: `project-management/`

| File | Purpose |
|------|---------|
| **README.md** | Overview of directives and how they work |
| **[internal] SPEC_PACKAGING_AGENT_PROMPT.md** | Specification decomposition rules |
| **[internal] SPEC_TO_TASK_MARKDOWN_AGENT.txt** | Task extraction rules |
| **[internal] STAKEHOLDER_BOARD_SCOPE_AGENT.txt** | Scope reduction directives |
| **[internal] STAKEHOLDER_DEVELOPER_AGENT.txt** | Quality enforcement rules |

**Authority**: Stakeholder Board  
**Modify With**: Board approval + full justification

**Read project-management/README.md for explanation**

---

### 4️⃣ Update Backlog

**Version-controlled change summaries using US-NNN naming**

Located in: `update-backlog/`

| File | Update | Type |
|------|--------|------|
| **README.md** | Policy & conventions | Documentation |
| **US-000-utils-migration.md** | Utils directory migration | refactor |
| **US-001-directory-reorganization.md** | Directory structure reorganization | refactor |
| **US-002-docs-consolidation.md** | Docs consolidation + Python policy | refactor |

**Format**: `US-[NNN]-[context-a]-[context-b].md`  
**Authority**: Authors (with review)  
**Policy**: See update-backlog/README.md

---

## 🎯 By Use Case

### "I'm a new developer"

1. Read: `system-guides/CONFIGURATION_GUIDE.md` (30 min)
2. Read: `system-guides/DEVELOPMENT_PIPELINE_SUMMARY.md` (30 min)
3. Bookmark: `system-guides/QUICK_REFERENCE.md`
4. Read: `DEVELOPER_AGENT_QUALITY_MANDATE.md` (understand 7 pillars)

**Total Time**: ~2 hours

### "I'm debugging configuration"

Go to: `system-guides/CONFIGURATION_GUIDE.md` → Troubleshooting section

### "I need a quick coding reference"

Bookmark: `system-guides/QUICK_REFERENCE.md`

### "I want to understand decisions"

Read in order:
1. `SCOPE_REDUCTION_SUMMARY.md` (scope decisions)
2. `project-breakdown.md` (architecture decisions)
3. `project-management/README.md` (process decisions)

### "I need to report a change"

1. Read: `update-backlog/README.md` (policy)
2. Create: `update-backlog/US-NNN-context-a-context-b.md`
3. Fill in: Using template from README
4. Commit: With full explanation

### "I'm reviewing code quality"

Reference:
- `DEVELOPER_AGENT_QUALITY_MANDATE.md` (7 pillars)
- `QUALITY_INTEGRATION_SUMMARY.md` (scope integration)
- `system-guides/QUICK_REFERENCE.md` (checklist)

---

## 🔐 Protection & Access

### What's Protected

All files in `.docs/` are **protected**:
- ✅ Cannot modify without change log
- ✅ Modifications require justification
- ✅ Changes tracked in update-backlog/

### Modification Workflow

```bash
# 1. Edit the file
vim PYTHON_ORGANIZATION_POLICY.md

# 2. Create update summary
touch update-backlog/US-NNN-policy-update.md

# 3. Fill in summary with template details

# 4. Commit both together
git add PYTHON_ORGANIZATION_POLICY.md update-backlog/US-NNN-*.md
git commit -m "US-NNN: Update Python organization policy

- Added requirement X
- Clarified rule Y
- Updated enforcement Z

See update-backlog/US-NNN-policy-update.md for details."
```

---

## 📊 Key Statistics

| Category | Count | Purpose |
|----------|-------|---------|
| **Core Governance** | 6 files | Authority documents |
| **System Guides** | 4 files | Developer resources |
| **Project Management** | 5 files | Internal directives |
| **Update Summaries** | 3+ files | Change history |
| **Total** | 18+ files | Complete documentation |

---

## 🔄 Relationship to Other Directories

### .docs/ (This Directory)
**Everything about the project**: governance, guides, history

### packages/
**Specifications and tasks**: What to build

### utils/
**Python code**: How to build it (utilities)

### .claude/
**System configuration**: Build environment settings

### Root Level
**Configuration**: development.cfg, .gitignore  
**Entry point**: __main__.py (future)  
**Metadata**: PROJECT_STRUCTURE.md

---

## 📝 File Types in .docs/

| Type | Examples | Purpose |
|------|----------|---------|
| **.md** | Most files | Markdown documentation |
| **.txt** | Some agent prompts | Text-based directives |
| **/README.md** | In subdirectories | Navigation & explanation |
| **/US-*.md** | In update-backlog/ | Update summaries |

---

## 🚀 Common Tasks

### Create New Guide

```bash
# 1. Draft in system-guides/
vim system-guides/NEW_GUIDE.md

# 2. Create update summary
touch update-backlog/US-NNN-guide-topic.md

# 3. Add to system-guides/README.md

# 4. Commit
git add system-guides/ update-backlog/ 
git commit -m "US-NNN: Add NEW_GUIDE.md"
```

### Report a Change

```bash
# See update-backlog/README.md for detailed policy
touch update-backlog/US-NNN-[context-a]-[context-b].md
# Fill with template, commit
```

### Update a Policy

```bash
# 1. Modify core governance file
vim PYTHON_ORGANIZATION_POLICY.md

# 2. Create detailed update summary
touch update-backlog/US-NNN-policy-change.md

# 3. Commit with explanation
git commit -m "US-NNN: Policy change explanation"
```

---

## 🎓 Learning Path

**First Time?**
1. This README (you're reading it)
2. system-guides/README.md (navigate guides)
3. system-guides/CONFIGURATION_GUIDE.md (setup)
4. DEVELOPER_AGENT_QUALITY_MANDATE.md (standards)

**Need Specific Info?**
- Use Quick Navigation table at top
- Search for keyword in appropriate section

**Making Changes?**
1. Read update-backlog/README.md (policy)
2. Create US-NNN-* file with template
3. Commit with reference

---

## 📞 Questions?

| Question | Answer |
|----------|--------|
| Where are developer guides? | system-guides/ |
| Where are internal directives? | project-management/ |
| How do I report a change? | update-backlog/README.md |
| What's the quality standard? | DEVELOPER_AGENT_QUALITY_MANDATE.md |
| What's out of scope? | SCOPE_REDUCTION_SUMMARY.md |
| How should I organize Python? | PYTHON_ORGANIZATION_POLICY.md |

---

## 🔍 Index by Topic

### Configuration & Setup
- system-guides/CONFIGURATION_GUIDE.md
- development.cfg (in root)
- PYTHON_ORGANIZATION_POLICY.md

### Quality & Standards
- DEVELOPER_AGENT_QUALITY_MANDATE.md
- QUALITY_INTEGRATION_SUMMARY.md
- system-guides/QUICK_REFERENCE.md (quality checklist)

### Architecture & Design
- project-breakdown.md
- SCOPE_REDUCTION_SUMMARY.md
- project-management/README.md

### Processes & Workflows
- project-management/ (directives)
- update-backlog/README.md (change policy)
- system-guides/DEVELOPMENT_PIPELINE_SUMMARY.md

### Change History
- update-backlog/ (all US-* files)
- REDUCTION_NOTES.md (scope history)

---

## 📋 Current Status

✅ **Consolidated**: All docs in .docs/  
✅ **Organized**: 4 clear subdirectories  
✅ **Indexed**: Navigation guides in each subdir  
✅ **Protected**: Access control enforced  
✅ **Versioned**: Changes tracked in update-backlog/  

**Status**: ✅ Production Ready

---

## 🔗 Navigation Links

| Go To | Purpose |
|-------|---------|
| system-guides/README.md | Developer guide navigation |
| project-management/README.md | Internal processes |
| update-backlog/README.md | Change log policy |
| PROJECT_STRUCTURE.md | Overall file structure (in root) |

---

**Last Updated**: 2026-04-10  
**Owner**: Architecture Team  
**Consolidated**: Yes (US-002)  
**Authority**: Stakeholder Board
