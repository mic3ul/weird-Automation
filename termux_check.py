#!/usr/bin/env python3
"""Read-only Termux environment diagnostics.

This utility checks the local Python/Android environment only. It does not
open Zefoy, automate TikTok interactions, solve CAPTCHAs, or send requests.
"""
from __future__ import annotations

import importlib.util
import os
import platform
import shutil
import sys


def check(label: str, ok: bool, detail: str) -> None:
    marker = "OK" if ok else "MISSING/UNSUPPORTED"
    print(f"[{marker}] {label}: {detail}")


def main() -> int:
    is_termux = bool(os.environ.get("PREFIX", "").startswith("/data/data/com.termux"))
    machine = platform.machine() or "unknown"
    check("Termux", is_termux, "Termux environment detected" if is_termux else "not running inside Termux")
    check("Python", sys.version_info >= (3, 10), platform.python_version())
    check("Architecture", machine in {"aarch64", "arm64"}, machine)
    check("pip", importlib.util.find_spec("pip") is not None, "Python package installer")
    check("Playwright package", importlib.util.find_spec("playwright") is not None,
          "installed" if importlib.util.find_spec("playwright") else "not installed")
    check("Requests package", importlib.util.find_spec("requests") is not None,
          "installed" if importlib.util.find_spec("requests") else "not installed")
    check("Git", shutil.which("git") is not None, shutil.which("git") or "not found on PATH")
    check("Storage path", os.path.isdir(os.path.expanduser("~")), os.path.expanduser("~"))
    print("\nThis is an environment report, not a compatibility certification.")
    print("Browser automation on Android requires a separately validated browser/runtime setup.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
