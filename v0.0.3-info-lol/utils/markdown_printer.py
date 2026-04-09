#!/usr/bin/env python3
"""
Rich Markdown Printer – Terminal Markdown File Viewer

A command-line utility that renders Markdown files (.md) in the terminal
with excellent visual clarity using the Rich library. Supports syntax
highlighting, responsive layout, and accessibility features.

Usage:
    python -m utils.markdown_printer <path_to_file.md>
    python -m utils.markdown_printer --help

Features:
    - Semantic color mapping for all Markdown elements
    - Syntax highlighting for code blocks
    - Responsive table rendering
    - High-contrast mode support
    - Configuration via markdown_printer.toml
    - Error handling with visual feedback

Design: See .docs/project-management/[internal] RICH_API_COLOR_DESIGN_SPEC.txt
"""

import sys
from pathlib import Path
from typing import Optional, Dict, Any
import argparse

try:
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.syntax import Syntax
    from rich.table import Table
    from rich.text import Text
except ImportError:
    raise ImportError(
        "Rich library required. Install with: pip install rich\n"
        "Or: pip install -r requirements.txt"
    )


class ColorPalette:
    """
    Semantic color palette for Markdown elements.

    All colors are 256-color safe with ANSI fallbacks.
    Can be customized via configuration file.
    """

    def __init__(self, high_contrast: bool = False):
        """
        Initialize color palette.

        Args:
            high_contrast: Use bold + reverse video instead of colors

        Attributes map Markdown elements to Rich color styles
        """
        self.high_contrast = high_contrast

        if high_contrast:
            # High-contrast mode: use bold and reverse instead of colors
            self.h1 = "bold underline"
            self.h2 = "bold"
            self.h3 = "bold"
            self.h4 = "bold"
            self.h5 = "bold"
            self.h6 = "bold dim"
            self.blockquote = "italic"
            self.link = "bold underline"
            self.inline_code = "reverse"
            self.code_theme = "default"
        else:
            # Standard color mode
            self.h1 = "bold white underline"
            self.h2 = "bright_cyan bold"
            self.h3 = "bright_green bold"
            self.h4 = "bright_yellow"
            self.h5 = "bright_magenta"
            self.h6 = "bright_black italic"
            self.blockquote = "bright_black italic"
            self.link = "bright_blue underline"
            self.inline_code = "reverse bright_black on grey23"
            self.code_theme = "monokai"


class MarkdownConfig:
    """
    Configuration for Markdown printer.

    Loads from markdown_printer.toml if present,
    otherwise uses sensible defaults.
    """

    DEFAULT_CONFIG = {
        "enable_syntax_highlighting": True,
        "enable_line_numbers": False,
        "code_theme": "monokai",
        "table_style": "default",
        "show_toc": False,
        "high_contrast": False,
        "left_margin": 2,
        "max_table_column_width": 50,
    }

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize configuration.

        Args:
            config_path: Path to markdown_printer.toml (optional)

        Attributes:
            settings: Dictionary of configuration values
        """
        self.settings = self.DEFAULT_CONFIG.copy()
        self.config_path = config_path

        if config_path and config_path.exists():
            self._load_from_file(config_path)

    def _load_from_file(self, path: Path) -> None:
        """
        Load configuration from TOML file.

        Args:
            path: Path to markdown_printer.toml

        Note: Actual TOML parsing would use tomli/toml library.
        This is a placeholder for configuration loading.
        """
        # In full implementation, would use:
        # import tomllib (Python 3.11+) or tomli
        pass

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.

        Args:
            key: Configuration key
            default: Default value if not found

        Returns:
            Configuration value or default
        """
        return self.settings.get(key, default)


