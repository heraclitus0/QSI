import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

from qsi import QSIEngine, QSIConfig, generate_dummy
from qsi import EpistemicAnalytics, EpistemicConfig


# ---------- Page ----------
st.set_page_config(page_title="QSI", layout="wide")
st.title("QSI")
st.caption("Quantitative Stochastic Intelligence")

# ---------- Data ----------
with st.container():
    col_u1, col_u2 = st.columns([3, 1], gap="large")
    with col_u1:
        uploaded = st.file_uploader(
            "Upload CSV  •  required columns: Date, Forecast, Actual, Unit_Cost",
            type=["csv"],
            help="UTF-8 CSV with a header row. Date will be parsed to timestamp."
        )
    with col_u2:
        use_sample = st.toggle("Use sample data", value=(uploaded is None))

if uploaded is not None:
    df = pd.read_csv(uploaded, parse_dates=["Date"])
elif use_sample:
    df = generate_dummy(days=60, segments=["SKU-A", "SKU-B"]).rename(columns={"Segment": "SKU"})
else:
    st.stop()

# Suggested segment columns
candidate_segments = [c for c in df.columns if c not in ("Date", "Forecast", "Actual", "Unit_Cost")]
segment_col = st.selectbox("Segment (optional)", ["None"] + candidate_segments, index=0)
groupby = None if segment_col == "None" else segment_col

# ---------- Configuration ----------
with st.expander("Configuration", expanded=False):
    c1, c2, c3 = st.columns(3)
    with c1:
        base = st.number_input("Base Θ", min_value=0.0, value=120.0, step=10.0)
        a = st.number_input("Θ sensitivity (a)", min_value=0.0, value=0.02, step=0.01, format="%.2f")
        cval = st.number_input("Memory accumulation (c)", min_value=0.0, value=0.25, step=0.01, format="%.2f")
        sigma = st.number_input("Noise σ", min_value=0.0, value=5.0, step=0.5)
    with c2:
        use_ewma = st.checkbox("Use EWMA threshold", value=True)
        alpha = st.slider("EWMA α", 0.01, 0.9, 0.25, 0.01)
        kval = st.slider("EWMA k", 0.5, 6.0, 3.0, 0.1)
    with c3:
        use_graph = st.checkbox("Couple segments (graph mode)", value=bool(groupby))
        seed = st.number_input("Seed", min_value=0, value=123, step=1)

cfg = QSIConfig(
    col_segment=groupby,
    base_threshold=base, a=a, c=cval, sigma=sigma, seed=int(seed),
    use_ewma=use_ewma, ewma_alpha=alpha, ewma_k=kval,
    use_cognize=True, use_graph=use_graph
)
engine = QSIEngine(cfg)

# ---------- Run ----------
df_out, report = engine.analyze(df, groupby=groupby)
diag = EpistemicAnalytics.enrich(df_out, EpistemicConfig(baseline_window=28, expiry_k=3))

# ---------- KPI Strip ----------
st.markdown("---")
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Loss", f"{report['summary']['total_loss']:.2f}")
k2.metric("Ruptures", report["summary"]["ruptures"])
k3.metric("Mean Drift", f"{report['summary']['mean_drift']:.2f}")
k4.metric("Scope Score", f"{diag['epistemic']['scope_score_0to1']:.2f}")
k5.metric("PSI", f"{diag['epistemic']['psi']:.3f}")

# ---------- Charts ----------
def fig_drift_vs_theta(frame: pd.DataFrame, date_col="Date"):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=frame[date_col], y=frame["drift"], mode="lines", name="Drift"))
    fig.add_trace(go.Scatter(x=frame[date_col], y=frame["Theta"], mode="lines", name="Threshold"))
    r = frame[frame["rupture"]]
    if not r.empty:
        fig.add_trace(go.Scatter(x=r[date_col], y=r["drift"], mode="markers", name="Rupture",
                                 marker=dict(size=8, symbol="x")))
    fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), legend=dict(orientation="h", x=0, y=1.05))
    return fig

def fig_segment_heatmap(frame: pd.DataFrame, seg_col: str, date_col="Date"):
    if not seg_col or seg_col not in frame.columns:
        return None
    pivot = frame.pivot_table(index=seg_col, columns=date_col, values="rupture_prob", aggfunc="mean").sort_index()
    fig = px.imshow(pivot.values, x=pivot.columns, y=pivot.index, aspect="auto",
                    labels=dict(color="Rupture probability"))
    fig.update_layout(margin=dict(l=0, r=0, t=10, b=0))
    return fig

st.plotly_chart(fig_drift_vs_theta(df_out), use_container_width=True)
hm = fig_segment_heatmap(df_out, groupby)
if hm is not None:
    st.plotly_chart(hm, use_container_width=True)

# ---------- Details ----------
with st.expander("Events"):
    st.dataframe(report["events"], use_container_width=True)

with st.expander("Economics"):
    st.json(diag["economics"], expanded=False)

with st.expander("Epistemic"):
    st.json(diag["epistemic"], expanded=False)

# ---------- Data Preview ----------
st.subheader("Data Preview")
st.dataframe(df_out.head(30), use_container_width=True)

# ---------- Downloads ----------
with st.expander("Download"):
    # CSV
    st.download_button(
        "Results CSV",
        data=df_out.to_csv(index=False).encode(),
        file_name="qsi_results.csv",
        mime="text/csv",
    )
    # JSON report (stable serialization)
    full_report = {
        "summary": report["summary"],
        "events": report["events"].to_dict(orient="records"),
        "economics": diag["economics"],
        "epistemic": diag["epistemic"],
        **({"by_segment": report.get("by_segment")} if "by_segment" in report else {})
    }
    st.download_button(
        "Report JSON",
        data=json.dumps(full_report, default=str, indent=2).encode(),
        file_name="qsi_report.json",
        mime="application/json",
    )

# ---------- Optional: Graph telemetry (only if provided by engine) ----------
if "graph" in report:
    with st.expander("Graph telemetry"):
        st.json(report["graph"], expanded=False)

