import streamlit as st
import pandas as pd
import json

from qsi import QSIEngine, QSIConfig, generate_dummy
from qsi import EpistemicAnalytics, EpistemicConfig

# ---------------- HEADER ----------------
st.set_page_config(page_title="QSI", layout="wide")
st.title("QSI")
st.caption("Quantitative Stochastic Intelligence (optional: show full form here)")

# ---------------- DATA INPUT ----------------
uploaded = st.file_uploader("Upload CSV (Date, Forecast, Actual, Unit_Cost)", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded, parse_dates=["Date"])
else:
    st.info("Using dummy dataset — upload your own to replace.")
    df = generate_dummy(days=60, segments=["SKU-A","SKU-B"]).rename(columns={"Segment":"SKU"})

# Detect possible segment columns
candidates = [c for c in df.columns if c not in ("Date", "Forecast", "Actual", "Unit_Cost")]
segment_col = st.selectbox("Optional segment column", ["(none)"] + candidates)
groupby = None if segment_col == "(none)" else segment_col

# ---------------- CONFIG ----------------
with st.expander("Configuration", expanded=False):
    col1, col2 = st.columns(2)

    with col1:
        use_ewma = st.checkbox("Use EWMA threshold", value=True)
        base = st.number_input("Base Θ", 0.0, 10000.0, 120.0, 10.0)
        a = st.number_input("Θ sensitivity (a)", 0.0, 10.0, 0.02, 0.01)
        cval = st.number_input("Memory accumulation (c)", 0.0, 10.0, 0.25, 0.01)
        sigma = st.number_input("Noise on Θ (σ)", 0.0, 100.0, 5.0, 0.5)

    with col2:
        alpha = st.slider("EWMA α", 0.01, 0.9, 0.25, 0.01)
        kval = st.slider("EWMA k", 0.5, 6.0, 3.0, 0.1)
        use_graph = st.checkbox("Couple segments (graph mode)", value=bool(groupby))

cfg = QSIConfig(
    col_segment=groupby,
    base_threshold=base, a=a, c=cval, sigma=sigma,
    use_ewma=use_ewma, ewma_alpha=alpha, ewma_k=kval,
    use_cognize=True, use_graph=use_graph
)
engine = QSIEngine(cfg)

# ---------------- RUN ANALYSIS ----------------
df_out, report = engine.analyze(df, groupby=groupby)
diag = EpistemicAnalytics.enrich(df_out, EpistemicConfig(baseline_window=28, expiry_k=3))

# ---------------- DASHBOARD ----------------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)
col1.metric("Total Loss", f"{report['summary']['total_loss']:.2f}")
col2.metric("Ruptures", report['summary']['ruptures'])
col3.metric("Mean Drift", f"{report['summary']['mean_drift']:.2f}")

col4, col5 = st.columns(2)
col4.metric("Scope Score", f"{diag['epistemic']['scope_score_0to1']:.2f}")
col5.metric("PSI", f"{diag['epistemic']['psi']:.3f}")

st.write("---")

# ---------------- DETAILED VIEWS ----------------
with st.expander("Events (ruptures)", expanded=False):
    st.dataframe(report["events"], use_container_width=True)

with st.expander("Economics breakdown", expanded=False):
    st.json(diag["economics"], expanded=False)

with st.expander("Epistemic diagnostics", expanded=False):
    st.json(diag["epistemic"], expanded=False)

# ---------------- OUTPUT ----------------
st.subheader("Data Preview")
st.dataframe(df_out.head(20), use_container_width=True)

# ---------------- DOWNLOADS ----------------
with st.expander("Download Results"):
    st.download_button("CSV: Full Run", df_out.to_csv(index=False).encode(), "qsi_run.csv")
    rep_json = {
        "summary": report["summary"],
        "events": report["events"].to_dict(orient="records"),
        "economics": diag["economics"],
        "epistemic": diag["epistemic"],
    }
    st.download_button("JSON: Report", json.dumps(rep_json, indent=2).encode(), "qsi_report.json")

