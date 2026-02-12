# src/first_agent/__init__.py

"""
first_agent package.

Public API surface:
- GradioUI: UI wrapper to launch agent in Gradio
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("first_agent")
except PackageNotFoundError:
    # When running from source without installation
    __version__ = "0.0.0"

# Keep imports lightweight: only re-export core public objects.
from .ui import GradioUI  # noqa: E402

__all__ = [
    "GradioUI",
    "__version__",
]
