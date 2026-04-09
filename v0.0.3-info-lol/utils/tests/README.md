# utils/tests – Test Suite for Utilities

Comprehensive test coverage for all Python utilities in `utils/` directory.

**Test Coverage Target**: >= 80% of code lines, >= 90% of critical paths

---

## Test Organization

```
utils/tests/
├── __init__.py                    ← Package initialization
├── test_markdown_printer.py       ← Tests for markdown_printer.py
├── test_config_loader.py          ← Tests for config_loader.py
└── README.md                      ← This file
```

---

## Test Files

### test_markdown_printer.py

**Purpose**: Comprehensive test coverage for markdown_printer utility

**Test Classes**:
- `TestColorPalette` – Color palette initialization and modes
- `TestMarkdownConfig` – Configuration management
- `TestMarkdownPrinterInit` – Initialization and validation
- `TestMarkdownPrinterMethods` – File reading and rendering methods
- `TestArgumentParser` – CLI argument parsing
- `TestMainFunction` – Main entry point and error handling
- `TestInitialization` – Import verification and startup checks

**Coverage**:
- ✅ Initialization (Pillar 7)
- ✅ Error handling (Pillar 2)
- ✅ Unit tests for all code paths (Pillar 3)
- ✅ Docstrings on all components (Pillar 1)

### test_config_loader.py

**Purpose**: Comprehensive test coverage for config_loader utility

**Test Classes**:
- `TestConfigBasics` – Config class initialization
- `TestConfigGet` – Value retrieval and defaults
- `TestConfigTypeConversion` – Type conversion methods
- `TestConfigSections` – Section iteration
- `TestValidation` – Configuration validation
- `TestInitializeConfig` – Entry point function
- `TestInitialization` – Import verification and startup checks

**Coverage**:
- ✅ Configuration handling (Pillar 5)
- ✅ Error handling (Pillar 2)
- ✅ Type conversion (Pillar 3)
- ✅ Initialization verification (Pillar 7)

---

## Running Tests

### Install Test Dependencies

```bash
pip install pytest pytest-cov
```

### Run All Tests

```bash
# From project root
pytest utils/tests/

# With verbose output
pytest -v utils/tests/

# With coverage report
pytest --cov=utils --cov-report=html utils/tests/
```

### Run Specific Test File

```bash
pytest utils/tests/test_markdown_printer.py
pytest utils/tests/test_config_loader.py
```

### Run Specific Test Class

```bash
pytest utils/tests/test_markdown_printer.py::TestColorPalette
pytest utils/tests/test_config_loader.py::TestConfigGet
```

### Run Specific Test

```bash
pytest utils/tests/test_markdown_printer.py::TestColorPalette::test_color_palette_init_normal_mode
```

---

## Seven Pillars Compliance

Every test file verifies compliance with the **Seven Pillars of Code Quality** from `.docs/DEVELOPER_AGENT_QUALITY_MANDATE.md`:

### Pillar 1: Docstrings & Comments
✅ Tests verify every function and class has descriptive docstrings
- Module docstrings explain purpose
- Function docstrings document Args, Returns, Raises
- Class docstrings describe purpose and behavior

### Pillar 2: Error Handling
✅ Tests verify all external operations have error handling
- File I/O wrapped in try-except
- Configuration missing key handling
- Type conversion validation
- Argument parsing error cases

### Pillar 3: Test Suite
✅ Tests cover all code paths
- Normal operation (happy path)
- Edge cases (empty files, unicode, special characters)
- Error paths (missing files, invalid types)
- Initialization and startup

### Pillar 4: Code Structure
✅ Tests verify code organization
- Functions don't exceed 50 lines
- Modules stay focused (no mixed concerns)
- Clear separation: validation, loading, conversion

### Pillar 5: Configuration & Environment
✅ Tests verify configuration externalization
- No hardcoded values
- Config file loading
- Environment variable override
- Default configuration

### Pillar 6: Logging & Diagnostics
✅ Tests verify logging where applicable
- Error messages are descriptive
- Configuration loading logged
- Validation provides diagnostics

### Pillar 7: Initialization Tests
✅ Tests verify startup requirements
- Imports available
- Classes instantiable
- Dependencies present
- No missing configuration

