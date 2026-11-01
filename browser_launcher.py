"""
Cross-platform browser launcher.
Uses termux_playwright on Android/Termux, falls back to playwright elsewhere.
"""
import os

from dotenv import load_dotenv

load_dotenv()

IS_TERMUX = (
    "com.termux" in os.environ.get("PREFIX", "")
    or os.path.exists("/data/data/com.termux")
)


async def create_browser_context(
    playwright_instance, headless=True, context_kwargs=None, **kwargs
):
    """Create a browser + context compatible with Termux and desktop."""
    launch_kwargs = dict(kwargs)
    if IS_TERMUX:
        from termux_playwright import launch

        headless = True
        launch_kwargs.setdefault(
            "executable_path",
            os.getenv(
                "CHROMIUM_PATH",
                "/data/data/com.termux/files/usr/bin/chromium-browser",
            ),
        )
        browser = await launch(
            playwright_instance,
            headless=headless,
            single_process=True,
            low_memory_mode=True,
            **launch_kwargs,
        )
    else:
        browser = await playwright_instance.chromium.launch(
            headless=headless,
            args=["--no-sandbox", "--disable-dev-shm-usage"],
            **launch_kwargs,
        )

    options = {
        "user_agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    if context_kwargs:
        options.update(context_kwargs)
    context = await browser.new_context(**options)
    return browser, context


def get_async_playwright():
    """Return the correct async_playwright context manager."""
    if IS_TERMUX:
        from termux_playwright import async_playwright_termux

        return async_playwright_termux()

    from playwright.async_api import async_playwright

    return async_playwright()
