# Project Management – Internal Directives & Agent Prompts

This directory contains internal documentation and agent prompts that define the architectural principles, processes, and decision-making frameworks for The Summoner's Chronicle project.

---

## Contents

### 🏗️ Agent Directives

These are the strict prompts given to agents (AI or human) to decompose specifications, extract tasks, reduce scope, and enforce quality standards.

#### 1. **[internal] SPEC_PACKAGING_AGENT_PROMPT.md**
**Purpose**: Decompose comprehensive specifications into hierarchical markdown packages

**What It Does**:
- Defines how to organize specs into logical modules
- Specifies package hierarchy and nesting rules
- Establishes cross-package navigation patterns
- Enforces consistent formatting

**Used For**: Breaking down the original League of Legends infographic spec into 36 organized markdown files

**Enforces**: Modular organization by concern (overview, visual-design, algorithms, infrastructure)

---

#### 2. **[internal] SPEC_TO_TASK_MARKDOWN_AGENT.txt**
**Purpose**: Extract actionable project management tasks from specification files

**What It Does**:
- Identifies units of work from markdown specs
- Creates standardized task descriptions
- Maps dependencies between tasks
- Assigns effort estimates and roles

**Used For**: Converting 36 specification files into 30 task.md files with ~150 tasks

**Enforces**: Consistent task format, realistic effort estimation, dependency tracking

**Task Format**:
```markdown
- **Task:** [Short title, max 10 words]
  - **Description:** [What needs to be done]
  - **Source:** [Which spec file]
  - **Dependencies:** [List of task titles or "None"]
  - **Estimated effort:** [XS/S/M/L/XL or hours]
  - **Assigned role:** [e.g., "Solo developer (with AI assistance)"]
  - **Milestone:** [MVP or Polish]
```

---

#### 3. **[internal] STAKEHOLDER_BOARD_SCOPE_AGENT.txt**
**Purpose**: Reduce project scope to be feasible for a solo developer with AI assistance

**What It Does**:
- Applies explicit scope reduction directives
- Removes out-of-scope items (localization, colorblind palettes, etc.)
- Simplifies specialist roles to solo developer tasks
- Consolidates milestones (many phases → MVP + Polish)

**Used For**: Reducing 85+ tasks (~800 hours) to 55 tasks (~350 hours)

**Enforces**:
- Out-of-scope items explicitly listed
- Effort estimates reduced appropriately
- All tasks assigned to "Solo developer (with AI assistance)"
- Only 2 milestones: MVP and Polish

---

#### 4. **[internal] STAKEHOLDER_DEVELOPER_AGENT.txt**
**Purpose**: Create quality enforcement standards for developer agents

**What It Does**:
- Defines 7 pillars of code quality
- Specifies pre-delivery checklists
- Creates quality report requirements
- Establishes mandatory compliance gates

**Used For**: Generating the DEVELOPER_AGENT_QUALITY_MANDATE.md

**Enforces**: No code accepted without:
- Docstrings on all modules/functions
- Error handling on external calls
- Test coverage ≥80% (lines) and ≥90% (critical paths)
- Code structure limits (functions ≤50 lines, modules ≤10 functions)
- Configuration externalization
- Comprehensive logging
- Initialization test suite

---

## How to Use These Directives

### For Architects

Read these to understand:
- How specifications are decomposed
- How tasks are extracted and estimated
- What scope decisions were made and why
- What quality standards are non-negotiable

### For Project Managers

Use these to:
- Understand task generation rules
- Review scope reduction rationale
- Verify effort estimates are realistic
- Ensure quality gates are enforced

### For Developers

These define the requirements you must meet:
- Quality mandate from STAKEHOLDER_DEVELOPER_AGENT
- Task format from SPEC_TO_TASK_MARKDOWN_AGENT
- Scope boundaries from STAKEHOLDER_BOARD_SCOPE_AGENT

### For AI Agents

These are actual prompts that agents follow to:
- Extract specifications into tasks
- Reduce scope appropriately
- Enforce quality standards
- Generate documentation

---

## Relationship to Other Documents

### Core Governance (.docs/)
- **DEVELOPER_AGENT_QUALITY_MANDATE.md** ← Generated FROM [internal] STAKEHOLDER_DEVELOPER_AGENT.txt
- **SCOPE_REDUCTION_SUMMARY.md** ← Results from [internal] STAKEHOLDER_BOARD_SCOPE_AGENT.txt

### Tasks (packages/*/tasks.md)
- Generated FROM [internal] SPEC_TO_TASK_MARKDOWN_AGENT.txt rules
- Using [internal] STAKEHOLDER_BOARD_SCOPE_AGENT.txt reductions
- Must meet quality standards from [internal] STAKEHOLDER_DEVELOPER_AGENT.txt

