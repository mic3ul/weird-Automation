#!/usr/bin/env python3
"""Read-only Termux environment diagnostics.

This utility checks the local Python/Android environment only. It does not
open third-party services, automate social interactions, solve CAPTCHAs,
spoof browser fingerprints, or send network requests.
"""
from __future__ import annotations

import importlib.util
import os
import platform
import shutil
import sys
from collections.abc import Mapping


MIN_PYTHON_VERSION = (3, 10)
OPTIONAL_PACKAGES = ("requests", "playwright")


def is_termux_environment(environ: Mapping[str, str] | None = None) -> bool:
    """Return whether the process appears to be running inside Termux."""
    env = os.environ if environ is None else environ
    return env.get("PREFIX", "").startswith("/data/data/com.termux")


def is_supported_python_version(version: tuple[int, int] | None = None) -> bool:
    """Check whether the interpreter meets the diagnostic's Python baseline."""
    value = sys.version_info[:2] if version is None else version
    return value >= MIN_PYTHON_VERSION


def is_supported_architecture(machine: str | None = None) -> bool:
    """Recognize ARM64 names commonly reported on Android devices."""
    value = (machine or platform.machine()).lower()
    return value in {"aarch64", "arm64"}


def check(label: str, ok: bool, detail: str, *, optional: bool = False) -> None:
    """Print a consistent status line; absent optional packages are informational."""
    marker = "OK" if ok else ("INFO" if optional else "MISSING/UNSUPPORTED")
    print(f"[{marker}] {label}: {detail}")


def main() -> int:
    is_termux = is_termux_environment()
    machine = platform.machine() or "unknown"
    python_ok = is_supported_python_version()
    arch_ok = is_supported_architecture(machine)
    pip_ok = importlib.util.find_spec("pip") is not None

    check(
        "Termux",
        is_termux,
        "Termux environment detected" if is_termux else "not running inside Termux",
    )
    check("Python >= 3.10", python_ok, platform.python_version())
    check(
        "Architecture",
        arch_ok,
        f"{machine} (ARM64 recognized; browser compatibility not established)",
    )
    check("pip", pip_ok, "available" if pip_ok else "not installed")

    for package in OPTIONAL_PACKAGES:
        installed = importlib.util.find_spec(package) is not None
        detail = "installed" if installed else "not installed; optional for diagnostics"
        check(f"{package} package", installed, detail, optional=True)

    git_path = shutil.which("git")
    check("Git", git_path is not None, git_path or "not found on PATH")
    home = os.path.expanduser("~")
    check("Home directory", os.path.isdir(home), home)

    print("\nDiagnostic only: passing these checks does not certify browser compatibility.")
    print("ARM64 recognition does not mean a browser runtime is supported.")
    print("Optional packages are reported for information; this script installs nothing.")
    print("This project does not provide automated engagement, CAPTCHA solving, or evasion support.")
    return 0 if is_termux and python_ok and arch_ok and pip_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
