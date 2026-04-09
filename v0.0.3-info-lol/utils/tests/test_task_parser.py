"""Test suite for task_parser utility with Rich formatting.

Covers parsing, rendering, error handling, and all seven pillars of quality.

Test Classes:
- TestTaskStatus: Enum value verification
- TestTaskMetadata: Data structure initialization
- TestTaskColor: Color palette mappings
- TestTaskParserInit: File validation and initialization
- TestTaskParserParsing: Task extraction and metadata parsing
- TestTaskParserRendering: Rich output generation
- TestMainFunction: CLI entry point with error handling
- TestInitialization: Module imports and dependencies
"""

import tempfile
from pathlib import Path
from unittest import mock

import pytest

from utils.task_parser import (
    TaskColor,
    TaskMetadata,
    TaskParser,
    TaskStatus,
    main,
)


class TestTaskStatus:
    """Test TaskStatus enumeration."""

    def test_all_status_values_defined(self):
        """Verify all task status values exist."""
        assert TaskStatus.PENDING.value == "pending"
        assert TaskStatus.IN_PROGRESS.value == "in_progress"
        assert TaskStatus.COMPLETED.value == "completed"
        assert TaskStatus.BLOCKED.value == "blocked"

    def test_status_enum_members(self):
        """Verify TaskStatus has expected members."""
        members = list(TaskStatus)
        assert len(members) == 4
        assert TaskStatus.PENDING in members


class TestTaskMetadata:
    """Test TaskMetadata data class."""

    def test_minimal_task_creation(self):
        """Create task with minimal required fields."""
        task = TaskMetadata(title="Test Task", description="Test description")
        assert task.title == "Test Task"
        assert task.description == "Test description"
        assert task.status == TaskStatus.PENDING

    def test_full_task_creation(self):
        """Create task with all fields populated."""
        task = TaskMetadata(
            title="Full Task",
            description="Complete description",
            source="packages/test.md",
            dependencies="Task A, Task B",
            effort="M (9-12 hours)",
            quality_required=True,
            role="Solo developer",
            milestone="MVP",
            status=TaskStatus.IN_PROGRESS,
        )
        assert task.title == "Full Task"
        assert task.quality_required is True
        assert task.milestone == "MVP"
        assert task.status == TaskStatus.IN_PROGRESS

    def test_default_status_is_pending(self):
        """Verify default status is PENDING."""
        task = TaskMetadata(title="Task", description="Desc")
        assert task.status == TaskStatus.PENDING

    def test_quality_required_flag(self):
        """Test quality mandate flag."""
        task_without = TaskMetadata(title="T", description="D", quality_required=False)
        task_with = TaskMetadata(title="T", description="D", quality_required=True)
        assert task_without.quality_required is False
        assert task_with.quality_required is True


class TestTaskColor:
    """Test TaskColor semantic color palette."""

    def test_effort_color_small(self):
        """Color for small effort tasks."""
        color = TaskColor.effort_color("S (6-10 hours)")
        assert color == TaskColor.EFFORT_SMALL

    def test_effort_color_medium(self):
        """Color for medium effort tasks."""
        color = TaskColor.effort_color("M (9-22 hours)")
        assert color == TaskColor.EFFORT_MEDIUM

    def test_effort_color_large(self):
        """Color for large effort tasks."""
        color = TaskColor.effort_color("L (16-26 hours)")
        assert color == TaskColor.EFFORT_LARGE

    def test_effort_color_xlarge(self):
        """Color for extra-large effort tasks."""
        color = TaskColor.effort_color("XL (26-40 hours)")
        assert color == TaskColor.EFFORT_XLARGE

    def test_effort_color_none(self):
        """Handle None effort gracefully."""
        color = TaskColor.effort_color(None)
        assert color == "white"

    def test_effort_color_empty_string(self):
        """Handle empty string effort gracefully."""
        color = TaskColor.effort_color("")
        assert color == "white"

    def test_milestone_color_mvp(self):
        """Color for MVP milestone."""
        color = TaskColor.milestone_color("MVP")
        assert color == TaskColor.MILESTONE_MVP

    def test_milestone_color_polish(self):
        """Color for Polish milestone."""
        color = TaskColor.milestone_color("Polish")
        assert color == TaskColor.MILESTONE_POLISH

    def test_milestone_color_future(self):
        """Color for Future milestone."""
        color = TaskColor.milestone_color("Future")
        assert color == TaskColor.MILESTONE_FUTURE

    def test_milestone_color_none(self):
        """Handle None milestone gracefully."""
        color = TaskColor.milestone_color(None)
        assert color == "white"

    def test_color_constants_defined(self):
        """Verify all color constants are strings."""
        assert isinstance(TaskColor.EFFORT_SMALL, str)
        assert isinstance(TaskColor.STATUS_COMPLETED, str)
        assert isinstance(TaskColor.MILESTONE_MVP, str)


