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
st.markdown("""
<style>
  .block-container { padding: 2rem 3rem; }
  .kpi-card { background:#0e0e0e; padding:16px 18px; border-radius:12px; border:1px solid #1f1f1f; }
  .kpi-label { color:#9aa0a6; font-size:12px; letter-spacing:.02em; }
  .kpi-value { color:#ffffff; font-size:28px; font-weight:600; margin-top:4px; }
  .section-divider { border-top:1px solid #1f1f1f; margin:18px 0 10px 0; }
</style>
""", unsafe_allow_html=True)

# Brand
logo_path = Path("QSI_logo.png")
c_logo, _ = st.columns([0.08, 0.92])
with c_logo:
    if logo_path.exists():
        st.image(Image.open(str(logo_path)), width=54)
    else:
        st.markdown("<div style='padding:4px 0 8px 0; font-weight:600;'>QSI</div>", unsafe_allow_html=True)


# ---------------- Data Ingest ----------------
u_col1, u_col2 = st.columns([4, 1])
with u_col1:
    uploaded = st.file_uploader(
        "Upload CSV  •  required columns: Date, Forecast, Actual, Unit_Cost",
        type=["csv"],
        help="UTF-8 CSV with header row. Date will be parsed to timestamp.",
    )
with u_col2:
    use_sample = st.toggle("Use sample data", value=(uploaded is None), help="Generate a demo dataset.")

if uploaded is not None:
    df = pd.read_csv(uploaded, parse_dates=["Date"])
elif use_sample:
    df = generate_dummy(days=60, segments=["SKU-A", "SKU-B"]).rename(columns={"Segment": "SKU"})
else:
    st.stop()

# Optional segment column
candidate_segments = [c for c in df.columns if c not in ("Date", "Forecast", "Actual", "Unit_Cost")]
segment_col = st.selectbox("Segment (optional)", ["None"] + candidate_segments, index=0)
groupby = None if segment_col == "None" else segment_col

# Optional boolean columns for policy
bool_cols = [c for c in df.columns if df[c].dropna().map(lambda x: isinstance(x, (bool, np.bool_))).all()]
policy_col = st.selectbox("Policy flag (optional boolean column)", ["None"] + bool_cols, index=0)
policy_col = None if policy_col == "None" else policy_col


# ---------------- Configuration ----------------
with st.expander("Detection Model • QSI engine", expanded=False):
    c1, c2, c3 = st.columns(3)

    # Native / EWMA
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

with st.expander("Cognize meta-policy (optional, runtime)", expanded=False):
    c4, c5, c6, c7 = st.columns(4)
    with c4:
        use_cognize = st.checkbox("Enable Cognize", value=True, help="Turn off to run native threshold engine.")
    with c5:
        epsilon = st.slider("ε (exploration)", 0.0, 0.5, 0.10, 0.01, help="Higher = explore more candidate policies.")
    with c6:
        promote_margin = st.slider("Promote margin", 1.00, 1.10, 1.02, 0.01, help="How much better a candidate must be.")
    with c7:
        cooldown_steps = st.number_input("Cooldown steps", min_value=1, value=20, step=1)

cfg = QSIConfig(
    col_segment=groupby,
    base_threshold=base, a=a, c=cval, sigma=sigma, seed=int(seed),
    use_ewma=use_ewma, ewma_alpha=alpha, ewma_k=kval,
    use_cognize=use_cognize, use_graph=use_graph,
    epsilon=epsilon, promote_margin=promote_margin, cooldown_steps=int(cooldown_steps),
)
engine = QSIEngine(cfg)

# ---------------- Epistemic Diagnostics Config ----------------
with st.expander("Epistemic diagnostics (scope • PSI • ETA)", expanded=False):
    d1, d2, d3 = st.columns(3)
    with d1:
        baseline_window = st.number_input("Baseline window (days)", min_value=5, value=28, step=1)
        recent_window = st.number_input("Recent window (days, 0=same as baseline)", min_value=0, value=0, step=1)
        recent_window = None if recent_window == 0 else int(recent_window)
    with d2:
        scope_lo = st.slider("Scope quantile low", 0.0, 0.20, 0.05, 0.01)
        scope_hi = st.slider("Scope quantile high", 0.80, 1.0, 0.95, 0.01)
        psi_bins = st.slider("PSI bins", 4, 30, 10, 1)
    with d3:
        on_target_pct = st.slider("On-target tolerance (%)", 0.0, 0.20, 0.05, 0.01)
        severe_pct = st.slider("Severe threshold (%)", 0.10, 0.60, 0.20, 0.01)
        expiry_k = st.number_input("ETA: consecutive breaches (k)", min_value=1, value=3, step=1)
        expiry_lookback = st.number_input("ETA: lookback window", min_value=7, value=28, step=1)

epi_cfg = EpistemicConfig(
    baseline_mode="window",
    baseline_window=int(baseline_window),
    scope_q_lo=float(scope_lo), scope_q_hi=float(scope_hi),
    psi_bins=int(psi_bins),
    recent_window=recent_window,
    on_target_pct=float(on_target_pct),
    severe_pct=float(severe_pct),
    expiry_k=int(expiry_k),
    expiry_lookback=int(expiry_lookback),
    groupby=groupby,
    policy_col=policy_col,
)

# ---------------- Run Engine ----------------
df_out, report = engine.analyze(df, groupby=groupby)
diag = EpistemicAnalytics.enrich(df_out, epi_cfg)

# ---------------- KPI Strip ----------------
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
k1, k2, k3, k4, k5 = st.columns([1.2, 1, 1, 1, 1])

def kpi(col, label, value_text):
    with col:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-label">{label}</div>'
            f'<div class="kpi-value">{value_text}</div></div>',
            unsafe_allow_html=True,
        )