---

## Test Metrics

### Coverage Goals

| Metric | Goal | Status |
|--------|------|--------|
| **Line Coverage** | >= 80% | ✅ Target |
| **Critical Path Coverage** | >= 90% | ✅ Target |
| **Test Count** | 50+ | ✅ Achieved |
| **Test Classes** | 14 | ✅ Complete |

### Key Test Scenarios

**markdown_printer.py**:
- 25+ unit tests
- Color palette modes (normal, high-contrast)
- File validation and error handling
- Argument parsing (all combinations)
- Rendering and output
- Edge cases (empty files, unicode)

**config_loader.py**:
- 30+ unit tests
- Type conversions (bool, int, float, list)
- Section management
- Configuration loading
- Environment variable override
- Validation and diagnostics

---

## Test Quality Standards

### Each Test Must:

✅ Have a clear, descriptive name (`test_what_it_does`)  
✅ Test one specific behavior (no mega-tests)  
✅ Have comments explaining complex setups  
✅ Use meaningful assertions with context  
✅ Clean up resources (temp files, mocks)  
✅ Handle edge cases and errors  
✅ Be independent (no test order dependencies)  

### Test File Structure:

```python
"""Module docstring with purpose and coverage info."""

import pytest
from module_under_test import *

class TestCategoryName:
    """Test class docstring explaining what's tested."""

    def test_specific_behavior(self):
        """Test docstring explaining what's being tested."""
        # Arrange
        setup = "test data"
        
        # Act
        result = function_under_test(setup)
        
        # Assert
        assert result == expected
```

---

## Mocking Strategy

Tests use `unittest.mock` to:
- Isolate units under test
- Mock file I/O for controlled testing
- Mock Rich library calls (complex dependencies)
- Simulate environment variables
- Control temporary files

Example:
```python
with patch.object(Path, 'exists', return_value=True):
    config = Config()
```

---

## CI/CD Integration

### Pre-commit Hook

```bash
pytest utils/tests/ --cov=utils --cov-fail-under=80
```

If any test fails or coverage drops below 80%, commit is blocked.

### Coverage Report

HTML coverage reports generated:
```bash
pytest --cov=utils --cov-report=html utils/tests/
# Report: htmlcov/index.html
```

---

## Troubleshooting

### Import Errors

```
ModuleNotFoundError: No module named 'markdown_printer'
```

**Fix**: Run from project root, ensure `__init__.py` exists in utils/

### Rich Library Not Found

```
ImportError: No module named 'rich'
```

**Fix**: `pip install rich`

### Test File Not Found

```
Error: file not found: utils/tests/test_*.py
```

**Fix**: Ensure you're in project root directory

---

## Adding New Tests

When adding a new utility to `utils/`:

1. **Create the utility**: `utils/my_utility.py`
2. **Create tests**: `utils/tests/test_my_utility.py`
3. **Target coverage**: >= 80% lines, >= 90% critical paths
4. **Test all 7 pillars**: Every quality aspect verified
5. **Update this README**: Add test information

Example structure:
```python
# utils/tests/test_my_utility.py
"""Test suite for my_utility.py"""

class TestMyUtility:
    def test_initialization(self): ...
    def test_core_function(self): ...
    def test_error_handling(self): ...
    def test_edge_cases(self): ...

class TestInitialization:
    def test_imports_available(self): ...
    def test_classes_instantiable(self): ...
```

---

## References

- **Quality Mandate**: `.docs/DEVELOPER_AGENT_QUALITY_MANDATE.md`
- **Python Policy**: `.docs/PYTHON_ORGANIZATION_POLICY.md`
- **Pytest Docs**: https://docs.pytest.org/
- **unittest.mock**: https://docs.python.org/3/library/unittest.mock.html

---

## Test Statistics

**As of 2026-04-10**:
- Total test files: 2
- Total test classes: 14
- Total test methods: 55+
- Coverage target: 80%+ lines
- Critical path coverage: 90%+
- Dependencies tested: markdown_printer, config_loader

---

**Status**: ✅ Test Suite Complete  
**Last Updated**: 2026-04-10  
**Policy**: US-003-python-test-policy (pending)