class TestTaskParserInit:
    """Test TaskParser initialization and validation."""

    def test_valid_initialization(self):
        """Initialize parser with valid tasks.md path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            test_file = tmppath / "tasks.md"
            test_file.write_text("# Tasks\n")

            parser = TaskParser(str(test_file))
            assert parser.file_path == test_file
            assert parser.tasks == []

    def test_file_not_found_error(self):
        """Raise FileNotFoundError for missing file."""
        with pytest.raises(FileNotFoundError):
            TaskParser("nonexistent/tasks.md")

    def test_invalid_extension_error(self):
        """Raise ValueError for wrong file extension."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            test_file = tmppath / "tasks.txt"
            test_file.write_text("# Tasks\n")

            with pytest.raises(ValueError, match="Invalid file type"):
                TaskParser(str(test_file))

    def test_parser_repr(self):
        """Verify string representation includes file and task count."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            test_file = tmppath / "tasks.md"
            test_file.write_text("# Tasks\n")

            parser = TaskParser(str(test_file))
            repr_str = repr(parser)
            assert "TaskParser" in repr_str
            assert "tasks=0" in repr_str


class TestTaskParserParsing:
    """Test task extraction and parsing."""

    def test_parse_single_task(self):
        """Parse single task from markdown."""
        content = """# Tasks
- **Task:** Simple Task
  - **Description:** Test description
  - **Estimated effort:** M (9-12 hours)
  - **Milestone:** MVP
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            test_file = tmppath / "tasks.md"
            test_file.write_text(content)

            parser = TaskParser(str(test_file))
            parser.parse()
            assert len(parser.tasks) == 1
            assert parser.tasks[0].title == "Simple Task"
            assert parser.tasks[0].effort == "M (9-12 hours)"

    def test_parse_multiple_tasks(self):
        """Parse multiple tasks from markdown."""
        content = """# Tasks
- **Task:** Task One
  - **Description:** First task

- **Task:** Task Two
  - **Description:** Second task

- **Task:** Task Three
  - **Description:** Third task
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            test_file = tmppath / "tasks.md"
            test_file.write_text(content)

            parser = TaskParser(str(test_file))
            parser.parse()
            assert len(parser.tasks) == 3

    def test_parse_quality_mandate_detection(self):
        """Detect quality mandate requirement in description."""
        content = """# Tasks
- **Task:** Mandated Task
  - **Description:** [Quality Mandate Required] Task with requirements
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            test_file = tmppath / "tasks.md"
            test_file.write_text(content)

            parser = TaskParser(str(test_file))
            parser.parse()
            assert parser.tasks[0].quality_required is True

    def test_parse_all_fields(self):
        """Parse task with all metadata fields."""
        content = """# Tasks
- **Task:** Full Task
  - **Description:** [Quality Mandate Required] Complete task
  - **Source:** packages/test.md
  - **Dependencies:** Task A, Task B
  - **Estimated effort:** XL (26-40 hours)
  - **Assigned role:** Solo developer
  - **Milestone:** MVP
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            test_file = tmppath / "tasks.md"
            test_file.write_text(content)

            parser = TaskParser(str(test_file))
            parser.parse()
            task = parser.tasks[0]
            assert task.title == "Full Task"
            assert task.source == "packages/test.md"
            assert "Task A" in task.dependencies
            assert task.effort == "XL (26-40 hours)"
            assert task.role == "Solo developer"
            assert task.milestone == "MVP"
            assert task.quality_required is True

    def test_parse_empty_file(self):
        """Handle empty markdown file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            test_file = tmppath / "tasks.md"
            test_file.write_text("")

            parser = TaskParser(str(test_file))
            parser.parse()
            assert len(parser.tasks) == 0

    def test_parse_no_tasks_in_header(self):
        """Handle file with header but no tasks."""
        content = "# Tasks\n\nNo tasks defined yet.\n"
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            test_file = tmppath / "tasks.md"
            test_file.write_text(content)

            parser = TaskParser(str(test_file))
            parser.parse()
            assert len(parser.tasks) == 0