kpi(k1, "Total Loss", f"{report['summary']['total_loss']:.2f}")
kpi(k2, "Ruptures", f"{report['summary']['ruptures']:.0f}")
kpi(k3, "Mean Drift", f"{report['summary']['mean_drift']:.2f}")
kpi(k4, "Scope Score", f"{diag['epistemic']['scope_score_0to1']:.2f}")
kpi(k5, "PSI", f"{diag['epistemic']['psi']:.2f}")

# ---------------- Chart Controls ----------------
c_plot1, c_plot2, c_plot3 = st.columns([1.3, 1, 1])
with c_plot1:
    show_mean = st.checkbox("Show rolling mean", True)
with c_plot2:
    band_win = st.slider("Volatility band window (days)", 3, 21, 7, 1)
with c_plot3:
    ygrid = st.checkbox("Show y-grid", True)

# ---------------- Charts ----------------
def _rolling_band(y: pd.Series, window: int = 7) -> pd.DataFrame:
    s = y.astype(float)
    m = s.rolling(window=window, min_periods=max(2, window // 2)).mean()
    std = s.rolling(window=window, min_periods=max(2, window // 2)).std(ddof=0)
    return pd.DataFrame({"mean": m, "lo": m - std, "hi": m + std})

def fig_drift_vs_theta(frame: pd.DataFrame, date_col: str = "Date",
                       show_mean_line: bool = True, band_window: int = 7) -> go.Figure:
    # Palette tuned for dark theme
    CLR_BAND  = "rgba(255,255,255,0.06)"   # volatility fill
    CLR_DRIFT = "rgba(220,220,220,1.00)"   # primary neutral (brighter, 2px)
    CLR_THETA = "rgba(160,160,160,0.95)"   # muted reference
    CLR_MEAN  = "rgba(200,200,200,0.55)"   # thin mean (optional)
    CLR_RUPT  = "rgba(232,73,73,1.00)"     # only red (ruptures)

    band = _rolling_band(frame["drift"], window=int(band_window))
    fig = go.Figure()

    # Volatility band (±1σ)
    fig.add_trace(go.Scatter(
        x=frame[date_col], y=band["hi"], line=dict(width=0),
        showlegend=False, hoverinfo="skip"
    ))
    fig.add_trace(go.Scatter(
        x=frame[date_col], y=band["lo"],
        fill="tonexty", fillcolor=CLR_BAND,
        line=dict(width=0), showlegend=False, hoverinfo="skip",
        name="Volatility"
    ))

    # Drift (primary)
    fig.add_trace(go.Scatter(
        x=frame[date_col], y=frame["drift"],
        mode="lines", name="Drift",
        line=dict(width=2, color=CLR_DRIFT)
    ))

    # Threshold (reference)
    fig.add_trace(go.Scatter(
        x=frame[date_col], y=frame["Theta"],
        mode="lines", name="Threshold",
        line=dict(width=1.5, color=CLR_THETA)
    ))

    # Rolling mean (optional)
    if show_mean_line:
        fig.add_trace(go.Scatter(
            x=frame[date_col], y=band["mean"],
            mode="lines", name="Mean",
            line=dict(width=1, color=CLR_MEAN, dash="dot")
        ))

    # Rupture markers (semantic red)
    rupt = frame[frame["rupture"]]
    if not rupt.empty:
        fig.add_trace(go.Scatter(
            x=rupt[date_col], y=rupt["drift"],
            mode="markers", name="Rupture",
            marker=dict(size=7, symbol="x", color=CLR_RUPT)
        ))

    fig.update_layout(
        margin=dict(l=0, r=0, t=6, b=0),
        legend=dict(orientation="h", x=0, y=1.08),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=ygrid, gridcolor="rgba(255,255,255,0.06)")
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

st.plotly_chart(fig_drift_vs_theta(df_out, show_mean_line=show_mean, band_window=band_win),
                use_container_width=True)
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

# Optional: deeper diagnostics / policy breakdown / group stats
if "diagnostics" in diag:
    with st.expander("Diagnostics", expanded=False):
        st.json(diag["diagnostics"], expanded=False)
if "by_group" in diag:
    with st.expander("By segment", expanded=False):
        st.json(diag["by_group"], expanded=False)
if "policy_breakdown" in diag:
    with st.expander("Policy vs Non-policy", expanded=False):
        st.json(diag["policy_breakdown"], expanded=False)

# Optional Cognize graph telemetry
if "graph" in report:
    with st.expander("Graph telemetry", expanded=False):
        st.json(report["graph"], expanded=False)

# ---------------- Data Preview ----------------
with st.expander("Data Preview", expanded=False):
    st.dataframe(df_out.head(30), use_container_width=True)

# ---------------- Downloads ----------------
with st.expander("Download"):
    st.download_button(
        "Results CSV",
        data=df_out.to_csv(index=False).encode(),
        file_name="qsi_results.csv",
        mime="text/csv",
    )

    export_report = {
        "summary": report["summary"],
        "events": report["events"].to_dict(orient="records"),
        "economics": diag.get("economics", {}),
        "epistemic": diag.get("epistemic", {}),
        "diagnostics": diag.get("diagnostics", {}),
    }
    if "by_segment" in report:
        export_report["by_segment"] = report["by_segment"]
    if "by_group" in diag:
        export_report["by_group"] = diag["by_group"]
    if "policy_breakdown" in diag:
        export_report["policy_breakdown"] = diag["policy_breakdown"]

    st.download_button(
        "Report JSON",
        data=json.dumps(export_report, default=str, indent=2).encode(),
        file_name="qsi_report.json",
        mime="application/json",
    )
