"""Streamlit entrypoint: run with `streamlit run app.py`."""

import streamlit as st

from monitor.ui import DISCLAIMER


st.set_page_config(page_title="AI / Macro Thesis Monitor", page_icon="📊", layout="wide")
st.sidebar.caption("Phase 1 • local fixtures only")
st.sidebar.info(DISCLAIMER)
navigation = st.navigation([
    st.Page("pages/dashboard.py", title="Dashboard", default=True),
    st.Page("pages/evidence.py", title="Evidence"),
    st.Page("pages/about.py", title="About"),
    st.Page("pages/methodology.py", title="Definitions & Methodology"),
])
navigation.run()
