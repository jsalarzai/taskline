#!/usr/bin/env python3
"""Taskline: a simple CLI task manager."""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

TASKS_FILE = Path.home() / ".taskline.json"
