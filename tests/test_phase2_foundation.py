import unittest

from monitor.phase2 import (
    CALCULATED_FORMULA_IDS, Provenance, calculate, derive_provenance, formula_snapshot_matches,
    metric_registry, normalize_unit, quality_for,
)
from monitor.fixtures import PANELS


class Phase2FoundationTests(unittest.TestCase):
    def test_p2_t01_formula_examples(self):
        cases = [
            ("V3-F04", [4.35, 4.10], ["percent", "percent"], 25),
            ("V3-F04", [435, 410], ["basis points", "basis points"], 25),
            ("V2-F02", [20, 12], ["USD", "USD"], 8),
            ("V2-F03", [120, 100], ["USD", "USD"], 0.2),
            ("V2-F04", [20, 10], ["USD", "USD"], 2),
            ("V2-F05", [-2, 10], ["USD", "USD"], -0.2),
            ("V2-F06", [10, 2], ["USD", "USD"], 5),
            ("V4-F05", [5, 10], ["USD", "USD"], 0.5),
            ("V4-F07", [2, 4], ["USD", "USD"], 50),
            ("V1-F03", [25, 100], ["tokens", "tokens"], 25),
            ("V1-F05", [40, -20], ["percent", "percent"], 2),
            ("V1-F01", [8, 10], ["USD", "USD"], 80),
            ("V1-F02", [125, 100], ["tokens", "tokens"], 125),
            ("V1-F04", [25, 100], ["tokens", "tokens"], 25),
            ("V4-F04", [0, 5], ["USD", "USD"], 0),
            ("V2-F07", [-3, 2], ["USD", "USD"], -5),
            ("V2-F01", [1, 2, 3, 4], ["USD"] * 4, 10),
            ("V4-F03", [1] * 12, ["USD"] * 12, 12),
            ("V6-F01", [1, 2, 3], ["MW"] * 3, 6),
            ("V4-F06", [2.5] + [2.0] * 12, ["ratio"] * 13, 0.5),
            ("V4-F02", [10] * 12 + [8] * 12, ["USD"] * 24, 24),
        ]
        for formula, values, units, expected in cases:
            with self.subTest(formula=formula, values=values):
                self.assertAlmostEqual(calculate(formula, values, units), expected)
        with self.assertRaises(ZeroDivisionError):
            calculate("V2-F04", [1, 0], ["USD", "USD"])
        with self.assertRaises(ZeroDivisionError):
            calculate("V1-F01", [1, 0], ["USD", "USD"])
        with self.assertRaises(ValueError):
            calculate("V2-F02", [1, None], ["USD", "USD"])
        with self.assertRaises(ValueError):
            calculate("V2-F02", [1, 2], ["USD", "percent"])

    def test_p2_t02_lineage_round_trip(self):
        a = Provenance(("raw:treasury-10y",), "https://source.test/10y", "2026-09-29", "2026-10-06")
        b = Provenance(("raw:treasury-2y",), "https://source.test/2y", "2026-09-29", "2026-10-06")
        derived = derive_provenance("V3-F04", [("V3-F02", a), ("V3-F01", b)],
                                   observed_at="2026-09-29", retrieved_at="2026-10-06")
        self.assertEqual(derived.raw_input_ids, ("raw:treasury-10y", "raw:treasury-2y"))
        self.assertEqual(derived.transformation, "V3-F04 <- V3-F02, V3-F01")
        self.assertIn("source.test/10y", derived.source_url)
        self.assertIn("source.test/2y", derived.source_url)
        self.assertTrue(derived.observed_at and derived.retrieved_at and derived.vintage_state)

    def test_p2_t03_formula_snapshot_guard(self):
        self.assertTrue(formula_snapshot_matches(), "update approved formula snapshot when definitions change")
        registry = metric_registry()
        self.assertEqual({key for key, row in registry.items() if row["formula"]},
                         set(CALCULATED_FORMULA_IDS))

    def test_p2_t04_explicit_unit_normalization(self):
        self.assertAlmostEqual(normalize_unit(250, "basis points", "percent"), 2.5)
        self.assertAlmostEqual(normalize_unit(0.25, "fraction", "percent"), 25)
        with self.assertRaises(ValueError):
            normalize_unit(2.5, "USD", "percent")

    def test_p2_t05_methodology_covers_displayed_metrics(self):
        registry = metric_registry()
        shown = {panel.metric.formula_id for panel in PANELS}
        self.assertEqual(len(PANELS), 7)
        self.assertTrue(shown <= registry.keys())
        for metric_id in shown:
            row = registry[metric_id]
            self.assertTrue(row["name"] and row["unit"] and row["definition"])
            self.assertTrue(row["formula"] or row["kind"] == "raw")
            self.assertTrue(row["source_priority"] and row["cadence"])
        self.assertEqual(len(registry), 47)

    def test_quality_flags_preserve_fixture_states(self):
        self.assertIn("STALE", quality_for("STALE", "delayed").flags)
        self.assertIn("UNAVAILABLE", quality_for("UNAVAILABLE").flags)
        self.assertIn("NOT_LIVE", quality_for("FIXTURE").flags)


if __name__ == "__main__":
    unittest.main()
