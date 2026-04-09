#!/usr/bin/env python3
"""
Configuration Loader for The Summoner's Chronicle Development Pipeline

This module loads and manages environment variables from development.cfg and
development.cfg.local files. It provides type-safe access to configuration
values with validation and fallback defaults.

Usage:
    from utils.config_loader import Config
    config = Config()

    # Access configuration values
    api_key = config.get('api_integration', 'RIOT_API_KEY')
    frontend_port = config.get_int('frontend', 'FRONTEND_PORT')
    debug_mode = config.get_bool('project', 'DEBUG_MODE')

    # List all config sections
    sections = config.sections()

    # Validate configuration
    config.validate()

Configuration Priority (highest to lowest):
    1. Environment variables (e.g., RIOT_API_KEY)
    2. development.cfg.local (local overrides, gitignored)
    3. development.cfg (default values)
    4. Built-in defaults

Type Conversion:
    - get_bool() converts strings like "true", "yes", "1" to boolean
    - get_int() converts strings to integers
    - get_float() converts strings to floats
    - get_list() converts comma-separated values to lists
"""

import os
import sys
import configparser
from pathlib import Path
from typing import Optional, List, Dict, Any


class ConfigError(Exception):
    """Raised when configuration is invalid or missing required values."""
    pass


class Config:
    """
    Configuration manager for The Summoner's Chronicle.

    Loads configuration from:
    1. Environment variables (highest priority)
    2. development.cfg.local (local overrides)
    3. development.cfg (defaults)
    4. Built-in defaults
    """

    def __init__(self, config_dir: str = "."):
        """
        Initialize the configuration loader.

        Args:
            config_dir: Directory containing development.cfg (default: current directory)

        Raises:
            ConfigError: If development.cfg is not found
        """
        self.config_dir = Path(config_dir)
        self.config_file = self.config_dir / "development.cfg"
        self.local_config_file = self.config_dir / "development.cfg.local"

        self.parser = configparser.ConfigParser()
        self._load_config()
        self._validate_required_files()

    def _load_config(self) -> None:
        """Load configuration files in priority order."""
        # Load main config file
        if not self.config_file.exists():
            raise ConfigError(
                f"Main configuration file not found: {self.config_file}\n"
                f"Please copy development.cfg.local.example to development.cfg.local "
                f"and update with your actual values."
            )

        self.parser.read(str(self.config_file))

        # Load local overrides if they exist
        if self.local_config_file.exists():
            self.parser.read(str(self.local_config_file))

    def _validate_required_files(self) -> None:
        """Validate that all required directories exist or can be created."""
        required_dirs = [
            self.parser.get('paths', 'DIST_DIR', fallback='./dist'),
            self.parser.get('paths', 'BUILD_DIR', fallback='./build'),
            self.parser.get('paths', 'DOCS_DIR', fallback='./.docs'),
            self.parser.get('storage', 'STORAGE_PATH', fallback='./data/uploads'),
            self.parser.get('storage', 'OUTPUT_DIR', fallback='./data/outputs'),
            self.parser.get('storage', 'TEMP_DIR', fallback='./data/temp'),
            self.parser.get('logging', 'LOG_FILE_PATH', fallback='./logs/development.log').rsplit('/', 1)[0],
        ]

        for dir_path in required_dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)

    def get(self, section: str, key: str, fallback: Optional[str] = None) -> str:
        """
        Get a configuration value as a string.

        Priority:
        1. Environment variable (uppercase section_key)
        2. development.cfg.local value
        3. development.cfg value
        4. fallback value

        Args:
            section: Configuration section name
            key: Configuration key name
            fallback: Default value if not found

        Returns:
            Configuration value as string

        Raises:
            ConfigError: If value not found and no fallback provided
        """
        # Check environment variable first
        env_key = f"{section.upper()}_{key}".upper()
        if env_key in os.environ:
            return os.environ[env_key]

        # Check config file
        try:
            return self.parser.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            if fallback is not None:
                return fallback
            raise ConfigError(
                f"Configuration key not found: [{section}] {key}\n"
                f"Please add it to development.cfg or development.cfg.local"
            )

    def get_bool(self, section: str, key: str, fallback: Optional[bool] = None) -> bool:
        """
        Get a configuration value as a boolean.

        Recognizes: true, yes, 1, on (case-insensitive) as True
        Recognizes: false, no, 0, off (case-insensitive) as False

        Args:
            section: Configuration section name
            key: Configuration key name
            fallback: Default value if not found

        Returns:
            Configuration value as boolean
        """
        value = self.get(section, key, fallback=None)

        if value is None:
            if fallback is not None:
                return fallback
            raise ConfigError(
                f"Boolean configuration key not found: [{section}] {key}"
            )

        return value.lower() in ('true', 'yes', '1', 'on')

    def get_int(self, section: str, key: str, fallback: Optional[int] = None) -> int:
        """
        Get a configuration value as an integer.

        Args:
            section: Configuration section name
            key: Configuration key name
            fallback: Default value if not found

        Returns:
            Configuration value as integer

        Raises:
            ConfigError: If value cannot be converted to integer
        """
        value = self.get(section, key, fallback=None)

        if value is None:
            if fallback is not None:
                return fallback
            raise ConfigError(
                f"Integer configuration key not found: [{section}] {key}"
            )

        try:
            return int(value)
        except ValueError:
            raise ConfigError(
                f"Configuration value is not an integer: [{section}] {key} = {value}"
            )

    def get_float(self, section: str, key: str, fallback: Optional[float] = None) -> float:
        """
        Get a configuration value as a float.

        Args:
            section: Configuration section name
            key: Configuration key name
            fallback: Default value if not found

        Returns:
            Configuration value as float

        Raises:
            ConfigError: If value cannot be converted to float
        """
        value = self.get(section, key, fallback=None)

        if value is None:
            if fallback is not None:
                return fallback
            raise ConfigError(
                f"Float configuration key not found: [{section}] {key}"
            )

        try:
            return float(value)
        except ValueError:
            raise ConfigError(
                f"Configuration value is not a float: [{section}] {key} = {value}"
            )

    def get_list(self, section: str, key: str, separator: str = ",",
                 fallback: Optional[List[str]] = None) -> List[str]:
        """
        Get a configuration value as a list of strings.

        Splits a comma-separated (or custom separator) value into a list.

        Args:
            section: Configuration section name
            key: Configuration key name
            separator: Character(s) to split on (default: comma)
            fallback: Default list if not found

        Returns:
            Configuration value as list of strings
        """
        value = self.get(section, key, fallback=None)

        if value is None:
            if fallback is not None:
                return fallback
            raise ConfigError(
                f"List configuration key not found: [{section}] {key}"
            )

        return [v.strip() for v in value.split(separator) if v.strip()]

    def sections(self) -> List[str]:
        """
        Get all configuration sections.

        Returns:
            List of section names
        """
        return self.parser.sections()

    def section_items(self, section: str) -> Dict[str, str]:
        """
        Get all key-value pairs in a section.

        Args:
            section: Configuration section name

        Returns:
            Dictionary of key-value pairs

        Raises:
            ConfigError: If section doesn't exist
        """
        if not self.parser.has_section(section):
            raise ConfigError(f"Configuration section not found: [{section}]")

        return dict(self.parser.items(section))

    def validate(self) -> Dict[str, List[str]]:
        """
        Validate required configuration values are present.

        Required keys (section, key):
        - (project, PROJECT_NAME)
        - (frontend, FRONTEND_FRAMEWORK)
        - (backend, BACKEND_LANGUAGE)
        - (api_integration, RIOT_API_KEY)
        - (security, SECRET_KEY)
        - (security, JWT_SECRET)

        Returns:
            Dictionary of validation results with errors list

        Raises:
            ConfigError: If critical configuration is missing
        """
        required_keys = [
            ('project', 'PROJECT_NAME'),
            ('project', 'ENVIRONMENT'),
            ('frontend', 'FRONTEND_FRAMEWORK'),
            ('frontend', 'FRONTEND_PORT'),
            ('backend', 'BACKEND_LANGUAGE'),
            ('backend', 'BACKEND_PORT'),
            ('api_integration', 'RIOT_API_KEY'),
            ('security', 'SECRET_KEY'),
            ('security', 'JWT_SECRET'),
        ]

        missing = []
        found = []

        for section, key in required_keys:
            try:
                value = self.get(section, key)
                if value and not value.startswith('your-') and not value.startswith('RGAPI-YOUR'):
                    found.append(f"✓ [{section}] {key}")
                else:
                    missing.append(f"✗ [{section}] {key} - placeholder value detected")
            except ConfigError:
                missing.append(f"✗ [{section}] {key} - not configured")

        if missing:
            raise ConfigError(
                f"Configuration validation failed. Missing or incomplete:\n" +
                "\n".join(missing) +
                f"\n\nFound {len(found)} required configurations.\n" +
                f"Please update development.cfg.local with actual values."
            )

        return {'missing': missing, 'found': found}

    def export_env_vars(self) -> Dict[str, str]:
        """
        Export all configuration as environment variables.

        Returns:
            Dictionary suitable for os.environ.update()
        """
        env_vars = {}

        for section in self.sections():
            for key, value in self.section_items(section).items():
                env_key = f"{section.upper()}_{key}".upper()
                env_vars[env_key] = value

        return env_vars

    def __repr__(self) -> str:
        """Return string representation of configuration."""
        sections = self.sections()
        total_keys = sum(len(self.section_items(s)) for s in sections)
        return (
            f"Config(sections={len(sections)}, keys={total_keys}, "
            f"local={'present' if self.local_config_file.exists() else 'missing'})"
        )


