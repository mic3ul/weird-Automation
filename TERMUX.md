# Android / Termux diagnostics

## Scope

This repository's Termux support is limited to a read-only environment check.
It does **not** make the Zefoy/TikTok interaction automation, browser workflow,
CAPTCHA handling, or anti-detection code supported on Android. Do not run
`main.py`, `tui_main.py`, or the desktop installer expecting the automation
to work in Termux.

## Prepare Termux

Install Python and Git from the Termux package manager:

```sh
pkg update
pkg install python git
```

Clone the repository and enter its directory:

```sh
git clone https://github.com/mic3ul/weird-Automation.git
cd weird-Automation
git switch termux-preflight
```

Run the read-only diagnostic:

```sh
python termux_check.py
```

The script checks the Termux environment, Python version, CPU architecture,
pip, selected Python packages, Git, and the home directory. It makes no network
requests and does not launch a browser.

## Interpreting the result

- A successful result means only that the basic environment checks passed.
- It does **not** prove that Playwright or Chromium can run on this Android
  device.
- A missing Playwright package is informational; installing it will not by
  itself provide a compatible browser runtime.
- If a check fails, share the complete terminal output for diagnosis.

## Tests

The diagnostic unit tests are run automatically by GitHub Actions for Python
3.10, 3.11, and 3.12 when relevant files change. They test environment-detection
logic only; they do not test browser compatibility or third-party automation.
