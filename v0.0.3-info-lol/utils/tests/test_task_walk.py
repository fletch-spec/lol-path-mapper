"""Test suite for task_walk utility with recursive project discovery.

Covers directory traversal, multi-file parsing, grouping, and rendering.

Test Classes:
- TestTaskOrganization: Grouping strategy enum
- TestProjectTask: Enhanced task with source info
- TestTaskWalkerInit: Initialization and validation
- TestTaskWalkerDiscovery: Finding and parsing task files
- TestTaskWalkerGrouping: Organizing tasks by role/department
- TestTaskWalkerRendering: Rich output generation
- TestMainFunction: CLI entry point
- TestInitialization: Module imports and dependencies
"""

import tempfile
from pathlib import Path
from unittest import mock

import pytest

from utils.task_walk import (
    ProjectTask,
    TaskOrganization,
    TaskWalker,
    main,
)


class TestTaskOrganization:
    """Test TaskOrganization enum."""

    def test_all_organization_strategies(self):
        """Verify all organization strategies defined."""
        assert TaskOrganization.BY_ROLE.value == "role"
        assert TaskOrganization.BY_DEPARTMENT.value == "department"
        assert TaskOrganization.BY_MILESTONE.value == "milestone"
        assert TaskOrganization.BY_STATUS.value == "status"

    def test_organization_enum_members(self):
        """Verify all organization strategies exist."""
        members = list(TaskOrganization)
        assert len(members) == 4


class TestProjectTask:
    """Test ProjectTask data class with source info."""

    def test_minimal_task_creation(self):
        """Create task with required fields."""
        task_path = Path("packages/test/tasks.md")
        task = ProjectTask(
            title="Test",
            description="Desc",
            source_file=task_path,
            department="test",
        )
        assert task.title == "Test"
        assert task.source_file == task_path
        assert task.department == "test"

    def test_full_task_creation(self):
        """Create task with all fields."""
        task_path = Path("packages/infrastructure/tasks.md")
        task = ProjectTask(
            title="Full Task",
            description="Complete",
            source_file=task_path,
            department="infrastructure",
            role="Solo developer",
            dependencies="Task A",
            effort="M (9-12 hours)",
            quality_required=True,
            milestone="MVP",
            source_context="tasks.md",
        )
        assert task.quality_required is True
        assert task.milestone == "MVP"

    def test_source_context_default(self):
        """Source context defaults to filename."""
        task_path = Path("packages/test/tasks.md")
        task = ProjectTask(
            title="T", description="D", source_file=task_path, department="test"
        )
        assert task.source_context == "tasks.md"


class TestTaskWalkerInit:
    """Test TaskWalker initialization."""

    def test_valid_initialization(self):
        """Initialize walker with valid root path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            walker = TaskWalker(str(tmppath))
            assert walker.root_path == tmppath
            assert walker.tasks == []

    def test_default_organization(self):
        """Default organization strategy is BY_ROLE."""
        with tempfile.TemporaryDirectory() as tmpdir:
            walker = TaskWalker(str(tmpdir))
            assert walker.organization == TaskOrganization.BY_ROLE

    def test_custom_organization(self):
        """Set custom organization strategy."""
        with tempfile.TemporaryDirectory() as tmpdir:
            walker = TaskWalker(
                str(tmpdir), organization=TaskOrganization.BY_DEPARTMENT
            )
            assert walker.organization == TaskOrganization.BY_DEPARTMENT

    def test_root_not_found(self):
        """Raise FileNotFoundError for missing root."""
        with pytest.raises(FileNotFoundError):
            TaskWalker("nonexistent/path")

    def test_root_not_directory(self):
        """Raise NotADirectoryError if root is a file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            test_file = tmppath / "test.txt"
            test_file.write_text("test")

            with pytest.raises(NotADirectoryError):
                TaskWalker(str(test_file))

    def test_walker_repr(self):
        """String representation includes root and organization."""
        with tempfile.TemporaryDirectory() as tmpdir:
            walker = TaskWalker(str(tmpdir))
            repr_str = repr(walker)
            assert "TaskWalker" in repr_str
            assert "tasks=0" in repr_str


