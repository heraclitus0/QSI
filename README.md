<p align="center">
  <img src="QSI_logo.png" alt="QSI Logo" width="120"/>
</p>

<h1 align="center">Quantitative Stochastic Intelligence</h1>

<p align="center">
  Adaptive rupture detection and epistemic diagnostics for dynamic systems.<br/>
  <b>Policy-calibrated intelligence that learns from volatility.</b>
</p>

---

## Overview

**QSI** (Quantitative Stochastic Intelligence) is a lightweight intelligence engine for analyzing forecast–actual systems under uncertainty.  
It detects ruptures (large misalignments), estimates preventable losses, and provides epistemic diagnostics on stability, volatility, and systemic resilience.

QSI is agnostic: it can be deployed anywhere drift matters — from **supply chains** to **finance**, **pharma**, **cybersecurity**, or **infrastructure**.

---

## Features

- **Detection Engine**
  - Native drift–threshold logic with memory (`Θ`, `E`).
  - EWMA adaptive thresholds.
  - Enterprise plug-ins: register custom θ models.
- **Cognize Integration (optional)**
  - Policy meta-manager (`ε`-greedy, shadow evaluation, safe promotion).
  - Graph-coupled agents for multi-segment interaction.
- **Epistemic Diagnostics**
  - Scope stability score.
  - Population Stability Index (PSI).
  - ETA to persistent breach.
  - Pareto loss concentration.
  - Weekend vs weekday dynamics.
- **Streamlit App**
  - Upload data (`Date, Forecast, Actual, Unit_Cost`).
  - Interactive toggles for detection model, policies, diagnostics.
  - Instant KPIs + visualization.

---

## Installation

```bash
git clone https://github.com/your-org/QSI.git
cd QSI
pip install -r requirements.txt
```

Run the interactive app:

```bash
streamlit run app.py
```

---

## Quick Start

```python
from qsi import QSIEngine, QSIConfig, generate_dummy

# Generate sample dataset
df = generate_dummy(days=60)

# Configure engine
cfg = QSIConfig(use_ewma=True, ewma_alpha=0.3, ewma_k=3.0)

# Analyze
engine = QSIEngine(cfg)
df_out, report = engine.analyze(df)

print(report["summary"])
```

---

## Use Cases

QSI is **domain-agnostic**. Any system with forecasts, expectations, or baselines can use it:

- **Supply Chain & Procurement**  
  Detect yield drifts, quantify preventable losses, stress-test contracts.

- **Finance & Risk**  
  Monitor volatility, detect abnormal deviations, quantify exposure.

- **Pharma & Healthcare**  
  Track demand–supply misalignments, prevent stockouts, stabilize trials.

- **Cybersecurity**  
  Detect anomalies in traffic, breach probabilities, stability under attack.

- **Infrastructure & Energy**  
  Forecast vs actual load monitoring, prevent cascading failures.

---

## Outputs

- **KPI Strip**: total preventable loss, rupture count, mean drift, scope score, PSI.  
- **Visualization**: drift vs threshold, rupture markers, volatility bands, segment heatmaps.  
- **Diagnostics**: JSON report (economics + epistemic alignment).  

---

## Repo Structure

```
QSI/
│── datasets/         # sample CSVs
│── qsi/              # engine + epistemic modules
│── tests/            # test scripts
│── app.py            # Streamlit dashboard
│── README.md         # executive overview
│── USER_GUIDE.md     # step-by-step usage
│── requirements.txt
│── QSI_logo.png
```

---

## License

Apache 2.0 — free for research and commercial use with attribution.

---

<p align="center">
  <i>QSI — from volatility to intelligence.</i>
</p>
