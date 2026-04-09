"""Task walk utility for verbose project-wide task discovery and organization.

Recursively searches project for all tasks.md files, parses tasks, and displays
them organized by role/department with detailed information using Rich formatting.

Module Structure:
- TaskOrganization: Enum for grouping strategy
- ProjectTask: Enhanced task with file source information
- TaskWalker: Recursive project scanner and organizer
- main(): CLI entry point
"""

import re
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


class TaskOrganization(Enum):
    """Task organization strategy."""

    BY_ROLE = "role"
    BY_DEPARTMENT = "department"
    BY_MILESTONE = "milestone"
    BY_STATUS = "status"


@dataclass
class ProjectTask:
    """Task with project location information.

    Extends basic task info with source file and directory context.
    """

    title: str
    description: str
    source_file: Path
    department: str  # Extracted from path (e.g., "infrastructure", "visual-design")
    role: Optional[str] = None
    dependencies: Optional[str] = None
    effort: Optional[str] = None
    quality_required: bool = False
    milestone: Optional[str] = None
    source_context: Optional[str] = None  # "README.md", "tasks.md", etc.

    def __post_init__(self) -> None:
        """Extract source context from file path."""
        if not self.source_context:
            self.source_context = self.source_file.name


class TaskWalker:
    """Recursively discover and organize tasks throughout project.

    Searches for tasks.md files, parses all tasks, and groups by
    role/department with verbose output via Rich formatting.

    Attributes:
        root_path: Project root directory to search from
        console: Rich Console for output
        tasks: Discovered tasks organized by grouping
        organization: Current grouping strategy
    """

    def __init__(
        self,
        root_path: str = "packages",
        organization: TaskOrganization = TaskOrganization.BY_ROLE,
    ):
        """Initialize task walker.

        Args:
            root_path: Root directory to search from
            organization: How to group tasks (by role, department, etc.)

        Raises:
            FileNotFoundError: If root path does not exist
        """
        self.root_path = Path(root_path)
        self.console = Console()
        self.tasks: List[ProjectTask] = []
        self.organization = organization

        self._validate_root()

    def _validate_root(self) -> None:
        """Validate root directory exists.

        Raises:
            FileNotFoundError: If root path does not exist
        """
        if not self.root_path.exists():
            raise FileNotFoundError(f"Root path not found: {self.root_path}")
        if not self.root_path.is_dir():
            raise NotADirectoryError(f"Root path is not a directory: {self.root_path}")

    def _find_task_files(self) -> List[Path]:
        """Recursively find all tasks.md files in project.

        Returns:
            List of Path objects pointing to tasks.md files
        """
        task_files = []
        for path in self.root_path.rglob("tasks.md"):
            task_files.append(path)
        return sorted(task_files)

    def _extract_department(self, file_path: Path) -> str:
        """Extract department/zone from file path.

        Extracts the directory name immediately under packages/:
        packages/infrastructure/data-sources/tasks.md -> "infrastructure"
        packages/visual-design/zones/zone-a/tasks.md -> "visual-design"

        Args:
            file_path: Path to tasks.md file

        Returns:
            Department name or "global" if at packages root
        """
        try:
            relative = file_path.relative_to(self.root_path)
            parts = relative.parts
            if len(parts) > 1:
                return parts[0]
            return "global"
        except ValueError:
            return "unknown"

    def _parse_task_from_file(self, file_path: Path) -> List[ProjectTask]:
        """Parse all tasks from a single tasks.md file.

        Args:
            file_path: Path to tasks.md file

        Returns:
            List of ProjectTask objects

        Raises:
            IOError: If file cannot be read
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except IOError as e:
            raise IOError(f"Cannot read {file_path}: {e}")

        tasks = []
        department = self._extract_department(file_path)

        # Split by task marker (main bullet point)
        task_blocks = re.split(r"\n- \*\*Task:\*\*", content)

        for block in task_blocks[1:]:  # Skip header
            lines = block.split("\n")
            task = ProjectTask(
                title="",
                description="",
                source_file=file_path,
                department=department,
            )

            # Extract task title (first line)
            if lines:
                task.title = lines[0].strip()

            # Extract fields from indented lines
            for line in lines[1:]:
                if not line.strip():
                    continue

                if "**Description:**" in line:
                    task.description = re.sub(
                        r".*\*\*Description:\*\*\s*", "", line
                    ).strip()
                elif "**Source:**" in line:
                    task.source_context = re.sub(
                        r".*\*\*Source:\*\*\s*", "", line
                    ).strip()
                elif "**Dependencies:**" in line:
                    task.dependencies = re.sub(
                        r".*\*\*Dependencies:\*\*\s*", "", line
                    ).strip()
                elif "**Estimated effort:**" in line:
                    effort_match = re.search(r"([A-Z]+\s*\([^)]+\))", line)
                    if effort_match:
                        task.effort = effort_match.group(1).strip()
                elif "**Assigned role:**" in line:
                    task.role = re.sub(r".*\*\*Assigned role:\*\*\s*", "", line).strip()
                elif "**Milestone:**" in line:
                    task.milestone = re.sub(
                        r".*\*\*Milestone:\*\*\s*", "", line
                    ).strip()

                # Quality mandate check
                if "[Quality Mandate Required]" in task.description:
                    task.quality_required = True

            if task.title:
                tasks.append(task)

        return tasks

    def walk(self) -> None:
        """Recursively discover and parse all tasks in project."""
        task_files = self._find_task_files()

        for file_path in task_files:
            try:
                file_tasks = self._parse_task_from_file(file_path)
                self.tasks.extend(file_tasks)
            except IOError as e:
                self.console.print(
                    Panel(f"[yellow]Warning:[/yellow] {e}", style="dim yellow")
                )

    def _group_tasks(self) -> Dict[str, List[ProjectTask]]:
        """Group tasks by current organization strategy.

        Returns:
            Dictionary with grouping key as key and list of tasks as value
        """
        grouped: Dict[str, List[ProjectTask]] = {}

        for task in self.tasks:
            if self.organization == TaskOrganization.BY_ROLE:
                key = task.role or "Unassigned"
            elif self.organization == TaskOrganization.BY_DEPARTMENT:
                key = task.department or "Unknown"
            elif self.organization == TaskOrganization.BY_MILESTONE:
                key = task.milestone or "Unplanned"
            elif self.organization == TaskOrganization.BY_STATUS:
                key = "Pending"  # Default status
            else:
                key = "Other"

            if key not in grouped:
                grouped[key] = []
            grouped[key].append(task)

        return grouped

    def render(self) -> None:
        """Render all discovered tasks organized by grouping strategy."""
        if not self.tasks:
            self.console.print(
                Panel(
                    "No tasks found. Run walk() first.",
                    style="red",
                    title="[!] Error",
                )
            )
            return

        grouped = self._group_tasks()

        # Header
        org_label = self.organization.value.replace("_", " ").title()
        self.console.print(
            Panel(
                f"[bold cyan]The Summoner's Chronicle[/bold cyan]\n[dim]{len(self.tasks)} Total Tasks[/dim] "
                f"| [yellow]Organized by {org_label}[/yellow]",
                style="blue",
                title="[*] Project Task Walk",
            )
        )

        # Render each group
        for group_name in sorted(grouped.keys()):
            group_tasks = grouped[group_name]
            self._render_group(group_name, group_tasks)

    def _render_group(self, group_name: str, group_tasks: List[ProjectTask]) -> None:
        """Render tasks for a single group.

        Args:
            group_name: Name of the group (role, department, etc.)
            group_tasks: List of tasks in the group
        """
        # Group header
        quality_count = sum(1 for t in group_tasks if t.quality_required)
        header = f"{group_name.upper()} [{len(group_tasks)} tasks"
        if quality_count > 0:
            header += f", {quality_count} require quality mandate"
        header += "]"

        self.console.print(Panel(header, style="bold cyan", expand=False))

        # Task details table
        table = Table(
            show_header=True, header_style="bold white", show_lines=False, width=120
        )
        table.add_column("Task", style="cyan", width=40)
        table.add_column("Effort", style="yellow", width=12)
        table.add_column("Milestone", style="green", width=10)
        table.add_column("Dependencies", style="dim", width=35)

        for task in group_tasks:
            # Task with quality badge
            quality_badge = "[Quality]" if task.quality_required else ""
            task_display = Text(task.title + (" " + quality_badge if quality_badge else ""))
            if task.quality_required:
                task_display.stylize(
                    "bold magenta",
                    len(task.title),
                    len(task.title) + len(quality_badge) + 1,
                )

            effort = task.effort or "--"
            milestone = task.milestone or "--"
            deps = (task.dependencies or "None")[:35]

            table.add_row(task_display, effort, milestone, deps)

        self.console.print(table)

        # Verbose details for each task
        for task in group_tasks:
            self._render_task_details(task)

        self.console.print()  # Spacing between groups

    def _render_task_details(self, task: ProjectTask) -> None:
        """Render verbose details for a single task.

        Args:
            task: ProjectTask to render
        """
        # Panel with task title
        title_text = f"[cyan]{task.title}[/cyan]"
        if task.quality_required:
            title_text += " [magenta][Quality Mandate Required][/magenta]"

        details = f"""[yellow]Description:[/yellow]
{task.description}

