"""Canonical executable surface capability registry.

This module is intentionally pure-data-first. Deployment resolution, runtime
mounting, contract generation, and modularity verification all consume the same
capability records so profile output is driven by executable surface wiring
rather than hand-maintained parallel route lists.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Final

