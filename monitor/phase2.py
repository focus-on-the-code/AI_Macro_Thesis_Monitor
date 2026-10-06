"""Phase 2 registry, explicit calculations, provenance and quality metadata."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import hashlib
from typing import Iterable


_ROOT = Path(__file__).resolve().parents[1]
_SOURCES = {
    "V1": ("Provider price pages; approved public usage proxies; company disclosures", "Provider snapshot / proxy cadence"),
    "V2": ("SEC EDGAR filings; company investor relations", "Quarterly; event-driven disclosures"),
    "V3": ("U.S. Treasury; FRED/ALFRED; approved public FX source", "Daily / source frequency"),
    "V4": ("Treasury Fiscal Data; TreasuryDirect; BEA/FRED", "Daily / monthly / quarterly by series"),
    "V5": ("Census BTOS; BLS; BEA", "Biweekly / quarterly by series"),
    "V6": ("EIA; approved public ISO/RTO source", "Hourly / daily / monthly by series"),
    "V7": ("BLS; Department of Labor; FRED", "Weekly / monthly by series"),
}
_UNITS = {
    "V1-F01": "index (base=100)", "V1-F02": "index (base=100)",
    "V1-F03": "percent", "V1-F04": "percent", "V1-F05": "ratio (proxy)",
    "V2-F01": "USD (company reporting scale)", "V2-F02": "USD (company reporting scale)",
    "V2-F03": "fraction", "V2-F04": "ratio", "V2-F05": "fraction",
    "V2-F06": "ratio", "V2-F07": "USD (company reporting scale)",
    "V2-F08": "percent (disclosed only)", "V2-F09": "USD (disclosed scale)",
    "V3-F01": "percent", "V3-F02": "percent", "V3-F03": "percent",
    "V3-F04": "basis points", "V3-F05": "percent", "V3-F06": "percent",
    "V3-F07": "percent", "V3-F08": "index points",
    "V4-F01": "USD", "V4-F02": "USD (receipts minus outlays)",
    "V4-F03": "USD", "V4-F04": "fraction", "V4-F05": "fraction",
    "V4-F06": "ratio", "V4-F07": "percent",
    "V5-F01": "percent", "V5-F02": "percent", "V5-F03": "percent",
    "V5-F04": "index / source unit", "V5-F05": "USD (real, source scale)",
    "V5-F06": "USD (real, source scale)",
    "V6-F01": "source unit (documented aggregation)", "V6-F02": "USD per kWh (source unit)",
    "V6-F03": "USD per MMBtu", "V6-F04": "USD per barrel",
    "V6-F05": "MW (source unit)", "V7-F01": "percent",
    "V7-F02": "persons (seasonally adjusted source unit)", "V7-F03": "claims (persons)",
    "V7-F04": "persons or percent (source series label required)",
    "V7-F05": "hours", "V7-F06": "percent", "V7-F07": "persons (industry series)",
}
_FORMULAS = {
    "V1-F01": "current basket cost / base-date basket cost * 100",
    "V1-F02": "observed proxy tokens / base-date proxy tokens * 100",
    "V1-F03": "open-weight observed tokens / total observed tokens * 100",
    "V1-F04": "frontier/proprietary observed tokens / total observed tokens * 100",
    "V1-F05": "% change in observed tokens / absolute % decline in effective workload price",
    "V2-F01": "sum(most recent four quarterly capex observations)",
    "V2-F02": "TTM operating cash flow - TTM capex",
    "V2-F03": "current TTM capex / prior-year TTM capex - 1",
    "V2-F04": "TTM operating cash flow / TTM capex",
    "V2-F05": "TTM free cash flow / TTM revenue",
    "V2-F06": "TTM EBIT / TTM interest expense (comparable inputs only)",
    "V2-F07": "current total debt - prior-year total debt",
    "V3-F04": "(10Y yield in percent - 2Y yield in percent) * 100 basis points per percentage point",
    "V4-F02": "sum(monthly receipts - monthly outlays, most recent 12 months)",
    "V4-F03": "sum(monthly net interest outlays, most recent 12 months)",
    "V4-F04": "rolling-12-month net interest / rolling-12-month receipts",
    "V4-F05": "debt held by public / comparable nominal GDP",
    "V4-F07": "indirect bidder accepted / total accepted * 100",
    "V6-F01": "documented aggregation of approved hourly/daily demand observations",
    "V4-F06": "published current bid-to-cover; deviation = current - median of trailing 12 comparable auctions",
}
CALCULATED_FORMULA_IDS = frozenset(_FORMULAS)
_FORMULA_SNAPSHOT = "61ccd6bb51d6f4a991fee107c8b002920f1dbbaae8edd55b7beef8ba9f076ead"
_REGISTRY_SNAPSHOT = "d2d83a7f5fbb68719d482973f34faa52dce33dc608fac83b6c754bcf20013ddc"


@dataclass(frozen=True)
class Provenance:
    raw_input_ids: tuple[str, ...]
    source_url: str
    observed_at: str
    retrieved_at: str
    vintage_state: str = "NOT_APPLICABLE"
    revision_state: str = "NOT_REVISED"
    transformation: str = "raw observation"


@dataclass(frozen=True)
class QualityFlags:
    status: str = "OK"
    flags: tuple[str, ...] = ()
    reason: str = ""


def metric_registry() -> dict[str, dict]:
    """Return stable registry entries enriched from the frozen v0.91 inventory."""
    inventory = json.loads((_ROOT / "registry/formula-inventory.json").read_text(encoding="utf-8"))
    result = {}
    for entry in inventory:
        panel = entry["panel_id"]
        sid, cadence = _SOURCES[panel]
        mid = entry["formula_id"]
        result[mid] = {
            **entry,
            "metric_id": mid,
            "name": entry["metric"],
            "unit": _UNITS[mid],
            "kind": "derived" if mid in _FORMULAS else "raw",
            "formula": _FORMULAS.get(mid),
            "source_priority": [sid],
            "cadence": cadence,
        }
    return result


def formula_snapshot_matches() -> bool:
    payload = (_ROOT / "registry/formula-inventory.json").read_bytes()
    code_registry = json.dumps(_FORMULAS, sort_keys=True, separators=(",", ":")).encode()
    return (hashlib.sha256(payload).hexdigest() == _FORMULA_SNAPSHOT and
            hashlib.sha256(code_registry).hexdigest() == _REGISTRY_SNAPSHOT)


def normalize_unit(value: float | None, unit: str, expected: str) -> float:
    """Normalize explicitly compatible ratios; never guess a unit."""
    if value is None:
        raise ValueError("missing input")
    if unit == expected:
        return float(value)
    ratio_units = {"fraction": 1.0, "percent": 100.0, "basis points": 10000.0}
    if expected in ratio_units and unit in ratio_units:
        return float(value) * ratio_units[expected] / ratio_units[unit]
    raise ValueError(f"incompatible unit {unit!r}; expected {expected!r}")


def calculate(formula_id: str, values: Iterable[float | None], units: Iterable[str]) -> float:
    """Evaluate supported frozen formula patterns with explicit missing/zero checks."""
    vals, actual_units = list(values), list(units)
    if len(vals) != len(actual_units) or any(v is None for v in vals):
        raise ValueError("missing or mismatched inputs")
    nums = [float(v) for v in vals]
    if not all(__import__("math").isfinite(v) for v in nums):
        raise ValueError("inputs must be finite")
    if formula_id in {"V1-F01", "V1-F02"}:
        if actual_units[0] != actual_units[1]:
            raise ValueError("index numerator and base must use identical units")
        if nums[1] == 0:
            raise ZeroDivisionError("base value is zero")
        return nums[0] / nums[1] * 100
    if formula_id == "V1-F05":
        if nums[0] == 0 and nums[1] == 0:
            raise ZeroDivisionError("price decline is zero")
        if nums[1] == 0:
            raise ZeroDivisionError("price decline is zero")
        return nums[0] / abs(nums[1])
    if formula_id == "V2-F01":
        if len(nums) != 4 or len(set(actual_units)) != 1:
            raise ValueError("TTM capex requires four quarterly values in identical units")
        return sum(nums)
    if formula_id == "V4-F02":
        if len(nums) != 24 or len(set(actual_units)) != 1:
            raise ValueError("rolling deficit requires 12 receipts and 12 outlays in identical units")
        return sum(nums[:12]) - sum(nums[12:])
    if formula_id == "V4-F03":
        if len(nums) != 12 or len(set(actual_units)) != 1:
            raise ValueError("rolling net interest requires 12 monthly values in identical units")
        return sum(nums)
    if formula_id == "V6-F01":
        if len(set(actual_units)) != 1:
            raise ValueError("aggregation observations must use identical units")
        return sum(nums)
    if formula_id == "V4-F06":
        if len(nums) != 13 or len(set(actual_units)) != 1:
            raise ValueError("auction comparison requires current value and 12 comparable auctions")
        ordered = sorted(nums[1:])
        median = (ordered[5] + ordered[6]) / 2
        return nums[0] - median
    if formula_id == "V3-F04":
        a = normalize_unit(nums[0], actual_units[0], "percent")
        b = normalize_unit(nums[1], actual_units[1], "percent")
        return (a - b) * 100
    if formula_id in {"V2-F02", "V2-F07"}:
        if actual_units[0] != actual_units[1]:
            raise ValueError("subtraction inputs must use identical units")
        return nums[0] - nums[1]
    if formula_id in {"V2-F03", "V2-F04", "V2-F05", "V2-F06", "V4-F04", "V4-F05", "V4-F07", "V1-F03", "V1-F04"}:
        if actual_units[0] != actual_units[1]:
            raise ValueError("ratio inputs must use identical units")
        if nums[1] == 0:
            raise ZeroDivisionError("denominator is zero")
        ratio = nums[0] / nums[1]
        return (ratio - 1 if formula_id == "V2-F03" else ratio) * (100 if formula_id in {"V1-F03", "V1-F04", "V4-F07"} else 1)
    raise ValueError(f"no executable calculation registered for {formula_id}")


def derive_provenance(formula_id: str, inputs: Iterable[tuple[str, Provenance]], *, observed_at: str, retrieved_at: str) -> Provenance:
    rows = list(inputs)
    if not rows:
        raise ValueError("derived provenance requires raw inputs")
    raw_ids = tuple(dict.fromkeys(raw_id for metric_id, p in rows for raw_id in (p.raw_input_ids or (metric_id,))))
    urls = tuple(dict.fromkeys(p.source_url for _, p in rows if p.source_url))
    return Provenance(raw_ids, " | ".join(urls), observed_at, retrieved_at,
                      vintage_state="MIXED_OR_SOURCE_DECLARED",
                      revision_state="REVISIONS_PRESERVED_OR_SOURCE_DECLARED",
                      transformation=formula_id + " <- " + ", ".join(metric_id for metric_id, _ in rows))


def quality_for(status: str, reason: str = "") -> QualityFlags:
    if status == "STALE":
        return QualityFlags(status, ("STALE",), reason)
    if status == "UNAVAILABLE":
        return QualityFlags(status, ("MISSING", "UNAVAILABLE"), reason)
    if status == "FIXTURE":
        return QualityFlags("ILLUSTRATIVE", ("FIXTURE", "NOT_LIVE"), "Synthetic fixture value")
    return QualityFlags(status or "OK")