class TestTaskParserRendering:
    """Test Rich rendering output."""

    def test_render_with_tasks(self):
        """Render task list with populated tasks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            test_file = tmppath / "tasks.md"
            test_file.write_text("""# Tasks
- **Task:** Test Task
  - **Description:** Test description
  - **Milestone:** MVP
""")
            parser = TaskParser(str(test_file))
            parser.parse()

            # Mock console to avoid terminal output
            with mock.patch.object(parser.console, "print"):
                parser.render()  # Should not raise

    def test_render_without_parsing(self):
        """Handle render without parse - should warn."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            test_file = tmppath / "tasks.md"
            test_file.write_text("# Tasks\n")

            parser = TaskParser(str(test_file))
            # Don't call parse()
            with mock.patch.object(parser.console, "print"):
                parser.render()  # Should handle gracefully


class TestMainFunction:
    """Test CLI entry point."""

    def test_main_success(self):
        """Main function succeeds with valid tasks file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            test_file = tmppath / "tasks.md"
            test_file.write_text("""# Tasks
- **Task:** CLI Test
  - **Description:** Testing main function
""")
            # Change to temp directory to find tasks.md
            with mock.patch("utils.task_parser.TaskParser") as mock_parser_class:
                mock_instance = mock.Mock()
                mock_parser_class.return_value = mock_instance
                result = main()
                assert result == 0
                mock_instance.parse.assert_called_once()
                mock_instance.render.assert_called_once()

    def test_main_file_not_found(self):
        """Main returns 1 on FileNotFoundError."""
        with mock.patch("utils.task_parser.TaskParser") as mock_parser_class:
            mock_parser_class.side_effect = FileNotFoundError("Not found")
            result = main()
            assert result == 1

    def test_main_invalid_file(self):
        """Main returns 1 on ValueError."""
        with mock.patch("utils.task_parser.TaskParser") as mock_parser_class:
            mock_parser_class.side_effect = ValueError("Invalid")
            result = main()
            assert result == 1

    def test_main_unexpected_error(self):
        """Main returns 1 on unexpected error."""
        with mock.patch("utils.task_parser.TaskParser") as mock_parser_class:
            mock_parser_class.side_effect = RuntimeError("Unexpected")
            result = main()
            assert result == 1


class TestInitialization:
    """Test module imports and dependencies."""

    def test_imports_available(self):
        """Verify all required imports load successfully."""
        from utils import task_parser

        assert hasattr(task_parser, "TaskStatus")
        assert hasattr(task_parser, "TaskMetadata")
        assert hasattr(task_parser, "TaskColor")
        assert hasattr(task_parser, "TaskParser")
        assert hasattr(task_parser, "main")

    def test_rich_library_available(self):
        """Verify Rich library is installed."""
        import rich
        assert hasattr(rich, "console")

    def test_classes_instantiable(self):
        """Verify key classes can be instantiated."""
        # TaskStatus enum
        assert TaskStatus.PENDING is not None

        # TaskMetadata
        task = TaskMetadata(title="Test", description="Test")
        assert task is not None

    def test_task_color_palette_complete(self):
        """Verify all color palette attributes defined."""
        assert TaskColor.EFFORT_SMALL
        assert TaskColor.STATUS_COMPLETED
        assert TaskColor.MILESTONE_MVP
        assert TaskColor.QUALITY_REQUIRED
