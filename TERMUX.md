# Android / Termux diagnostics

## Support status

This branch supports **environment diagnostics only** on Android / Termux. It does
not establish that the repository's third-party browser workflow is compatible
with Android, and it does not provide a supported way to automate engagement
on a TikTok account.

Do not run `main.py`, `tui_main.py`, or `install.py` on a personal account
as a compatibility test. The diagnostic passing is not a go-ahead to run the
engagement workflow.

## Prepare Termux

Install only the tools needed for the read-only diagnostic:

```sh
pkg update
pkg install python git
```

Clone the repository and enter the diagnostics branch:

```sh
git clone https://github.com/mic3ul/weird-Automation.git
cd weird-Automation
git switch termux-preflight
```

Run the diagnostic:

```sh
python termux_check.py
```

The script checks the Termux environment, Python version (3.10+), CPU
architecture, pip, optional package presence, Git, and the home directory.
It makes no network requests, installs no packages, and does not launch a
browser.

## Interpreting the result

- `[OK]` means that a local environment check passed.
- `[INFO]` for Requests or Playwright means the package is absent; neither is
  required to run this diagnostic.
- ARM64 recognition does not prove that a compatible Chromium/browser runtime
  exists.
- Installing the Playwright Python package alone does not install or validate
  a working Android browser runtime.
- A successful diagnostic is not evidence that third-party automation works.

If a diagnostic check fails, share the complete terminal output for analysis.
Do not share account passwords, session cookies, authentication tokens, or
private browser profiles.

## Automated tests

GitHub Actions runs the read-only unit tests against Python 3.10, 3.11, 3.12,
3.13, and 3.14 when the relevant files change on this branch. These tests cover
environment-detection logic only. They do not run Android, launch Chromium,
connect to TikTok, or test engagement automation.

## Safe next validation

The next useful Termux validation is limited to confirming that the diagnostic
and its unit tests behave consistently on the device. Browser compatibility
must be assessed separately in a controlled environment that you own or are
authorized to test; do not use a personal social-media account as a test target.
