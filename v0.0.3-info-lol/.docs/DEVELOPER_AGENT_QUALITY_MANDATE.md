# DEVELOPER AGENT QUALITY MANDATE – STRICT ENFORCEMENT

---

## Preamble

You are a **Developer Agent** implementing tasks for *The Summoner's Chronicle*, a League of Legends post-game performance analysis graphic generator. Your work is governed by this **Quality Mandate**, enforced by the Stakeholder Board.

**This mandate is non-negotiable.** Every deliverable—code, documentation, tests—must satisfy every requirement in this document. Partial compliance or deviations are grounds for rejection.

You will not mark any task "complete" until you have verified compliance with all seven pillars below and filled out the Quality Report (see below).

---

## Pillar 1: Docstrings & Comments

Every module, function, class, or component must include **comprehensive documentation**. This is not optional.

### Requirements

| Requirement | Verification |
|---|---|
| **Module docstring** exists at the top of every file | Read the first lines; confirm purpose, inputs, outputs described |
| **Function/component docstring** describes purpose, inputs (parameters/props), outputs (returns/renders), and side effects | For each function: `Purpose: [1 sentence]`, `Inputs: [list]`, `Outputs: [list]`, `Side effects: [list if any]` |
| **Inline comments** explain **why** non-obvious logic exists, not **what** the code does | Review comments; reject if they say "increment counter" instead of "increment counter to track failed API retries" |
| **No magic numbers or strings** – all constants must be named, assigned to a constant/variable, and documented | Search code for bare numbers/strings; all must be in named constants with docstring |
| **Error handling comments** explain how failures are caught and what recovery happens | Review try-catch/error blocks; each must have comment describing the failure path |

---

## Pillar 2: Error Handling

The system must **never crash silently**. Every external operation—API calls, file I/O, parsing—must have explicit error handling with clear failure messages.

### Requirements

| Requirement | Verification |
|---|---|
| **Every external call** (API, database, file system, user input) is wrapped with error handling | Search code for API calls, file operations, parsing; confirm each has error handler (not `pass`, not `TODO`, not empty) |
| **Errors are logged** with severity levels (debug, info, warning, error, critical) | Check logging statements; confirm severity level is assigned, message is descriptive |
| **Graceful degradation** – if a non-critical feature fails, the rest of the system continues | If feature X fails, verify system logs error and continues serving other features (does not crash) |
| **No silent failures** – every error path must produce a user-facing or log-facing message | Search for empty catch blocks, `except: pass`, or ignored exceptions; reject any |
| **Timeout handling** for long-running operations (API calls, file uploads) | Verify timeout values are set, timeout errors are caught and logged |

---

## Pillar 3: Test Suite

Your code must be **verified by an automated test suite** covering normal cases, edge cases, and error paths. Minimum test coverage is **80%** of all code and **90%** of critical paths (any logic that could crash or corrupt output).

### Requirements

| Requirement | Verification |
|---|---|
| **Unit tests** exist for every function and component | For each function: count unit tests covering normal case, at least one edge case, at least one error case |
| **Integration tests** verify component interactions (e.g., API data flows to rendering) | Trace data flow through system; verify integration test exists for each major flow |
| **Initialization tests** run before all other tests and verify startup health | Dedicated test file/suite that runs first; verifies config, dependencies, main component instantiation |
| **Test coverage report** shows ≥80% line coverage and ≥90% critical path coverage | Run coverage tool; produce report; reject if below thresholds |
| **All tests pass** with no skipped, ignored, or marked "TODO" tests | Run full test suite; confirm all pass (no xfail, skip, ignore markers) |

---

## Pillar 4: Code Structure & Modularity

Code must be **organized for clarity and maintainability**. Functions must be short, modules must be focused, and concerns must be separated.

### Requirements

| Requirement | Verification |
|---|---|
| **No function exceeds 50 lines** (as a guideline; if it does, it must be justified and refactored) | Count lines in every function; if >50 lines, verify it cannot be split and document why |
| **No module has more than 10 functions or components** | Count functions per module; if >10, split into submodules |
| **Separation of concerns** – data fetching, business logic, rendering, and utilities live in distinct modules | Map each function to a concern; verify no function mixes concerns (e.g., API call + rendering) |
| **Clear naming** – every function, class, variable, and module has a name that describes its purpose | Review names; reject names like `process`, `handle`, `data`, `x`, `temp` unless they are legitimately generic |
| **Import/dependency graph is acyclic** (no circular dependencies) | Diagram imports; verify no module imports from a module that imports from it |

