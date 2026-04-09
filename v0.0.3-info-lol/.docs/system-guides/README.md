# System Guides – Developer Documentation

This directory contains user-facing guides and reference material for The Summoner's Chronicle development system.

## Quick Links

### 📋 Setup & Configuration
- **[CONFIGURATION_GUIDE.md](CONFIGURATION_GUIDE.md)** – Complete setup guide for development environment
  - How to create local configuration
  - Getting API keys
  - Type-safe config access in code
  - Troubleshooting configuration issues

### 📊 Overview & Architecture
- **[DEVELOPMENT_PIPELINE_SUMMARY.md](DEVELOPMENT_PIPELINE_SUMMARY.md)** – High-level project overview
  - Architecture layers overview
  - Development workflow phases
  - Project metrics and statistics
  - Getting started checklist
  - File structure reference

### ⚡ Quick Reference
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** – Developer cheat sheet (printable)
  - Essential commands
  - 7 pillars of quality (quick version)
  - Common mistakes
  - File locations
  - Key numbers and timelines

---

## Purpose

These guides are designed for:
- **New developers**: Start here for setup and onboarding
- **Active developers**: Use QUICK_REFERENCE.md while coding
- **Architects**: See DEVELOPMENT_PIPELINE_SUMMARY.md for system design
- **Maintainers**: Reference CONFIGURATION_GUIDE.md for troubleshooting

---

## Navigation

### By Use Case

**"I'm new and just getting started"**
→ Read in this order:
1. DEVELOPMENT_PIPELINE_SUMMARY.md (Overview, 30 min)
2. CONFIGURATION_GUIDE.md (Setup, 30 min)
3. QUICK_REFERENCE.md (Bookmark for daily use)

**"I'm debugging configuration issues"**
→ Go to: CONFIGURATION_GUIDE.md → Troubleshooting section

**"I need a quick reference while coding"**
→ Use: QUICK_REFERENCE.md (print or bookmark)

**"I want to understand the system architecture"**
→ Read: DEVELOPMENT_PIPELINE_SUMMARY.md → Architecture Layers

---

## File Details

| File | Lines | Purpose | Audience |
|------|-------|---------|----------|
| CONFIGURATION_GUIDE.md | 400+ | Configuration setup and usage | Developers |
| DEVELOPMENT_PIPELINE_SUMMARY.md | 500+ | System overview and architecture | Everyone |
| QUICK_REFERENCE.md | 300+ | Developer cheat sheet | Active developers |

---

## Updating These Guides

Any changes to these guides must be:
1. Documented in update-backlog/ with a new US-* summary
2. Include change log entry explaining the update
3. Follow the naming convention: US-NNN-context-a-context-b.md

**Example workflow**:
```bash
# 1. Update the guide
vim CONFIGURATION_GUIDE.md

# 2. Create update summary
touch ../update-backlog/US-002-config-guide-update.md

# 3. Fill in update details
# 4. Commit both together
git add CONFIGURATION_GUIDE.md ../update-backlog/US-002-*.md
git commit -m "US-002: Update CONFIGURATION_GUIDE.md with new section

- Added troubleshooting for import errors
- Clarified environment variable priority
- Added Docker setup example

See update-backlog/US-002-config-guide-update.md for details."
```

See [update-backlog/README.md](../update-backlog/README.md) for the update backlog policy.

---

## Related Documentation

**Core Governance** (.docs/):
- DEVELOPER_AGENT_QUALITY_MANDATE.md – Quality standards
- project-breakdown.md – Architecture and timeline
- SCOPE_REDUCTION_SUMMARY.md – Scope decisions

**Project Management** (project-management/):
- Internal agent directives
- Specification packaging rules
- Scope reduction rules

**Update Backlog** (update-backlog/):
- US-000-utils-migration.md – Utils directory move
- US-001-directory-reorganization.md – This reorganization
- README.md – Update backlog policy

---

## Version Info

**Last Updated**: 2026-04-10  
**Status**: ✅ Production Ready  
**Owner**: Architecture Team
