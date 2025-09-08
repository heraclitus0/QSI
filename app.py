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

from pathlib import Path
from PIL import Image

st.markdown(
    """
    <style>
      .block-container { padding: 2rem 3rem; }
      .brand-pad { padding: 4px 0 8px 0; }
    </style>
    """,
    unsafe_allow_html=True,
)

logo_path = Path("QSI_logo.png")
col_logo, col_spacer = st.columns([0.08, 0.92])
with col_logo:
    if logo_path.exists():
        st.image(Image.open(str(logo_path)), width=54)
    else:
        st.markdown('<div class="brand-pad"><strong>QSI</strong></div>', unsafe_allow_html=True)


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
    s = y.astype(float)
    m = s.rolling(window=window, min_periods=max(2, window // 2)).mean()
    std = s.rolling(window=window, min_periods=max(2, window // 2)).std(ddof=0)
    return pd.DataFrame({"mean": m, "lo": m - std, "hi": m + std})

def fig_drift_vs_theta(frame: pd.DataFrame, date_col: str = "Date", show_mean: bool = True) -> go.Figure:
    # Palette (dark theme)
    clr_band   = "rgba(255,255,255,0.06)"     # volatility band fill
    clr_drift  = "rgba(235,235,235,1.0)"      # primary line (neutral)
    clr_theta  = "rgba(160,160,160,1.0)"      # threshold (muted grey)
    clr_mean   = "rgba(200,200,200,0.55)"     # rolling mean (thin)
    clr_rupt   = "rgba(232,73,73,1.0)"        # rupture markers (only red on chart)

    band = _rolling_band(frame["drift"], window=7)
    fig = go.Figure()

    # Volatility band (±1σ)
    fig.add_traces([
        go.Scatter(x=frame[date_col], y=band["hi"], line=dict(width=0), showlegend=False, hoverinfo="skip"),
        go.Scatter(
            x=frame[date_col], y=band["lo"],
            fill="tonexty", fillcolor=clr_band,
            line=dict(width=0), showlegend=False, hoverinfo="skip",
            name="Volatility band"
        ),
    ])

    # Drift (primary)
    fig.add_trace(go.Scatter(
        x=frame[date_col], y=frame["drift"],
        mode="lines", name="Drift",
        line=dict(width=2, color=clr_drift)
    ))

    # Threshold (reference)
    fig.add_trace(go.Scatter(
        x=frame[date_col], y=frame["Theta"],
        mode="lines", name="Threshold",
        line=dict(width=1.5, color=clr_theta)
    ))

    # Rolling mean (optional, thin)
    if show_mean:
        fig.add_trace(go.Scatter(
            x=frame[date_col], y=band["mean"],
            mode="lines", name="Mean",
            line=dict(width=1, color=clr_mean, dash="dot")
        ))

    # Rupture markers (red)
    r = frame[frame["rupture"]]
    if not r.empty:
        fig.add_trace(go.Scatter(
            x=r[date_col], y=r["drift"],
            mode="markers", name="Rupture",
            marker=dict(size=7, symbol="x", color=clr_rupt),
        ))

    fig.update_layout(
        margin=dict(l=0, r=0, t=6, b=0),
        legend=dict(orientation="h", x=0, y=1.08),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)")
    )
    return fig



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