[yellow]Source:[/yellow] {task.source_context} [{task.source_file.relative_to(self.root_path.parent) if self.root_path.parent in task.source_file.parents else task.source_file}]
[yellow]Department:[/yellow] {task.department}
[yellow]Effort:[/yellow] {task.effort or "Unestimated"}
[yellow]Milestone:[/yellow] {task.milestone or "Unplanned"}"""

        if task.dependencies and task.dependencies.lower() != "none":
            details += f"\n[yellow]Dependencies:[/yellow] {task.dependencies}"

        self.console.print(Panel(details, title=title_text, style="dim", expand=False))

    def summary(self) -> None:
        """Print summary statistics of discovered tasks."""
        if not self.tasks:
            return

        grouped = self._group_tasks()
        total_effort = self._estimate_total_effort()
        quality_count = sum(1 for t in self.tasks if t.quality_required)
        milestone_counts = {}
        for task in self.tasks:
            milestone = task.milestone or "Unplanned"
            milestone_counts[milestone] = milestone_counts.get(milestone, 0) + 1

        summary_text = f"""[green]Total Tasks:[/green] {len(self.tasks)}
[green]Groups:[/green] {len(grouped)}
[magenta]Quality Mandate Required:[/magenta] {quality_count}/{len(self.tasks)}
[yellow]Estimated Total Effort:[/yellow] {total_effort} hours"""

        for milestone in sorted(milestone_counts.keys()):
            count = milestone_counts[milestone]
            summary_text += f"\n[cyan]{milestone}:[/cyan] {count} tasks"

        self.console.print(Panel(summary_text, title="[#] Summary", style="dim"))

    def _estimate_total_effort(self) -> str:
        """Estimate total project effort from all tasks.

        Returns:
            Human-readable effort estimate (e.g., "145-220 hours")
        """
        effort_map = {
            "s": (6, 10),
            "m": (9, 22),
            "l": (16, 26),
            "xl": (26, 40),
        }

        total_min = 0
        total_max = 0

        for task in self.tasks:
            if task.effort:
                effort_level = task.effort.lower()[0:2].strip()
                if effort_level.startswith("x"):
                    effort_level = "xl"
                if effort_level in effort_map:
                    min_h, max_h = effort_map[effort_level]
                    total_min += min_h
                    total_max += max_h

        if total_min == 0 and total_max == 0:
            return "Unable to estimate"

        return f"{total_min}-{total_max}"

    def __repr__(self) -> str:
        """String representation of walker state."""
        return f"TaskWalker(root='{self.root_path}', org='{self.organization.value}', tasks={len(self.tasks)})"


def main(argv: Optional[List[str]] = None) -> int:
    """CLI entry point for task walk utility.

    Args:
        argv: Command line arguments (optional)

    Returns:
        Exit code: 0 on success, 1 on error
    """
    try:
        walker = TaskWalker(
            root_path="packages", organization=TaskOrganization.BY_ROLE
        )
        walker.walk()
        walker.render()
        walker.summary()
        return 0

    except FileNotFoundError as e:
        console = Console()
        console.print(
            Panel(f"[red]Path not found:[/red] {e}", style="red", title="[X] Error")
        )
        return 1

    except NotADirectoryError as e:
        console = Console()
        console.print(
            Panel(
                f"[red]Invalid directory:[/red] {e}", style="red", title="[X] Error"
            )
        )
        return 1

    except Exception as e:
        console = Console()
        console.print(
            Panel(
                f"[red]Unexpected error:[/red] {type(e).__name__}: {e}",
                style="red",
                title="[X] Error",
            )
        )
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
