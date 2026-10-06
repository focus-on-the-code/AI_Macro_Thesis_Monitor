"""Phase 1 contract checks that run without a browser or live services."""

from contextlib import nullcontext
from dataclasses import replace
from pathlib import Path
import runpy
import sys
import types
import unittest
from unittest.mock import patch

from monitor.fixtures import PANELS, REGIME, formula_inventory
from monitor import ui


ROOT = Path(__file__).resolve().parents[1]


class Recorder:
    def __init__(self):
        self.calls = []
        self.sidebar = self
        self.pages = []

    def __getattr__(self, name):
        def record(*args, **kwargs):
            self.calls.append((name, args, kwargs))
            if name == "columns":
                return [nullcontext() for _ in range(args[0])]
            if name in {"container", "expander"}:
                return nullcontext()
            if name == "Page":
                self.pages.append((args, kwargs))
                return (args, kwargs)
            if name == "navigation":
                return types.SimpleNamespace(run=lambda: self.calls.append(("run", (), {})))
            return None
        return record

    def named(self, name):
        return [call for call in self.calls if call[0] == name]


class Phase1UITests(unittest.TestCase):
    def setUp(self):
        self.st = Recorder()

    def test_p1_t01_navigation_and_page_render_reentry(self):
        for _ in range(2):  # a fresh app execution models a direct URL refresh
            st = Recorder()
            with patch.dict(sys.modules, {"streamlit": st}):
                runpy.run_path(str(ROOT / "app.py"), run_name="__main__")
                self.assertEqual([p[1]["title"] for p in st.pages],
                                 ["Dashboard", "Evidence", "About", "Definitions & Methodology"])
                self.assertEqual(len(st.named("run")), 1)
                for path, _ in st.pages:
                    runpy.run_path(str(ROOT / path[0]), run_name="__main__")
            self.assertEqual(len(st.named("title")), 4)
            self.assertEqual(len(st.named("warning")), 6)  # seven-panel states also warn twice

    def test_p1_t02_panel_inventory(self):
        self.assertEqual([panel.id for panel in PANELS], [f"V{i}" for i in range(1, 8)])
        self.assertNotEqual(PANELS[5].name, PANELS[6].name)
        ui.dashboard(self.st)
        headings = [call[1][0] for call in self.st.named("subheader")]
        self.assertEqual([h for h in headings if h.startswith("V")],
                         [f"{p.id} — {p.name}" for p in PANELS])
        self.assertEqual(len(REGIME), 10)

    def test_p1_t03_ticker_proximity(self):
        for panel in PANELS:
            st = Recorder()
            ui.render_panel(st, panel, formula_inventory())
            headings = [c[1][0] for c in st.named("subheader")]
            self.assertEqual(headings, [f"{panel.id} — {panel.name}"])
            tables = st.named("table")
            self.assertEqual(len(tables), 1)
            self.assertEqual([row["Instrument"] for row in tables[0][1][0]], list(panel.tickers))
            self.assertIn("market proxies", " ".join(c[1][0] for c in st.named("markdown")))

    def test_p1_t04_disclosures(self):
        inventory = formula_inventory()
        for panel in PANELS:
            st = Recorder()
            ui.render_panel(st, panel, inventory)
            self.assertEqual([c[1][0] for c in st.named("expander")], ["How this is calculated"])
            content = " ".join(str(c[1][0]) for c in st.named("write"))
            for expected in (inventory[panel.metric.formula_id]["definition"],
                             panel.metric.raw_inputs, panel.metric.unit, panel.metric.source,
                             "Observation date:", "retrieval date:", "revision/vintage:"):
                self.assertIn(expected, content)

    def test_p1_t05_layout_structure(self):
        # Structural smoke only; actual tablet/desktop rendering needs Streamlit and browser QA.
        ui.dashboard(self.st)
        self.assertEqual([c[1][0] for c in self.st.named("columns")], [2] * 5)
        self.assertEqual(len(self.st.named("container")), 7)
        self.assertTrue(all(set(c[1][0][0]) == {"Instrument", "Price", "Change"}
                            for c in self.st.named("table")[:7]))

    def test_p1_t06_stale_unavailable_and_missing_injection(self):
        statuses = {panel.metric.status for panel in PANELS}
        self.assertTrue({"FIXTURE", "STALE", "UNAVAILABLE"}.issubset(statuses))
        missing = replace(PANELS[0], metric=replace(PANELS[0].metric, value=None,
                          status="UNAVAILABLE", reason="Injected missing fixture", last_success="2026-09-01"))
        ui.render_panel(self.st, missing, formula_inventory())
        warning = self.st.named("warning")[0][1][0]
        self.assertIn("UNAVAILABLE", warning)
        self.assertIn("2026-09-01", warning)
        self.assertIn("Injected missing fixture", warning)
        self.assertEqual(self.st.named("metric")[0][1][1], "Unavailable")
        self.assertEqual(len(self.st.named("expander")), 1)


if __name__ == "__main__":
    unittest.main()
