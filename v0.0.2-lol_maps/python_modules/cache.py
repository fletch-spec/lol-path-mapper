"""Cache.py
This file handles init, IO, and destruct of the _cache (replays, timelines, )

"""


print("[LOADING]: Cache module...", end="")

from .classes import MatchDirectory

class CacheController:
    def __init__(self, cli, config, reset=False):
        try:
            self.cli = cli
            self.load_config(config)
            self.initialize(reset)
        except Exception as e:
            self.cli(f"{e}")

    def load_config(self, config):
        _root = config.get("root_directory", ".")
        self.cache_dir = os.path.join(_root, "_cache")
        self.matchDirectory = MatchDirectory(self.cache_dir)
        self.output_dir = os.path.join(_root, "output")

    def initialize(self, reset):
        if reset:
            self.wipe_cache()
        self.create_cache()
        self.create_output()
        from ._test.cache_tests import run_test
        if run_test(self):
            return 0

    def create_cache(self):
        os.makedirs(self.cache_dir, exist_ok=True)
        for child in ["replay_files", "render_data", "json_matches"]:
            child_dir = os.path.join(self.cache_dir, child)
            os.makedirs(child_dir, exist_ok=True)

    def create_output(self):
        os.makedirs(self.output_dir, exist_ok=True)
        for child in ["renders", "analyzed_matches"]:
            child_dir = os.path.join(self.output_dir, child)
            os.makedirs(child_dir, exist_ok=True)

    def wipe_cache(self):
        self.cli("Attemping wipe..")
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)
        else:
            raise Exception("Failed to wipe cache")

    def get_output_dir(self):
        return self.output_dir


import json
import os
import re
import struct
import sys
import shutil
from datetime import datetime, timezone


if __name__ == "__main__":
    print("This module is not meant to be run directly. Please run main.py instead.")

def create_cache(cache_dir):
    """Create the cache directory if it doesn't exist."""
    os.makedirs(cache_dir, exist_ok=True)
    replay_dir = os.path.join(cache_dir, "replay_files")
    os.makedirs(replay_dir, exist_ok=True)

def wipe_cache(cache_dir):
    """Delete all files in the cache directory."""
    if os.path.exists(cache_dir):
        print(f"Cache exists at: {os.path.abspath(cache_dir)}")
        print(f"Files before deletion: {os.listdir(cache_dir)}")
        shutil.rmtree(cache_dir)
        print(f"Deleted. Exists now: {os.path.exists(cache_dir)}")
    else:
        print(f"Cache directory '{cache_dir}' does not exist.")

def reset_cache(cache_dir):
    """Wipe the cache and recreate the directory structure."""
    wipe_cache(cache_dir)
    create_cache(cache_dir)
    print("Cache has been reset.")

def save_api_key(cache_dir, api_key):
    """Save the API key to a file in the cache directory."""
    if not api_key: 
        print("No API key provided. Skipping save.")
        return
    api_key_path = os.path.join(cache_dir, "api_key.txt")
    with open(api_key_path, "w") as f:
        f.write(api_key)
    print(f"API key saved to {api_key_path}")

print('good')