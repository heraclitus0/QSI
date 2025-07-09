import streamlit as st
import pandas as pd
import plotly.express as px
from rupture import generate_dummy, compute_drift_thresholds, compute_ewma_threshold

# --- Config ---
st.set_page_config(page_title="Rupture Detector", layout="wide")

# --- Sidebar Inputs ---
st.sidebar.title("Configuration")
upload = st.sidebar.file_uploader("Upload data (CSV or Excel)", type=["csv", "xls", "xlsx"])

use_dummy = st.sidebar.checkbox("Use dummy data", value=not upload)
days = st.sidebar.slider("Days (dummy)", 7, 90, 30)

st.sidebar.markdown("---")
st.sidebar.subheader("Drift Detection Settings")
c = st.sidebar.slider("Drift scaling factor", 0.0, 1.0, 0.05, 0.01)
a = st.sidebar.slider("Rupture sensitivity", 0.0, 1.0, 0.1, 0.01)
base_threshold = st.sidebar.number_input("Base threshold", 0, 500, 100)
sigma = st.sidebar.number_input("Noise estimate", 0, 200, 30)

st.sidebar.markdown("---")
st.sidebar.subheader("EWMA Smoothing")
alpha = st.sidebar.slider("Alpha", 0.01, 0.5, 0.2)
k = st.sidebar.slider("Sigma multiplier", 1, 5, 3)

# --- Load & Validate Data ---
if use_dummy:
    df = generate_dummy(days=days)
else:
    try:
        ext = upload.name.split('.')[-1]
        if ext == "csv":
            df = pd.read_csv(upload, parse_dates=["Date"])
        else:
            df = pd.read_excel(upload, parse_dates=["Date"])
        required_cols = {"Date", "Forecast", "Actual", "Unit_Cost"}
        if not required_cols.issubset(df.columns):
            st.error(f"Missing columns. Required: {required_cols}")
            st.stop()
    except Exception as e:
        st.error("Error reading file. Ensure proper format and date column.")
        st.stop()

# --- Drift Detection Computation ---
df_drift, ruptures, total_loss = compute_drift_thresholds(df, c, a, base_threshold, sigma, seed=42)
df_final = compute_ewma_threshold(df_drift, alpha=alpha, k=k)

# --- Header ---
st.title("Rupture Detector")
st.markdown("Detect where forecast vs. actual data diverges and money is lost.")

# --- Plotly Chart ---
fig = px.line(df_final, x="Date", y=["Delta", "Threshold_EWMA"], labels={"value": "Value", "variable": "Metric"})
fig.add_scatter(x=ruptures["Date"], y=ruptures["Delta"], mode="markers",
                marker=dict(color="red", size=8), name="Rupture")
fig.update_layout(title="Forecast Drift vs Adaptive Threshold", xaxis_title="Date", yaxis_title="Units")

st.plotly_chart(fig, use_container_width=True)

# --- Results Summary ---
st.subheader("Summary")
st.write(f"**Total preventable loss:** ₹{int(total_loss):,}")

st.subheader("Rupture Events")
if ruptures.empty:
    st.info("No ruptures detected – system is well-aligned.")
else:
    st.dataframe(
        ruptures[["Date", "Delta", "Threshold", "Loss"]].assign(
            Date=ruptures["Date"].dt.strftime("%Y-%m-%d"),
            Loss=ruptures["Loss"].map(lambda x: f"₹{x:,.0f}")
        ),
        use_container_width=True
    )

# --- Download ---
st.download_button(
    label="Download Rupture Report (CSV)",
    data=df_final.to_csv(index=False),
    file_name="rupture_log.csv",
    mime="text/csv"
)
