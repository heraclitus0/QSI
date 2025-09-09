# QSI User Guide

## Introduction
Quantitative Stochastic Intelligence (QSI) is a diagnostic system for detecting forecast drifts, rupture events, and hidden economic loss. This guide describes how to operate the QSI Streamlit application, interpret its outputs, and configure its advanced controls.

The guide is organized into:
1. Interface Overview
2. Configuration Controls
3. Analysis Outputs
4. Board-Level Diagnostics
5. Developer Mode
6. Use Cases

---

## 1. Interface Overview
The Streamlit application provides three panels:

- **Configuration Panel**: Interactive controls for selecting the analysis engine and adjusting thresholds, probabilities, and policies.  
- **Analysis Panel**: Visualization of drifts, thresholds, ruptures, and associated losses.  
- **Diagnostics Panel**: Board-level metrics including scope, stability indices, breach projections, and policy breakdowns.  

---

## 2. Configuration Controls

### Engine Selection
- **Native**: Baseline memory model using static thresholds.  
- **EWMA**: Thresholds adapt to volatility via Exponentially Weighted Moving Average.  
- **Cognize**: Advanced epistemic engine with policy management (requires Cognize library).  
- **Graph Mode**: Cognize extended to multiple segments, with coupling effects between them.  

**Guidance**:  
- Use *Native* for simple, stable series.  
- Use *EWMA* for noisy data requiring adaptive smoothing.  
- Use *Cognize* for complex, adaptive scenarios.  
- Use *Graph Mode* for multi-segment dependencies.  

### Threshold Parameters (Î)
- **Base Threshold**: Initial sensitivity to drift.  
- **a (Sensitivity)**: Degree to which accumulated memory raises the threshold.  
- **c (Memory Accumulation)**: Rate at which drift compounds in memory.  
- **Ï (Noise)**: Stochastic fluctuation applied to the threshold.  

**Interpretation**:  
Threshold determines when a deviation becomes a rupture. Lower thresholds detect smaller deviations; higher thresholds reduce false positives.  

### Rupture Probability
- **k (Slope)**: Sharpness of the probability curve.  
- **Midpoint**: Center of the probability curve (rupture probability = 0.5).  

**Interpretation**:  
Defines how aggressively QSI converts drift margins into rupture probabilities rather than binary signals.  

### EWMA Parameters
(Available when EWMA mode is selected.)  
- **Alpha**: Responsiveness of smoothing (0.1 = slow, 0.8 = fast).  
- **k**: Width of the adaptive band, relative to volatility.  

### Cognize Meta-Policy
(Available when Cognize is active.)  
- **Epsilon**: Exploration rate; frequency of testing alternative policies.  
- **Promote Margin**: Advantage required before promoting a new policy.  
- **Cooldown Steps**: Minimum interval before switching policies again.  

### Custom Models
- **Custom Model**: Select an enterprise-defined threshold generator.  
- **Custom Parameters**: Adjust the parameters of the custom model.  
- **Respect Custom Î in Cognize**: Determines whether Cognize must follow the enterprise threshold rather than its own.  

---

## 3. Analysis Outputs
The analysis panel presents:  

- **Drift Curve**: Absolute deviation between forecasts and actuals.  
- **Threshold Curve (Î)**: Adaptive threshold line.  
- **Rupture Markers**: Points where drift exceeds threshold.  
- **Loss Curve**: Estimated monetary loss at rupture points.  

Outputs can be downloaded as CSV (rupture events) or JSON (full report).  

---

## 4. Board-Level Diagnostics
Metrics are computed by the Epistemic Analytics module.  

- **Scope Score**: Proportion of recent drifts falling within the baseline band.  
- **Population Stability Index (PSI)**: Degree of distributional shift between baseline and recent drift.  
- **ETA to Persistent Breach**: Projected time until sustained rupture conditions occur.  
- **Pareto Loss Share**: Concentration of loss among top X% of days.  
- **Weekend vs. Weekday Drift**: Relative volatility across calendar segments.  
- **Policy Breakdown** (if applicable): Comparative drift and loss statistics between policy and non-policy groups.  
- **Segment Breakdown** (if applicable): Drift and rupture statistics per SKU, region, or segment.  

---

## 5. Developer Mode
QSI can be used directly as a Python library:

```python
from qsi import QSIEngine, QSIConfig, generate_dummy

df = generate_dummy(days=60, segments=["SKU-A", "SKU-B"])
cfg = QSIConfig(use_ewma=True, ewma_alpha=0.2, ewma_k=3.0)
engine = QSIEngine(cfg)
df_out, report = engine.analyze(df, groupby="Segment")
```

Custom threshold models can be registered:

```python
from qsi.qsi_engine import register_custom_model

def my_model(drift, params, df):
    return drift.rolling(7).mean() * 1.2

register_custom_model("my_theta", my_model)
```

---

## 6. Use Cases
QSI is domain-agnostic and adaptable:

- **Supply Chains**: Detect demand forecast ruptures, safeguard margins.  
- **Pharmaceuticals**: Monitor deviation in clinical trial outcomes.  
- **Cybersecurity**: Identify anomalous drifts in access or transaction logs.  
- **Finance**: Detect regime shifts in trading signals or risk exposures.  
- **IoT and Sensors**: Real-time rupture detection in sensor networks.  

---

## Conclusion
QSI provides an adaptive framework for monitoring, diagnosing, and managing drift in volatile environments. Its design balances interpretability, configurability, and extensibility, enabling application across diverse industries.