### Specifications (packages/*/README.md)
- Generated FROM [internal] SPEC_PACKAGING_AGENT_PROMPT.md rules
- Decomposed into hierarchical packages and sub-packages

---

## Workflow

### How It All Works Together

```
Original Specification
        ↓
SPEC_PACKAGING_AGENT_PROMPT.md
        ↓
36 Organized Specification Files (packages/)
        ↓
SPEC_TO_TASK_MARKDOWN_AGENT.txt
        ↓
150+ Tasks (packages/*/tasks.md)
        ↓
STAKEHOLDER_BOARD_SCOPE_AGENT.txt
        ↓
55 Scoped Tasks (~350 hours) (MVP + Polish)
        ↓
STAKEHOLDER_DEVELOPER_AGENT.txt
        ↓
DEVELOPER_AGENT_QUALITY_MANDATE.md (7 pillars)
        ↓
Quality-Enforced Implementation
```

---

## Using These Prompts for Future Work

### To Extract New Tasks

1. Read: [internal] SPEC_TO_TASK_MARKDOWN_AGENT.txt
2. Identify units of work in spec files
3. Create tasks following the template
4. Estimate effort (XS/S/M/L/XL)
5. Assign role: "Solo developer (with AI assistance)"
6. Set milestone: MVP or Polish

### To Reduce New Scope

1. Read: [internal] STAKEHOLDER_BOARD_SCOPE_AGENT.txt
2. Apply explicit out-of-scope directives
3. Simplify tasks from specialist roles to solo roles
4. Reduce effort estimates appropriately
5. Document in SCOPE_REDUCTION_SUMMARY.md

### To Enforce Quality

1. Read: [internal] STAKEHOLDER_DEVELOPER_AGENT.txt
2. Use 7 pillars in code review
3. Require quality reports before task completion
4. Enforce pre-delivery checklist
5. Update DEVELOPER_AGENT_QUALITY_MANDATE.md if needed

---

## Authority & Governance

**Source**: Stakeholder Board Decisions (documented 2026-04-10)

**Authority**:
- SPEC_PACKAGING_AGENT_PROMPT.md ← Architecture authority
- SPEC_TO_TASK_MARKDOWN_AGENT.txt ← Project management authority
- STAKEHOLDER_BOARD_SCOPE_AGENT.txt ← Executive board decision
- STAKEHOLDER_DEVELOPER_AGENT.txt ← Quality authority

**Enforcement**: 
- Settings.json enforces these directives through protected files
- Code reviews verify compliance with DEVELOPER_AGENT_QUALITY_MANDATE.md
- Task completion gates verify all directives are met

---

## Updating These Directives

**Important**: These directives should rarely change. They represent:
- Fundamental architectural decisions
- Scope reduction board decisions
- Quality standards

**To Update**:
1. Document rationale for change
2. Create US-* update summary in update-backlog/
3. Update corresponding .docs/ file (if applicable)
4. Commit with full explanation
5. Notify stakeholders

**Example**:
```bash
# Change directive
vim "[internal] STAKEHOLDER_DEVELOPER_AGENT.txt"

# Document update
touch ../update-backlog/US-NNN-quality-update.md

# Commit
git add "[internal] STAKEHOLDER_DEVELOPER_AGENT.txt" ../update-backlog/US-NNN-*.md
git commit -m "US-NNN: Update quality mandate

[Explanation of why directive changed]

See update-backlog/US-NNN-quality-update.md"
```

---

## Protection & Access

These files are **protected** in .claude/settings.json:
- ✅ Cannot be modified without change log
- ✅ Modifications require justification
- ✅ Changes are tracked in update-backlog/

**Modification Workflow**:
1. Create branch
2. Modify directive
3. Create update-backlog/US-* summary
4. Commit with explanation
5. Require review before merge

---

## References

**See Also**:
- .docs/DEVELOPER_AGENT_QUALITY_MANDATE.md (generated from STAKEHOLDER_DEVELOPER_AGENT.txt)
- .docs/SCOPE_REDUCTION_SUMMARY.md (results from STAKEHOLDER_BOARD_SCOPE_AGENT.txt)
- .docs/project-breakdown.md (architectural decisions)
- packages/ (specifications organized per SPEC_PACKAGING_AGENT_PROMPT.md)
- packages/*/tasks.md (tasks extracted per SPEC_TO_TASK_MARKDOWN_AGENT.txt)

---

## Version Info

**Last Updated**: 2026-04-10  
**Owner**: Stakeholder Board  
**Authority**: Architecture & Project Management  
**Status**: ✅ Production Directives