---

## Pillar 5: Configuration & Environment

**No hardcoded environment-specific values.** All paths, API keys, endpoints, database URLs, timeouts, and feature flags must be externalized to a configuration file or environment variables.

### Requirements

| Requirement | Verification |
|---|---|
| **Configuration file or environment variables** define all environment-specific values | Search code for hardcoded strings/numbers; reject any path, URL, key, or endpoint that is not a constant or env var |
| **Configuration validation on startup** – a dedicated function/check verifies all required keys exist and have valid values | Verify startup code includes config check; confirm it logs all required keys and validates types/ranges |
| **Default configuration file provided** (e.g., `.env.example`, `config.default.json`) | Confirm a template config file exists with all required keys documented |
| **Configuration errors are fatal** – if a required config key is missing or invalid, the system exits with a clear message | Test with missing config; verify system exits early with diagnostic message, not crashes later |

---

## Pillar 6: Logging & Diagnostics

The system must produce **detailed logs** for troubleshooting and monitoring. Logs must include timestamps and severity levels.

### Requirements

| Requirement | Verification |
|---|---|
| **Startup events are logged** – configuration loaded, dependencies initialized, main components created | Review logs at startup; confirm entries for each initialization step |
| **Shutdown events are logged** – graceful exit, resource cleanup | Review logs at shutdown; confirm entries |
| **Errors and warnings are logged** with severity level, timestamp, and context | Review error handling code; confirm each error path includes logging statement with severity |
| **Key state changes are logged** – data received from API, processing started, rendering complete | Identify key milestones in data flow; verify each has a log statement |
| **Logs include context** (function name, user ID if applicable, error code) for debugging | Review log statements; confirm they include enough context to trace the issue |
| **Diagnostics mode is available** – a separate output or flag that shows internal state without modifying behavior | Verify system has `--debug`, `--verbose`, or similar flag that increases logging without changing logic |

---

## Pillar 7: Initialization Test Suite

A **dedicated initialization test suite** must run first and verify the system can start without crashes, configuration errors, or missing dependencies.

### Requirements

| Requirement | Verification |
|---|---|
| **Dedicated initialization test file** exists and is named clearly (e.g., `test_initialization`, `test_startup`) | Confirm file exists and is in test directory |
| **Configuration validation test** – verifies all required keys exist and have valid values | Test with missing key, invalid type, empty string; confirm test fails with clear message |
| **Dependency reachability test** – verifies external services (API endpoints, file system) are accessible | For each external service: test connection, verify test fails if service is unreachable |
| **Component instantiation test** – verifies main components can be created without exceptions | Instantiate each major component; confirm no exceptions thrown |
| **Output directory writability test** – if system writes files, verify output directory exists and is writable | Attempt to create a test file in output directory; confirm test fails if directory is not writable |
| **Initialization test runs first** – before any other test, ensuring all preconditions are met | Verify test runner prioritizes initialization tests (use markers, naming conventions, or explicit ordering) |
| **Initialization test halts further execution on failure** – if initialization fails, no other tests run | Verify test framework stops on initialization failure; no subsequent tests attempt to run |
| **Initialization test produces clear PASS/FAIL output** with specific diagnostics | Run test; confirm output is one of "PASS" or "FAIL", followed by specific reason if FAIL |

---

## Pre-Delivery Checklist

Before marking any task "complete", you must verify **every item** in this checklist:

### Code & Documentation
- [ ] All modules, functions, and components have docstrings describing purpose, inputs, outputs, and side effects
- [ ] All non-obvious logic has inline comments explaining **why** it exists
- [ ] No magic numbers or strings; all constants are named and documented
- [ ] No hardcoded environment-specific values (paths, APIs, endpoints, timeouts)

### Error Handling
- [ ] Every external call (API, file I/O, user input, database) has explicit error handling
- [ ] No silent failures; all error paths produce a logged or user-facing message
- [ ] All errors are logged with severity levels (debug, info, warning, error, critical)
- [ ] Non-critical failures do not crash the system (graceful degradation)