class TestTaskWalkerDiscovery:
    """Test recursive task file discovery."""

    def test_find_single_task_file(self):
        """Find single tasks.md in root."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            task_file = tmppath / "tasks.md"
            task_file.write_text("# Tasks\n")

            walker = TaskWalker(str(tmppath))
            files = walker._find_task_files()
            assert len(files) == 1
            assert files[0].name == "tasks.md"

    def test_find_nested_task_files(self):
        """Find tasks.md in nested directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            (tmppath / "zone-a").mkdir()
            (tmppath / "zone-b").mkdir()

            (tmppath / "tasks.md").write_text("# Root tasks\n")
            (tmppath / "zone-a" / "tasks.md").write_text("# Zone A tasks\n")
            (tmppath / "zone-b" / "tasks.md").write_text("# Zone B tasks\n")

            walker = TaskWalker(str(tmppath))
            files = walker._find_task_files()
            assert len(files) == 3

    def test_no_task_files(self):
        """Handle directory with no tasks.md files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            (tmppath / "some-file.txt").write_text("content")

            walker = TaskWalker(str(tmppath))
            files = walker._find_task_files()
            assert len(files) == 0

    def test_extract_department_from_path(self):
        """Extract department name from file path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            file_path = tmppath / "infrastructure" / "data-sources" / "tasks.md"

            walker = TaskWalker(str(tmppath))
            dept = walker._extract_department(file_path)
            assert dept == "infrastructure"

    def test_extract_department_root_level(self):
        """Root level tasks.md has 'global' department."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            file_path = tmppath / "tasks.md"

            walker = TaskWalker(str(tmppath))
            dept = walker._extract_department(file_path)
            assert dept == "global"


class TestTaskWalkerParsing:
    """Test multi-file task parsing."""

    def test_parse_single_file(self):
        """Parse tasks from single file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            task_file = tmppath / "tasks.md"
            task_file.write_text("""# Tasks
- **Task:** Task One
  - **Description:** First task
  - **Assigned role:** Developer
""")

            walker = TaskWalker(str(tmppath))
            walker.walk()
            assert len(walker.tasks) == 1
            assert walker.tasks[0].title == "Task One"

    def test_parse_multiple_files(self):
        """Parse tasks from multiple files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            (tmppath / "zone-a").mkdir()
            (tmppath / "zone-b").mkdir()

            root_task = tmppath / "tasks.md"
            root_task.write_text("""# Global
- **Task:** Global Task
  - **Description:** Root level
""")

            zone_a_task = tmppath / "zone-a" / "tasks.md"
            zone_a_task.write_text("""# Zone A
- **Task:** Zone A Task
  - **Description:** In zone A
""")

            zone_b_task = tmppath / "zone-b" / "tasks.md"
            zone_b_task.write_text("""# Zone B
- **Task:** Zone B Task
  - **Description:** In zone B
""")

            walker = TaskWalker(str(tmppath))
            walker.walk()
            assert len(walker.tasks) == 3

    def test_department_assignment_during_parse(self):
        """Tasks assigned correct department during parsing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            (tmppath / "infrastructure").mkdir()

            task_file = tmppath / "infrastructure" / "tasks.md"
            task_file.write_text("""# Tasks
- **Task:** Infra Task
  - **Description:** Infrastructure work
""")

            walker = TaskWalker(str(tmppath))
            walker.walk()
            assert walker.tasks[0].department == "infrastructure"

    def test_quality_mandate_detection_across_files(self):
        """Detect quality mandate in all parsed tasks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            task_file = tmppath / "tasks.md"
            task_file.write_text("""# Tasks
- **Task:** Quality Task
  - **Description:** [Quality Mandate Required] Must comply
""")

            walker = TaskWalker(str(tmppath))
            walker.walk()
            assert walker.tasks[0].quality_required is True


class TestTaskWalkerGrouping:
    """Test task grouping strategies."""

    def test_group_by_role(self):
        """Group tasks by assigned role."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            task_file = tmppath / "tasks.md"
            task_file.write_text("""# Tasks
- **Task:** Solo Task
  - **Description:** Solo work
  - **Assigned role:** Solo developer

- **Task:** Agent Task
  - **Description:** Agent work
  - **Assigned role:** Solo+Agent
""")

            walker = TaskWalker(
                str(tmppath), organization=TaskOrganization.BY_ROLE
            )
            walker.walk()
            grouped = walker._group_tasks()

            assert "Solo developer" in grouped
            assert "Solo+Agent" in grouped
            assert len(grouped["Solo developer"]) == 1

    def test_group_by_department(self):
        """Group tasks by department."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            (tmppath / "infrastructure").mkdir()
            (tmppath / "visual-design").mkdir()

            infra_task = tmppath / "infrastructure" / "tasks.md"
            infra_task.write_text("""# Tasks
- **Task:** Infra Task
  - **Description:** Infrastructure
""")

            visual_task = tmppath / "visual-design" / "tasks.md"
            visual_task.write_text("""# Tasks
- **Task:** Visual Task
  - **Description:** Visual work
""")

            walker = TaskWalker(
                str(tmppath), organization=TaskOrganization.BY_DEPARTMENT
            )
            walker.walk()
            grouped = walker._group_tasks()

            assert "infrastructure" in grouped
            assert "visual-design" in grouped

    def test_group_by_milestone(self):
        """Group tasks by milestone."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            task_file = tmppath / "tasks.md"
            task_file.write_text("""# Tasks
- **Task:** MVP Task
  - **Description:** MVP work
  - **Milestone:** MVP

- **Task:** Polish Task
  - **Description:** Polish work
  - **Milestone:** Polish
""")

            walker = TaskWalker(
                str(tmppath), organization=TaskOrganization.BY_MILESTONE
            )
            walker.walk()
            grouped = walker._group_tasks()

            assert "MVP" in grouped
            assert "Polish" in grouped

    def test_unassigned_tasks_handled(self):
        """Handle tasks without role/department/milestone."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            task_file = tmppath / "tasks.md"
            task_file.write_text("""# Tasks
