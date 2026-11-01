"""Unit tests for the read-only Termux diagnostics."""
from termux_check import is_supported_architecture, is_termux_environment


def test_detects_termux_prefix():
    assert is_termux_environment({"PREFIX": "/data/data/com.termux/files/usr"})


def test_rejects_non_termux_prefix():
    assert not is_termux_environment({"PREFIX": "/usr"})


def test_missing_prefix_is_not_termux():
    assert not is_termux_environment({})


def test_accepts_arm64_architecture_names():
    assert is_supported_architecture("aarch64")
    assert is_supported_architecture("arm64")


def test_rejects_unvalidated_architecture():
    assert not is_supported_architecture("x86_64")