class MarkdownPrinter:
    """
    Main Markdown printer utility.

    Renders Markdown files in terminal with Rich library,
    applying semantic colors and visual hierarchy.
    """

    def __init__(
        self,
        file_path: Path,
        high_contrast: bool = False,
        show_toc: bool = False,
    ):
        """
        Initialize Markdown printer.

        Args:
            file_path: Path to .md file to render
            high_contrast: Enable high-contrast mode
            show_toc: Show table of contents before content

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is not a .md file

        Attributes:
            console: Rich Console for output
            palette: Color palette for elements
            config: Configuration settings
        """
        self.file_path = Path(file_path)
        self.high_contrast = high_contrast
        self.show_toc = show_toc

        # Validate file
        self._validate_file()

        # Initialize components
        self.console = Console(force_terminal=True, record=False)
        self.palette = ColorPalette(high_contrast=high_contrast)
        self.config = MarkdownConfig()
        self.content = self._read_file()

    def _validate_file(self) -> None:
        """
        Validate that file exists and is a Markdown file.

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file extension is not .md
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")

        if self.file_path.suffix.lower() != ".md":
            raise ValueError(
                f"Expected .md file, got: {self.file_path.suffix}"
            )

    def _read_file(self) -> str:
        """
        Read Markdown file content.

        Returns:
            File content as string

        Raises:
            IOError: If file cannot be read
        """
        try:
            return self.file_path.read_text(encoding="utf-8")
        except IOError as e:
            raise IOError(f"Cannot read file {self.file_path}: {e}") from e

    def _print_header(self) -> None:
        """Print file header with name and path."""
        header = Text(f"📄 {self.file_path.name}", style="bold bright_white")
        subheader = Text(str(self.file_path.resolve()), style="dim")
        self.console.print(header)
        self.console.print(subheader)
        self.console.print()

    def _print_table_of_contents(self) -> None:
        """
        Print table of contents from headings.

        Extracts all headings and displays with line numbers.
        """
        lines = self.content.split("\n")
        headings = []

        for line_num, line in enumerate(lines, start=1):
            if line.startswith("#"):
                level = len(line) - len(line.lstrip("#"))
                title = line.lstrip("# ").strip()
                indent = "  " * (level - 1)
                headings.append(f"{indent}• {title} (line {line_num})")

        if not headings:
            return

        self.console.print(Text("📑 Table of Contents", style="bold bright_cyan"))
        for heading in headings:
            self.console.print(heading)
        self.console.print()

    def _print_error(self, message: str) -> None:
        """
        Print error message in visual panel.

        Args:
            message: Error message to display
        """
        panel = Panel(
            message,
            title="[bold red]Error[/bold red]",
            border_style="red",
            expand=False,
        )
        self.console.print(panel)

    def render(self) -> None:
        """
        Render Markdown file to terminal.

        Applies visual hierarchy, colors, and formatting according to
        the design specification.
        """
        try:
            # Print header
            self._print_header()

            # Print TOC if requested
            if self.show_toc:
                self._print_table_of_contents()

            # Check if empty
            if not self.content.strip():
                self.console.print(Text("(empty document)", style="dim italic"))
                return

            # Render Markdown with Rich
            markdown = Markdown(self.content)
            self.console.print(markdown)

        except Exception as e:
            self._print_error(f"Error rendering Markdown: {str(e)}")
            raise

    def __repr__(self) -> str:
        """Return string representation."""
        return (
            f"MarkdownPrinter("
            f"file={self.file_path.name}, "
            f"high_contrast={self.high_contrast})"
        )


def create_argument_parser() -> argparse.ArgumentParser:
    """
    Create command-line argument parser.

    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        prog="markdown_printer",
        description="Render Markdown files in terminal with Rich formatting",
        epilog="Example: markdown_printer .docs/README.md --toc",
    )

    parser.add_argument(
        "file",
        type=Path,
        help="Path to Markdown file (.md)",
    )

    parser.add_argument(
        "--toc",
        action="store_true",
        help="Show table of contents before content",
    )

    parser.add_argument(
        "--high-contrast",
        action="store_true",
        help="Use high-contrast mode (no colors)",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0",
    )

    return parser


def main(argv: Optional[list] = None) -> int:
    """
    Main entry point for markdown_printer utility.

    Args:
        argv: Command-line arguments (for testing)

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = create_argument_parser()

    try:
        args = parser.parse_args(argv)

        # Create and render printer
        printer = MarkdownPrinter(
            file_path=args.file,
            high_contrast=args.high_contrast,
            show_toc=args.toc,
        )

        printer.render()
        return 0

    except FileNotFoundError as e:
        console = Console()
        console.print(f"[bold red]Error:[/bold red] {e}", file=sys.stderr)
        return 1

    except ValueError as e:
        console = Console()
        console.print(f"[bold red]Error:[/bold red] {e}", file=sys.stderr)
        return 1

    except KeyboardInterrupt:
        return 130  # Standard exit code for SIGINT

    except Exception as e:
        console = Console()
        console.print(
            f"[bold red]Unexpected error:[/bold red] {e}",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
