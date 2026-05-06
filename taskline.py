#!/usr/bin/env python3
"""Taskline: a simple CLI task manager."""

# Imports & Constants

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

TASKS_FILE = Path.home() / ".taskline.json"

# File I/O Helpers

def get_tasks_path() -> Path: # -> Path is the return type annotation that returns a `Path` object.
    """Return the path to the JSON storage file."""
    return TASKS_FILE

def load_tasks() -> List[Dict]:
    """Load tasks from file, return empty list if missing or corrupted."""
    path = get_tasks_path()
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError):
        return []

def save_tasks(tasks: List[Dict]) -> None:
    """Write the task list to the JSON file."""
    path = get_tasks_path()
    # Ensure parent directory exists (though it's home)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, default=str)

def add_task():

def list_tasks():

def remove_task():

def done_task():

def clear_tasks():

main():
