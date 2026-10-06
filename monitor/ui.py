"""Phase 1 Streamlit views backed exclusively by illustrative local fixtures."""

from monitor.fixtures import OBSERVED, RETRIEVED, PANELS, REGIME, Panel, formula_inventory
from monitor.phase2 import metric_registry, quality_for


DISCLAIMER = (
    "Research and decision-support only — not investment advice. "
    "No automated trade execution. All values on this Phase 1 site are fictional fixtures, not live quotes."
)


def page_intro(st, title: str, description: str) -> None:
    st.title(title)
    st.caption(description)
    st.warning(DISCLAIMER)


def render_regime(st) -> None:
    st.subheader("Current Market & Macro Regime")
    st.caption("Illustrative fixture snapshot, not a current market reading. Changes are fictional weekly examples.")
    # Two cells per row remain readable on tablets; Streamlit stacks them on narrow screens.
    for offset in range(0, len(REGIME), 2):
        columns = st.columns(2)
        for column, (name, value, change, source) in zip(columns, REGIME[offset:offset + 2]):
            with column:
                st.metric(name, value, change, delta_color="off")
                st.caption(f"Fixture • observed {OBSERVED} • source family: {source}; market timing: not live")


def render_panel(st, panel: Panel, inventory: dict[str, dict]) -> None:
    metric = panel.metric
    definition = inventory[metric.formula_id]
    registered = metric_registry()[metric.formula_id]
    quality = quality_for(metric.status, metric.reason)
    with st.container(border=True):
        st.subheader(f"{panel.id} — {panel.name}")
        st.caption(panel.question)
        if metric.status != "FIXTURE":
            st.warning(f"{metric.status} — last successful update: {metric.last_success}. {metric.reason}")
        st.metric(metric.name, metric.value if metric.value is not None else "Unavailable",
                  metric.change if metric.value is not None else None, delta_color="off")
        st.caption(f"Unit: {metric.unit} • observed: {OBSERVED if metric.value is not None else 'missing'} • "
                   f"retrieved: {RETRIEVED} • {', '.join(quality.flags) or quality.status}")

        st.info("Chart placeholder — no historical observations are connected in Phase 1. "
                "The future chart will preserve the source frequency and provenance.")

        st.markdown("**Relevant market proxies**")
        st.caption("These instruments are market confirmation/proxies, not causal proof. "
                   "Quotes and changes are unavailable until an approved source is connected.")
        st.table([{"Instrument": ticker, "Price": "Unavailable", "Change": "Unavailable"}
                  for ticker in panel.tickers])

        st.markdown("**Interpretation (fixture scenario)**")
        st.write(panel.interpretation)

        with st.expander("How this is calculated", expanded=False):
            st.write(f"**{metric.name}** ({metric.formula_id})")
            st.write(f"Definition / formula: {definition['definition']}")
            st.write(f"Registry ID: {registered['metric_id']} • type: {registered['kind']}")
            if registered["formula"]:
                st.write(f"Calculation: {registered['formula']}")
            st.write(f"Fixture raw inputs / example: {metric.raw_inputs}")
            input_ids = metric.raw_input_ids or (f"{metric.formula_id}:fixture-input",)
            st.write(f"Lineage input IDs: {', '.join(input_ids)}")
            st.write(f"Unit: {metric.unit}")
            st.write(f"Source: {metric.source}")
            if metric.source_url:
                st.write(f"Source directory: {metric.source_url}")
            st.write(f"Observation date: {OBSERVED if metric.value is not None else 'missing'}")
            st.write(f"Fixture retrieval date: {RETRIEVED}; last successful update: {metric.last_success}")
            st.write(f"Status: {quality.status}; revision/vintage: {metric.vintage_state}. "
                     f"Source priority: {', '.join(registered['source_priority'])}. Cadence: {registered['cadence']}.")
            st.write("Limitation: this example is not an implemented live calculation; "
                     "source mapping and vintage policy remain TBD for later phases.")
            if metric.reason:
                st.write(f"Availability reason: {metric.reason}")
        st.caption(f"Source family: {metric.source} • last successful fixture update: {metric.last_success}")


def dashboard(st, panels=PANELS) -> None:
    page_intro(st, "AI / Macro Thesis Monitor",
               "Seven independent lenses on the AI investment cycle • Phase 1 fixture preview")
    render_regime(st)
    st.divider()
    inventory = formula_inventory()
    for panel in panels:
        render_panel(st, panel, inventory)
    st.subheader("Market Performance")
    st.info("Placeholder — no market-price feed is connected. Panel-specific proxies appear with each variable above.")
    st.subheader("Recent Evidence & News")
    st.info("Placeholder — no evidence or news collector is connected. The Evidence page explains the planned ledger.")
    st.subheader("Thesis summary")
    st.write("Paulsen and Eisman are hypotheses to test, not trading signals. Contradictory evidence remains visible "
             "across the seven separate panels; no master buy/sell or risk score is calculated.")


