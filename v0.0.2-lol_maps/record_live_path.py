import argparse
import os
import sys

# Ensure Unicode output works on Windows terminals
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from python_modules import cache, api, render


DEFAULT_MAP = None

def make_match_dir(match_id):
    folder = os.path.join(cache.get_output_dir(), match_id)
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, f"{type_}.png")
