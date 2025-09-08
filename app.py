import json
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image

from qsi import QSIEngine, QSIConfig, generate_dummy
from qsi import EpistemicAnalytics, EpistemicConfig


# ---------------- Page & Header ----------------
st.set_page_config(page_title="QSI", layout="wide")


st.markdown(
    """
    <style>
      .block-container { padding: 2rem 3rem; }
      .kpi-card { background: #0e0e0e; padding: 16px 18px; border-radius: 12px; border: 1px solid #1f1f1f; }
      .kpi-label { color: #9aa0a6; font-size: 12px; letter-spacing: .02em; }
      .kpi-value { color: #ffffff; font-size: 28px; font-weight: 600; margin-top: 4px; }
      .section-divider { border-top: 1px solid #1f1f1f; margin: 18px 0 10px 0; }
    </style>
    """,
    unsafe_allow_html=True,
)


logo_path = Path("QSI_logo.png")
if logo_path.exists():
    col_h1, col_h2, col_h3 = st.columns([1, 2, 1])
    with col_h2:
        st.image(Image.open(str(logo_path)), width=100)
        st.markdown(
            '<div style="text-align:center; color:#aaaaaa; font-size:16px; margin-top:6px;">'
            'Quantitative Stochastic Intelligence'
            '</div>',
            unsafe_allow_html=True,
        )
else:
    # Fallback if logo missing
    st.title("QSI")
    st.caption("Quantitative Stochastic Intelligence")


# ---------------- Data Ingest ----------------
u_col1, u_col2 = st.columns([4, 1])
with u_col1:
    uploaded = st.file_uploader(
        "Upload CSV  •  columns required: Date, Forecast, Actual, Unit_Cost",
        type=["csv"],
        help="UTF-8 CSV with header row. Date will be parsed to timestamp.",
    )
with u_col2:
    use_sample = st.toggle("Use sample data", value=(uploaded is None), help="Generate a small demo dataset.")

if uploaded is not None:
    df = pd.read_csv(uploaded, parse_dates=["Date"])
elif use_sample:
    df = (
        generate_dummy(days=60, segments=["SKU-A", "SKU-B"])
        .rename(columns={"Segment": "SKU"})
    )
else:
    st.stop()


candidate_segments = [c for c in df.columns if c not in ("Date", "Forecast", "Actual", "Unit_Cost")]
segment_col = st.selectbox("Segment (optional)", ["None"] + candidate_segments, index=0)
groupby = None if segment_col == "None" else segment_col


# ---------------- Configuration ----------------
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


# ---------------- Run Engine ----------------
df_out, report = engine.analyze(df, groupby=groupby)
diag = EpistemicAnalytics.enrich(df_out, EpistemicConfig(baseline_window=28, expiry_k=3))


# ---------------- KPI Strip ----------------
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
k1, k2, k3, k4, k5 = st.columns([1.2, 1, 1, 1, 1])

def kpi(col, label, value):
    with col:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-label">{label}</div>'
            f'<div class="kpi-value">{value}</div></div>',
            unsafe_allow_html=True,
        )

kpi(k1, "Total Loss", f"{report['summary']['total_loss']:.2f}")
kpi(k2, "Ruptures", f"{report['summary']['ruptures']}")
kpi(k3, "Mean Drift", f"{report['summary']['mean_drift']:.2f}")
kpi(k4, "Scope Score", f"{diag['epistemic']['scope_score_0to1']:.2f}")
kpi(k5, "PSI", f"{diag['epistemic']['psi']:.3f}")


# ---------------- Charts ----------------
def _rolling_band(y: pd.Series, window: int = 7) -> pd.DataFrame:
    """Return rolling mean and std; robust to short series."""
    s = y.astype(float)
    m = s.rolling(window=window, min_periods=max(2, window // 2)).mean()
    std = s.rolling(window=window, min_periods=max(2, window // 2)).std(ddof=0)
    return pd.DataFrame({"mean": m, "lo": m - std, "hi": m + std})

def fig_drift_vs_theta(frame: pd.DataFrame, date_col="Date") -> go.Figure:
    band = _rolling_band(frame["drift"], window=7)

    fig = go.Figure()

    # Volatility band (±1σ around rolling mean)
    fig.add_traces([
        go.Scatter(
            x=frame[date_col], y=band["hi"], line=dict(width=0), showlegend=False, hoverinfo="skip"
        ),
        go.Scatter(
            x=frame[date_col], y=band["lo"],
            fill="tonexty", fillcolor="rgba(100,100,255,0.08)",
            line=dict(width=0), showlegend=False, hoverinfo="skip"
        ),
    ])

    # Drift & Threshold
    fig.add_trace(go.Scatter(x=frame[date_col], y=frame["drift"], mode="lines", name="Drift"))
    fig.add_trace(go.Scatter(x=frame[date_col], y=frame["Theta"], mode="lines", name="Threshold"))

    # Rupture markers
    r = frame[frame["rupture"]]
    if not r.empty:
        fig.add_trace(
            go.Scatter(
                x=r[date_col], y=r["drift"],
                mode="markers", name="Rupture",
                marker=dict(size=8, symbol="x")
            )
        )

    fig.update_layout(
        margin=dict(l=0, r=0, t=8, b=0),
        legend=dict(orientation="h", x=0, y=1.08),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)")
    )
    return fig

def fig_segment_heatmap(frame: pd.DataFrame, seg_col: str, date_col="Date"):
    if not seg_col or seg_col not in frame.columns:
        return None
    pivot = frame.pivot_table(index=seg_col, columns=date_col, values="rupture_prob", aggfunc="mean").sort_index()
    if pivot.empty:
        return None
    fig = px.imshow(
        pivot.values, x=pivot.columns, y=pivot.index,
        aspect="auto", labels=dict(color="Rupture probability"),
    )
    fig.update_layout(margin=dict(l=0, r=0, t=8, b=0))
    return fig

st.plotly_chart(fig_drift_vs_theta(df_out), use_container_width=True)
hm = fig_segment_heatmap(df_out, groupby)
if hm is not None:
    st.plotly_chart(hm, use_container_width=True)


# ---------------- Details ----------------
with st.expander("Events", expanded=False):
    st.dataframe(report["events"], use_container_width=True)

with st.expander("Economics", expanded=False):
    st.json(diag["economics"], expanded=False)

with st.expander("Epistemic", expanded=False):
    st.json(diag["epistemic"], expanded=False)

# Optional Cognize graph telemetry
if "graph" in report:
    with st.expander("Graph telemetry", expanded=False):
        st.json(report["graph"], expanded=False)


# ---------------- Data Preview ----------------
st.subheader("Data Preview")
st.dataframe(df_out.head(30), use_container_width=True)


# ---------------- Downloads ----------------
with st.expander("Download"):
    # CSV results
    st.download_button(
        "Results CSV",
        data=df_out.to_csv(index=False).encode(),
        file_name="qsi_results.csv",
        mime="text/csv",
    )

    # JSON report (stable)
    export_report = {
        "summary": report["summary"],
        "events": report["events"].to_dict(orient="records"),
        "economics": diag["economics"],
        "epistemic": diag["epistemic"],
    }
    if "by_segment" in report:
        export_report["by_segment"] = report["by_segment"]

    st.download_button(
        "Report JSON",
        data=json.dumps(export_report, default=str, indent=2).encode(),
        file_name="qsi_report.json",
        mime="application/json",
    )