- **Task:** No Role Task
  - **Description:** Task without role
""")

            walker = TaskWalker(
                str(tmppath), organization=TaskOrganization.BY_ROLE
            )
            walker.walk()
            grouped = walker._group_tasks()

            assert "Unassigned" in grouped


class TestTaskWalkerEstimation:
    """Test effort estimation."""

    def test_estimate_total_effort(self):
        """Calculate total project effort."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            task_file = tmppath / "tasks.md"
            task_file.write_text("""# Tasks
- **Task:** Small Task
  - **Description:** Small work
  - **Estimated effort:** S (6-10 hours)

- **Task:** Large Task
  - **Description:** Large work
  - **Estimated effort:** L (16-26 hours)
""")

            walker = TaskWalker(str(tmppath))
            walker.walk()
            estimate = walker._estimate_total_effort()

            assert "22" in estimate  # 6+16 min, 10+26 max
            assert "-" in estimate


class TestTaskWalkerRendering:
    """Test Rich rendering output."""

    def test_render_with_tasks(self):
        """Render discovered tasks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            task_file = tmppath / "tasks.md"
            task_file.write_text("""# Tasks
- **Task:** Test Task
  - **Description:** Test
""")

            walker = TaskWalker(str(tmppath))
            walker.walk()

            with mock.patch.object(walker.console, "print"):
                walker.render()  # Should not raise

    def test_render_without_walk(self):
        """Handle render without walk - should warn."""
        with tempfile.TemporaryDirectory() as tmpdir:
            walker = TaskWalker(str(tmpdir))
            # Don't call walk()
            with mock.patch.object(walker.console, "print"):
                walker.render()  # Should handle gracefully

    def test_summary_statistics(self):
        """Generate summary statistics."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            task_file = tmppath / "tasks.md"
            task_file.write_text("""# Tasks
- **Task:** Quality Task
  - **Description:** [Quality Mandate Required] Test
  - **Milestone:** MVP
""")

            walker = TaskWalker(str(tmppath))
            walker.walk()

            with mock.patch.object(walker.console, "print"):
                walker.summary()  # Should not raise


class TestMainFunction:
    """Test CLI entry point."""

    def test_main_success(self):
        """Main function succeeds with valid project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            task_file = tmppath / "tasks.md"
            task_file.write_text("# Tasks\n- **Task:** Test\n  - **Description:** Test\n")

            with mock.patch("utils.task_walk.TaskWalker") as mock_walker_class:
                mock_instance = mock.Mock()
                mock_walker_class.return_value = mock_instance
                result = main()
                assert result == 0
                mock_instance.walk.assert_called_once()

    def test_main_root_not_found(self):
        """Main returns 1 on FileNotFoundError."""
        with mock.patch("utils.task_walk.TaskWalker") as mock_walker_class:
            mock_walker_class.side_effect = FileNotFoundError("Not found")
            result = main()
            assert result == 1

    def test_main_not_directory(self):
        """Main returns 1 on NotADirectoryError."""
        with mock.patch("utils.task_walk.TaskWalker") as mock_walker_class:
            mock_walker_class.side_effect = NotADirectoryError("Not dir")
            result = main()
            assert result == 1

    def test_main_unexpected_error(self):
        """Main returns 1 on unexpected error."""
        with mock.patch("utils.task_walk.TaskWalker") as mock_walker_class:
            mock_walker_class.side_effect = RuntimeError("Unexpected")
            result = main()
            assert result == 1


class TestInitialization:
    """Test module imports and dependencies."""

    def test_imports_available(self):
        """Verify all required imports load."""
        from utils import task_walk

        assert hasattr(task_walk, "TaskOrganization")
        assert hasattr(task_walk, "ProjectTask")
        assert hasattr(task_walk, "TaskWalker")
        assert hasattr(task_walk, "main")

    def test_rich_library_available(self):
        """Verify Rich library is installed."""
        import rich

        assert hasattr(rich, "console")

    def test_classes_instantiable(self):
        """Verify key classes can be instantiated."""
        assert TaskOrganization.BY_ROLE is not None

        task_path = Path("packages/test/tasks.md")
        task = ProjectTask(
            title="Test", description="Test", source_file=task_path, department="test"
        )
        assert task is not None

    def test_enum_values_accessible(self):
        """Verify all enum values accessible."""
        assert TaskOrganization.BY_ROLE
        assert TaskOrganization.BY_DEPARTMENT
        assert TaskOrganization.BY_MILESTONE
        assert TaskOrganization.BY_STATUS
