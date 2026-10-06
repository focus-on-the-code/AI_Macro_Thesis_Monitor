"""Hosted browser smoke checks for the Phase 1 Streamlit shell."""

from __future__ import annotations

import argparse
from pathlib import Path

from playwright.sync_api import sync_playwright


PAGES = ("Dashboard", "Evidence", "About", "Definitions & Methodology")
OUT = Path("artifacts/phase1-browser")


def wait_ready(page) -> None:
    page.wait_for_load_state("domcontentloaded")
    page.get_by_role("link", name="Dashboard", exact=True).wait_for(timeout=15_000)


def no_horizontal_overflow(page) -> None:
    overflow = page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 2")
    assert not overflow, f"horizontal overflow at viewport {page.viewport_size}"


def click_page(page, name: str) -> None:
    page.get_by_role("link", name=name, exact=True).click()
    page.wait_for_timeout(500)
    wait_ready(page)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8501")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 1000})
        page.goto(args.base_url)
        wait_ready(page)

        dashboard_text = page.locator("body").inner_text()
        for panel_id in range(1, 8):
            assert f"V{panel_id} —" in dashboard_text, f"missing V{panel_id} panel"
        assert page.get_by_text("Energy", exact=False).count() >= 1
        assert page.get_by_text("Labor", exact=False).count() >= 1
        dashboard_text = dashboard_text.upper()
        assert "STALE" in dashboard_text
        assert "UNAVAILABLE" in dashboard_text
        assert page.get_by_text("How this is calculated", exact=True).count() == 7

        page.screenshot(path=str(OUT / "dashboard-desktop.png"), full_page=True)
        for name in PAGES[1:]:
            click_page(page, name)
            assert page.get_by_role("heading", name=name).count() >= 1
            page.screenshot(path=str(OUT / (name.split()[0].lower() + "-desktop.png")), full_page=True)

        click_page(page, "Dashboard")
        for name in PAGES[1:]:
            click_page(page, name)
        page.set_viewport_size({"width": 1024, "height": 900})
        click_page(page, "Dashboard")
        no_horizontal_overflow(page)
        page.screenshot(path=str(OUT / "dashboard-tablet.png"), full_page=True)
        page.set_viewport_size({"width": 390, "height": 844})
        page.reload()
        wait_ready(page)
        no_horizontal_overflow(page)
        page.screenshot(path=str(OUT / "dashboard-mobile.png"), full_page=True)
        browser.close()


if __name__ == "__main__":
    main()
