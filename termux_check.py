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


def is_termux_environment(environ: Mapping[str, str] | None = None) -> bool:
    """Return whether the process appears to be running inside Termux."""
    env = os.environ if environ is None else environ
    return env.get("PREFIX", "").startswith("/data/data/com.termux")


def is_supported_architecture(machine: str | None = None) -> bool:
    """Check for the ARM64 architectures commonly reported on Android."""
    value = (machine or platform.machine()).lower()
    return value in {"aarch64", "arm64"}


def check(label: str, ok: bool, detail: str) -> None:
    marker = "OK" if ok else "MISSING/UNSUPPORTED"
    print(f"[{marker}] {label}: {detail}")


def main() -> int:
    is_termux = is_termux_environment()
    machine = platform.machine() or "unknown"
    python_ok = sys.version_info >= (3, 10)
    arch_ok = is_supported_architecture(machine)
    pip_ok = importlib.util.find_spec("pip") is not None
    requests_ok = importlib.util.find_spec("requests") is not None
    playwright_ok = importlib.util.find_spec("playwright") is not None

    check("Termux", is_termux, "Termux environment detected" if is_termux else "not running inside Termux")
    check("Python >= 3.10", python_ok, platform.python_version())
    check("Architecture", arch_ok, machine)
    check("pip", pip_ok, "available" if pip_ok else "not installed")
    check("Requests package", requests_ok, "installed" if requests_ok else "not installed")
    check("Playwright package", playwright_ok, "installed" if playwright_ok else "not installed")
    git_path = shutil.which("git")
    check("Git", git_path is not None, git_path or "not found on PATH")
    home = os.path.expanduser("~")
    check("Home directory", os.path.isdir(home), home)

    print("\nDiagnostic only: passing these checks does not certify browser compatibility.")
    print("Android browser/runtime support must be validated independently.")
    print("This project does not provide automated engagement, CAPTCHA solving, or evasion support.")
    return 0 if is_termux and python_ok and arch_ok and pip_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