def initialize_config(config_dir: str = ".") -> Config:
    """
    Initialize configuration and validate setup.

    This is the recommended way to load configuration at application startup.

    Args:
        config_dir: Directory containing development.cfg

    Returns:
        Initialized and validated Config object

    Raises:
        ConfigError: If configuration is invalid or incomplete
    """
    try:
        config = Config(config_dir)
        config.validate()
        return config
    except ConfigError as e:
        print(f"Configuration Error: {e}", file=sys.stderr)
        sys.exit(1)


# Example usage and testing
if __name__ == "__main__":
    """
    Test script for configuration loader.

    Usage:
        python -m utils.config_loader
    """
    try:
        # Load configuration
        config = Config()
        print(f"✓ Configuration loaded: {config}")

        # Display all sections
        print("\nConfiguration Sections:")
        for section in config.sections():
            items = config.section_items(section)
            print(f"  [{section}] ({len(items)} keys)")

        # Show sample values
        print("\nSample Values:")
        print(f"  PROJECT_NAME: {config.get('project', 'PROJECT_NAME')}")
        print(f"  ENVIRONMENT: {config.get('project', 'ENVIRONMENT')}")
        print(f"  FRONTEND_FRAMEWORK: {config.get('frontend', 'FRONTEND_FRAMEWORK')}")
        print(f"  BACKEND_LANGUAGE: {config.get('backend', 'BACKEND_LANGUAGE')}")
        print(f"  FRONTEND_PORT: {config.get_int('frontend', 'FRONTEND_PORT')}")
        print(f"  DEBUG_MODE: {config.get_bool('project', 'DEBUG_MODE')}")

        # Validate configuration
        print("\nValidating Configuration...")
        config.validate()
        print("✓ Configuration validation passed!")

    except ConfigError as e:
        print(f"✗ Configuration Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected Error: {e}", file=sys.stderr)
        sys.exit(1)