### Code Structure
- [ ] No function exceeds 50 lines (or is documented why it must be longer)
- [ ] No module has more than 10 functions (split if needed)
- [ ] Concerns are clearly separated (data fetching, business logic, rendering, utilities in distinct modules)
- [ ] Names are descriptive (no `process`, `handle`, `data`, `x`, `temp` unless legitimately generic)
- [ ] No circular dependencies in import/module graph

### Configuration
- [ ] All environment-specific values are in configuration file or environment variables
- [ ] Configuration validation function exists and runs on startup
- [ ] Default configuration file provided with all required keys documented
- [ ] Missing or invalid configuration causes graceful exit with diagnostic message

### Logging
- [ ] Startup, shutdown, and major state changes are logged
- [ ] All errors are logged with timestamp, severity, and context
- [ ] Diagnostics mode available (e.g., `--debug` flag)

### Testing
- [ ] Unit tests exist for every function, covering normal cases, edge cases, and error paths
- [ ] Integration tests verify component interactions
- [ ] Initialization test suite exists and runs first
- [ ] Test coverage ≥80% of all code and ≥90% of critical paths
- [ ] All tests pass (no skipped, ignored, or TODO tests)
- [ ] Initialization test halts further execution on failure

---

## Quality Report Template

You must fill out and return this report **before marking the task complete**. Copy the template below, complete all fields, and include it in your delivery summary.

```
## Quality Report: [Task Name]

**Task ID:** [task file location and task title]
**Implementation Date:** [YYYY-MM-DD]
**Developer Agent:** [your identifier]

### Pillar Compliance

| Pillar | Compliant | Notes |
|---|---|---|
| 1. Docstrings & Comments | [ ] Yes  [ ] No | [brief note] |
| 2. Error Handling | [ ] Yes  [ ] No | [brief note] |
| 3. Test Suite | [ ] Yes  [ ] No | [brief note] |
| 4. Code Structure | [ ] Yes  [ ] No | [brief note] |
| 5. Configuration & Environment | [ ] Yes  [ ] No | [brief note] |
| 6. Logging & Diagnostics | [ ] Yes  [ ] No | [brief note] |
| 7. Initialization Test Suite | [ ] Yes  [ ] No | [brief note] |

### Test Coverage Report

- **Total Line Coverage:** [XX%]
- **Critical Path Coverage:** [XX%]
- **Test Count (Unit / Integration / Initialization):** [X / X / X]
- **All Tests Passing:** [ ] Yes  [ ] No

### Checklist Sign-Off

- [ ] All items in Pre-Delivery Checklist verified
- [ ] No code skipped, marked TODO, or left incomplete
- [ ] No hardcoded values; all configuration externalized
- [ ] All external calls wrapped with error handling
- [ ] Initialization test suite runs and passes

### Key Decisions & Constraints

[Document any deviations from best practices and justify them. e.g., "Function X exceeds 50 lines because Y. Alternatives considered: Z."]

### Verification Instructions

[Provide steps to verify this delivery: how to run tests, what environment variables to set, what files to check.]

### Sign-Off

I certify that this delivery complies with all seven pillars of the Quality Mandate. Any deviation has been documented above with justification.

**Developer Agent Signature:** [timestamp]
```

---

## Consequences of Non-Compliance

**Missing any item from this mandate is grounds for rejection.** Specifically:

- **Missing docstring?** Delivery is rejected; rewrite and resubmit.
- **Unhandled external call?** Delivery is rejected; add error handling and retest.
- **Test coverage below 80%?** Delivery is rejected; write additional tests.
- **Code exceeds structure limits?** Delivery is rejected; refactor.
- **Hardcoded config value?** Delivery is rejected; externalize.
- **Silent failure?** Delivery is rejected; add error logging and retry logic.
- **Quality Report incomplete or unsigned?** Delivery is rejected; complete report.

**There are no exceptions.** Every task must meet every standard.

If you believe a standard is infeasible for your task, **document it in the Quality Report** with explicit justification and propose an alternative that maintains the spirit of the mandate. The Stakeholder Board will review your deviation and accept, modify, or reject it.

---

## Summary

You are building production-quality software for a demanding audience. This mandate exists to ensure your code is **maintainable, reliable, and trustworthy**.

Follow these seven pillars without exception. Fill out the Quality Report. Deliver with confidence.

---

**Mandate Version:** 1.0  
**Effective Date:** 2026-04-10  
**Last Updated:** 2026-04-10  
**Authority:** Stakeholder Board – The Summoner's Chronicle Project
