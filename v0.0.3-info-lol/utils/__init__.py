"""
Utilities package for The Summoner's Chronicle development pipeline.

This package contains shared utilities and helper modules used across
the project.

Modules:
    config_loader: Configuration management and environment variable handling
"""

from .config_loader import Config, ConfigError, initialize_config

__all__ = ['Config', 'ConfigError', 'initialize_config']
__version__ = '1.0.0'