def evidence(st) -> None:
    page_intro(st, "Evidence", "The evidence ledger is a Phase 7 capability; no source ingestion is active.")
    st.info("No evidence records are loaded. Future records will distinguish PRIMARY / VERIFIED, "
            "SECONDARY / ESTIMATE and THESIS / CLAIM, with SUPPORTS / COUNTERS / AMBIGUOUS "
            "impact tied to a named hypothesis and source timestamps.")
    st.write("The fixture interpretations on Dashboard are examples, not verified claims or a live evidence balance.")


def about(st) -> None:
    page_intro(st, "About", "Why this monitor exists and what it cannot establish")
    st.write("This public-data-first research tool connects market proxies, macro data and company disclosures "
             "to inspect changes in the AI investment cycle. It began with two lenses, not conclusions:")
    st.markdown("- **Paulsen lens:** a steepening Treasury curve may precede weaker relative technology and "
                "communications earnings leadership.\n"
                "- **Eisman lens:** model price competition, capital intensity, buyer concentration and financing "
                "complexity may weaken AI infrastructure economics.\n"
                "- **Combined thesis:** returns from AI may not match the capital, energy and financing committed "
                "to produce them, particularly under restrictive rates or labor disruption.")
    st.write("Counter-evidence matters: cheaper AI may expand adoption and value for users. Correlation is not "
             "causation. Fixtures do not validate any of these claims; this phase has no live data or forecasts.")
    st.markdown("**Starting sources (hypotheses, not endorsement)**\n\n"
                "- [Jim Paulsen article](https://www.perplexity.ai/discover/you/steepening-yield-curve-signals-hFEga6XzT.ejP_SsQG4dLA)\n"
                "- [Steve Eisman interview on AI pricing](https://www.youtube.com/watch?v=2crQa6Y3nMw)\n"
                "- [Steve Eisman, Prof G Markets interview](https://www.youtube.com/watch?v=PJrq_bw7bPc)")


ABBREVIATIONS = {
    "ALFRED": "Archival Federal Reserve Economic Data", "BEA": "Bureau of Economic Analysis",
    "BLS": "Bureau of Labor Statistics", "BTOS": "Business Trends and Outlook Survey",
    "CFO": "Cash Flow from Operations", "EIA": "U.S. Energy Information Administration",
    "FCF": "Free Cash Flow", "FRED": "Federal Reserve Economic Data",
    "HY": "High Yield", "OAS": "Option-Adjusted Spread", "SEC": "U.S. Securities and Exchange Commission",
    "TTM": "Trailing Twelve Months", "YoY": "Year over Year",
    "2s10s": "10-year Treasury yield minus 2-year Treasury yield",
}


def methodology(st) -> None:
    page_intro(st, "Definitions & Methodology", "Auditable Phase 1 fixture definitions; live methods remain unimplemented")
    st.subheader("Abbreviations")
    st.table([{"Abbreviation": key, "Meaning": value} for key, value in ABBREVIATIONS.items()])
    st.subheader("Metric registry")
    st.caption("Dashboard disclosures and this page use the same canonical metric registry. "
               "No live collectors or paid services are connected.")
    inventory = formula_inventory()
    registry = metric_registry()
    for panel in PANELS:
        with st.expander(f"{panel.id} — {panel.name}"):
            for item in inventory.values():
                if item["panel_id"] == panel.id:
                    row = registry[item["formula_id"]]
                    kind = "formula: " + (row["formula"] or "raw metric")
                    st.write(f"**{row['name']} ({row['metric_id']})** — {row['definition']} "
                             f"Unit: {row['unit']}; {kind}; source: {'; '.join(row['source_priority'])}; "
                             f"cadence: {row['cadence']}.")
            st.write(f"Panel proxies: {', '.join(panel.tickers)}. Market confirmation, not causal proof.")
            if panel.metric.source_url:
                st.write(f"Source/API directory: {panel.metric.source_url}")
    st.subheader("Policy and limitations")
    st.write("All dashboard values are synthetic local fixtures. Source cost/auth: no service connected; "
             "free public sources are planned and paid services require owner approval. "
             "Update cadence is proposed per fixture, not an active schedule.")
    st.write("Revision/vintage policy: revisable macro values must retain then-known observations in a later phase. "
             "No historical replay or live revision handling exists here. Interpretations are scenario copy, not "
             "rule-generated conclusions; future rules must be grounded in observed deltas and preserve contradictions.")
    st.write("Formula version: frozen PRD v0.91 definitions; implementation mapping and change history are TBD. "
             "Change log: Phase 1 added a fixture display only; no calculation methodology changed.")
