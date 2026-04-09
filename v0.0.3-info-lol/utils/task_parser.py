"""Task parser utility for displaying project tasks with Rich formatting.

Reads tasks.md files and renders a visually clear list of tasks with status,
effort estimates, milestones, and dependencies using the Rich library.

Module Structure:
- TaskStatus: Enum for task completion states
- TaskMetadata: Data class for parsed task information
- TaskColor: Color palette for semantic task rendering
- TaskParser: Main parser and renderer
- main(): CLI entry point
"""

import re
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Optional

from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich.style import Style


class TaskStatus(Enum):
    """Task completion status enumeration."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"


@dataclass
class TaskMetadata:
    """Parsed task metadata from tasks.md."""

    title: str
    description: str
    source: Optional[str] = None
    dependencies: Optional[str] = None
    effort: Optional[str] = None
    quality_required: bool = False
    role: Optional[str] = None
    milestone: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING


class TaskColor:
    """Semantic color palette for tasks."""

    # Effort levels: size/duration
    EFFORT_SMALL = "cyan"  # S: 6-10 hours
    EFFORT_MEDIUM = "yellow"  # M: 9-22 hours
    EFFORT_LARGE = "magenta"  # L: 16-26 hours
    EFFORT_XLARGE = "red"  # XL: 26-40 hours

    # Task status indicators
    STATUS_PENDING = "dim white"
    STATUS_IN_PROGRESS = "yellow"
    STATUS_COMPLETED = "green"
    STATUS_BLOCKED = "red"

    # Milestone badges
    MILESTONE_MVP = "bold green"
    MILESTONE_POLISH = "bold yellow"
    MILESTONE_FUTURE = "bold cyan"

    # Quality mandate
    QUALITY_REQUIRED = "bold magenta"

    @staticmethod
    def effort_color(effort: Optional[str]) -> str:
        """Get color for effort level."""
        if not effort:
            return "white"
        effort = effort.upper().strip()
        if effort.startswith("S"):
            return TaskColor.EFFORT_SMALL
        elif effort.startswith("M"):
            return TaskColor.EFFORT_MEDIUM
        elif effort.startswith("L") and not effort.startswith("XL"):
            return TaskColor.EFFORT_LARGE
        elif effort.startswith("XL"):
            return TaskColor.EFFORT_XLARGE
        return "white"

    @staticmethod
    def milestone_color(milestone: Optional[str]) -> str:
        """Get color for milestone badge."""
        if not milestone:
            return "white"
        milestone = milestone.strip().lower()
        if milestone == "mvp":
            return TaskColor.MILESTONE_MVP
        elif milestone == "polish":
            return TaskColor.MILESTONE_POLISH
        elif milestone == "future":
            return TaskColor.MILESTONE_FUTURE
        return "white"


class TaskParser:
    """Parse and render tasks.md file with Rich formatting.

    Attributes:
        file_path: Path to tasks.md file
        console: Rich Console for rendering
        tasks: Parsed list of TaskMetadata objects
    """

    def __init__(self, file_path: str = "packages/tasks.md"):
        """Initialize parser with path to tasks.md.

        Args:
            file_path: Path to tasks.md (relative to project root)

        Raises:
            FileNotFoundError: If tasks.md does not exist
            ValueError: If file does not have .md extension
        """
        self.file_path = Path(file_path)
        self.console = Console()
        self.tasks: List[TaskMetadata] = []

        self._validate_file()

    def _validate_file(self) -> None:
        """Validate file exists and has correct extension.

        Raises:
            FileNotFoundError: If file does not exist
            ValueError: If file is not .md extension
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"Tasks file not found: {self.file_path}")
        if self.file_path.suffix != ".md":
            raise ValueError(
                f"Invalid file type: {self.file_path.suffix}. Expected .md"
            )

    def _read_file(self) -> str:
        """Read tasks.md file with UTF-8 encoding.

        Returns:
            File contents as string

        Raises:
            IOError: If file cannot be read
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return f.read()
        except IOError as e:
            raise IOError(f"Cannot read {self.file_path}: {e}")

    def _parse_tasks(self, content: str) -> List[TaskMetadata]:
        """Parse task entries from markdown content.

        Extracts task blocks (bullet points) and extracts structured metadata.
        Each task starts with "- **Task:**" and contains field lines like
        "  - **Field:** value".

        Args:
            content: Full markdown file contents

        Returns:
            List of parsed TaskMetadata objects
        """
        tasks = []

        # Split by task marker (main bullet point)
        task_blocks = re.split(r"\n- \*\*Task:\*\*", content)

        for block in task_blocks[1:]:  # Skip header
            lines = block.split("\n")
            task = TaskMetadata(title="", description="")

            # Extract task title (first line)
            if lines:
                task.title = lines[0].strip()

            # Extract fields from indented lines
            for line in lines[1:]:
                if not line.strip():
                    continue

                # Parse "  - **Field:** value" format
                if "**Description:**" in line:
                    task.description = re.sub(
                        r".*\*\*Description:\*\*\s*", "", line
                    ).strip()
                elif "**Source:**" in line:
                    task.source = re.sub(r".*\*\*Source:\*\*\s*", "", line).strip()
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

    def parse(self) -> None:
        """Parse tasks.md file and populate task list."""
        content = self._read_file()
        self.tasks = self._parse_tasks(content)

    def render(self) -> None:
        """Render parsed tasks as formatted Rich output."""
        if not self.tasks:
            self.console.print(
                Panel(
                    "No tasks found. Parse file first with .parse()",
                    style="red",
                    title="[!] Error",
                )
            )
            return

        # Title
        self.console.print(
            Panel(
                f"[bold cyan]The Summoner's Chronicle[/bold cyan]\n[dim]{len(self.tasks)} Global Tasks[/dim]",
                style="blue",
                title="[*] Project Tasks",
            )
        )

        # Create task table
        table = Table(show_header=True, header_style="bold white", show_lines=False)
        table.add_column("Task", style="cyan", width=35)
        table.add_column("Effort", style="yellow", width=15)
        table.add_column("Milestone", style="green", width=12)
        table.add_column("Status", style="white", width=12)

        # Add task rows
        for task in self.tasks:
            effort_text = Text(task.effort or "--", style=TaskColor.effort_color(task.effort))
            milestone_text = Text(
                task.milestone or "--", style=TaskColor.milestone_color(task.milestone)
            )

            # Quality badge
            quality_badge = (
                " [Quality]" if task.quality_required else ""
            )

            task_display = Text(task.title + quality_badge)
            if task.quality_required:
                task_display.stylize(TaskColor.QUALITY_REQUIRED, len(task.title), len(task.title) + len(quality_badge))

            table.add_row(task_display, effort_text, milestone_text, "[.] Pending")

        self.console.print(table)

        # Summary panel
        mvp_count = sum(1 for t in self.tasks if t.milestone == "MVP")
        quality_count = sum(1 for t in self.tasks if t.quality_required)

        summary = f"[green]MVP Tasks:[/green] {mvp_count} | [magenta]Quality Mandate:[/magenta] {quality_count}/{len(self.tasks)}"
        self.console.print(Panel(summary, style="dim", title="[#] Summary"))

    def __repr__(self) -> str:
        """String representation of parser state."""
        return f"TaskParser(file='{self.file_path}', tasks={len(self.tasks)})"


def main(argv: Optional[List[str]] = None) -> int:
    """CLI entry point for task parser.

    Args:
        argv: Command line arguments (unused, reserved for future flags)

    Returns:
        Exit code: 0 on success, 1 on error
    """
    try:
        parser = TaskParser("packages/tasks.md")
        parser.parse()
        parser.render()
        return 0

    except FileNotFoundError as e:
        console = Console()
        console.print(
            Panel(f"[red]File not found:[/red] {e}", style="red", title="[X] Error")
        )
        return 1

    except ValueError as e:
        console = Console()
        console.print(
            Panel(f"[red]Invalid file:[/red] {e}", style="red", title="[X] Error")
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
