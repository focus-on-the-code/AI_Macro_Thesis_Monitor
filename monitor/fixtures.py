"""Clearly fictional display fixtures for the Phase 1 UI; no network access."""

from dataclasses import dataclass
from pathlib import Path
import json


OBSERVED = "2026-09-29 (fixture)"
RETRIEVED = "2026-10-06 (fixture build)"


@dataclass(frozen=True)
class Metric:
    name: str
    value: str | None
    change: str
    unit: str
    formula_id: str
    raw_inputs: str
    source: str
    source_url: str
    cadence: str
    status: str = "FIXTURE"
    last_success: str = OBSERVED
    reason: str = ""
    raw_input_ids: tuple[str, ...] = ()
    vintage_state: str = "NOT_APPLICABLE_FIXTURE"


@dataclass(frozen=True)
class Panel:
    id: str
    name: str
    question: str
    metric: Metric
    tickers: tuple[str, ...]
    interpretation: str


REGIME = (
    ("S&P 500", "6,100", "weekly +0.4%", "market-price provider TBD"),
    ("Nasdaq", "19,800", "weekly +0.6%", "market-price provider TBD"),
    ("2Y Treasury", "4.10%", "weekly +3 bp", "U.S. Treasury"),
    ("10Y Treasury", "4.35%", "weekly +5 bp", "U.S. Treasury"),
    ("2s10s", "25 bp", "weekly +2 bp", "U.S. Treasury"),
    ("HY spread", "330 bp", "weekly +4 bp", "FRED"),
    ("Broad USD", "103.0", "weekly −0.2%", "Federal Reserve"),
    ("Brent", "$78.00", "weekly +1.2%", "EIA/market source TBD"),
    ("Henry Hub gas", "$3.10", "weekly +2.0%", "EIA"),
    ("Gold", "$2,650", "weekly −0.3%", "market-price provider TBD"),
)


PANELS = (
    Panel("V1", "AI Economics & Competition", "Is useful AI demand keeping pace with falling prices?",
          Metric("Comparable AI workload price index", "80", "−20 vs base", "index, base=100",
                 "V1-F01", "Illustrative basket cost $8; base basket cost $10; 8 / 10 × 100",
                 "Provider price pages (future source); fictional fixture", "", "Provider updates"),
          ("NVDA", "AMD", "AVGO", "GOOGL", "MSFT", "AMZN", "IGV"),
          "The fixture price index fell while the example demand proxy is not measured. Lower prices could widen adoption, but observed volume would need to rise enough to offset pressure before this signal strengthens."),
    Panel("V2", "AI Capital, Credit & Concentration", "Can investment be supported by cash flow and diverse demand?",
          Metric("TTM free cash flow", "$8B", "illustrative +$1B", "USD billions",
                 "V2-F02", "Illustrative TTM operating cash flow $20B; TTM capex $12B; 20 − 12",
                 "SEC EDGAR/company filings (future source); fictional fixture", "https://www.sec.gov/search-filings/edgar-application-programming-interfaces", "Quarterly"),
          ("MSFT", "GOOGL", "AMZN", "META", "ORCL", "NVDA", "AVGO", "AMD"),
          "The example cash surplus rose, but financing and customer concentration are not yet represented. Filing-backed capex, debt and customer disclosures would strengthen or weaken this reading."),
    Panel("V3", "Rates, Credit & Liquidity", "Are financing conditions tightening or easing?",
          Metric("2s10s spread", "25 bp", "+2 bp weekly", "basis points",
                 "V3-F04", "Illustrative 10Y 4.35%; 2Y 4.10%; (4.35 − 4.10) × 100",
                 "U.S. Treasury (future source); fictional fixture", "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve", "Daily"),
          ("TLT", "IEF", "SHY", "HYG", "LQD", "GLD"),
          "The example curve steepened slightly, while the 10Y yield remains elevated. Credit spreads and the absolute cost of capital would determine whether conditions are genuinely easing."),
    Panel("V4", "Fiscal Position", "Are financing costs and auction absorption changing?",
          Metric("Net interest / receipts", "18%", "+1 pp illustrative", "percent",
                 "V4-F04", "Illustrative rolling-12-month net interest $0.9T; receipts $5T; 0.9 / 5 × 100",
                 "Treasury Fiscal Data (future source); fictional fixture", "https://fiscaldata.treasury.gov/", "Monthly"),
          ("TLT", "IEF", "SHY", "GLD"),
          "The example interest burden rose, which could narrow fiscal flexibility. A sustained series of comparable auctions, not a single weak sale, would clarify whether absorption is deteriorating."),
    Panel("V5", "AI Productivity Diffusion", "Is AI value spreading beyond its suppliers?",
          Metric("Business AI adoption", "20%", "+3 pp illustrative", "percent of employer businesses",
                 "V5-F01", "Raw illustrative survey share: 20 of 100 employer businesses",
                 "Census BTOS (future source); fictional fixture", "https://www.census.gov/data/experimental-data-products/business-trends-and-outlook-survey.html", "Biweekly"),
          ("SPY", "RSP", "XLK", "XLI", "IGV", "IWM"),
          "The example adoption share rose, suggesting broader interest beyond suppliers. Productivity and investment measures would need to corroborate this; co-movement alone would not establish causation."),
    Panel("V6", "Energy", "Are power and fuel constraints increasing costs?",
          Metric("U.S. electricity demand", "104 index", "+4% illustrative YoY", "index, prior year=100",
                 "V6-F01", "Illustrative current demand 104 units; prior year 100; (104 / 100 − 1) × 100",
                 "EIA (future source); fictional fixture", "https://www.eia.gov/opendata/", "Daily/weekly aggregation",
                 status="STALE", last_success="2026-09-22 (fixture)",
                 reason="Simulated source delay; latest observation withheld."),
          ("XLE", "XLU", "XOP", "CEG", "VST"),
          "The last successful fixture suggested higher demand, but this panel is stale. A current demand and price series would be needed to assess whether energy costs are becoming a binding constraint."),
    Panel("V7", "Labor", "Is the labor market absorbing change?",
          Metric("Unemployment rate", None, "change unavailable", "percent",
                 "V7-F01", "Raw metric; fixture observation intentionally missing",
                 "BLS (future source); fictional fixture", "https://www.bls.gov/developers/home.htm", "Monthly",
                 status="UNAVAILABLE", last_success="2026-08-31 (fixture)",
                 reason="Simulated missing observation; no substitute or inferred value."),
          ("SPY", "RSP", "IWM", "XLY", "XLP"),
          "The current labor reading is unavailable, so no directional conclusion is warranted. Payrolls, claims and sector breadth would be needed to distinguish broad cooling from concentrated weakness."),
)


def formula_inventory() -> dict[str, dict]:
    path = Path(__file__).resolve().parents[1] / "registry" / "formula-inventory.json"
    return {entry["formula_id"]: entry for entry in json.loads(path.read_text(encoding="utf-8"))}
