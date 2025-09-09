# QSI User Guide

Quantitative Stochastic Intelligence (QSI) is an adaptive rupture detection and epistemic diagnostics engine.  
It integrates native statistical thresholds, EWMA smoothing, and Cognize-based metapolicies into one framework.  
This guide explains each control, parameter, and output so that users can confidently apply QSI across domains.

---

## 1. Getting Started

You can run QSI in two modes:
- **Streamlit App**: Upload your dataset (`Date, Forecast, Actual, Unit_Cost`) and configure detection interactively.  
- **Python API**: Import QSI in your own scripts.

```python
from qsi import QSIEngine, QSIConfig, generate_dummy

cfg = QSIConfig()
engine = QSIEngine(cfg)
df_out, report = engine.analyze(df)
```

---

## 2. Detection Engine Modes

- **Native Thresholds**: Base formula with memory accumulation and noise.  
- **EWMA Threshold**: Exponentially Weighted Moving Average for adaptive smoothing.  
- **Cognize**: Policy-driven metacontrol for adaptive, self-correcting thresholds.  
- **Graph Mode**: Coupling across multiple segments (e.g., SKUs, regions).  

---

## 3. Threshold Parameters

- **Base Threshold (Îâ):** Initial sensitivity to drift.  
- **a (Sensitivity):** Degree to which accumulated memory (E) raises the threshold.  
- **c (Memory Accumulation):** Rate at which drift compounds in memory.  
- **Ï (Noise):** Stochastic fluctuation applied to the threshold.  

**Interpretation:**  
- Lower thresholds detect smaller deviations (sensitive but noisy).  
- Higher thresholds filter noise but risk missing subtle ruptures.  

---

## 4. EWMA Parameters

- **Î± (Alpha):** Weight given to recent drift values. Closer to 1 â faster adaptation.  
- **k (Multiplier):** Number of standard deviations applied to define the threshold band.  

**Use Case:** When markets are volatile and require adaptive smoothing.  

---

## 5. Cognize Metapolicy

- **Îµ (Exploration):** Probability of exploring new policies.  
- **Promote Margin:** How much better a candidate policy must perform before adoption.  
- **Cooldown Steps:** Delay before the same policy is reconsidered.  

**Use Case:** When you want the system to learn which thresholding strategy works best.  

---

## 6. Probability Model

- **k (Slope):** Controls sharpness of probability curve around threshold.  
- **Midpoint:** Defines margin at which rupture probability is 50%.  

**Interpretation:** A steeper slope means âhardâ ruptures. A shallower slope means âsofterâ probability.  

---

## 7. Graph Parameters (Multi-Segment)

- **Graph Damping:** Reduces cascade intensity across segments.  
- **Max Graph Depth:** How far influence propagates across networked nodes.  

**Use Case:** Multi-SKU, multi-region, or multi-asset systems where failures propagate.  

---

## 8. Epistemic Diagnostics

QSI integrates board-level analytics for governance and systemic resilience:  

- **Scope Score (0â1):** Fraction of recent drift contained within baseline band.  
- **PSI (Population Stability Index):** Distribution shift indicator.  
- **ETA (Expiry to Persistent Breach):** Projected time until consistent rupture.  
- **Pareto Share:** Fraction of loss driven by top X% of days.  
- **Weekend vs Weekday Multiplier:** Drift skew across calendar effects.  

---

## 9. Outputs

- **Drift:** Absolute deviation between forecast and actual.  
- **Theta (Î):** Applied threshold at each step.  
- **Rupture:** Binary event when drift > Î.  
- **Loss:** Economic impact (drift Ã unit cost).  
- **Report JSON:** Structured summary for downstream systems.  

---

## 10. How to Use Each Toggle (Streamlit UI)

- **Use EWMA Threshold:** Enables adaptive smoothing.  
- **Enable Cognize:** Activates metapolicy learning.  
- **Use Graph Mode:** Links segments dynamically.  
- **Show Rolling Mean:** Adds contextual smoothing line.  
- **Volatility Band Window:** Defines rolling window for Â±1Ï band.  
- **Y-Grid:** Toggles vertical scale clarity.  

---

## 11. Best Practices

- Start with **EWMA** for adaptive baselines.  
- Enable **Cognize** when facing unpredictable environments.  
- Use **Graph Mode** only when clear cross-segment dependencies exist.  
- Review **Economics** and **Epistemic** sections before making board-level decisions.  

---

## 12. Example Workflow

1. Upload CSV (`Date, Forecast, Actual, Unit_Cost`).  
2. Select segmentation column if applicable.  
3. Choose detection model (Native, EWMA, Cognize).  
4. Tune threshold, memory, and noise parameters.  
5. Analyze rupture events, losses, and diagnostics.  
6. Export CSV/JSON for reporting or enterprise integration.  

---

## 13. Disclaimer

QSI is an adaptive intelligence engine. Its outputs depend on configuration and data quality.  
For mission-critical environments (e.g., healthcare, finance, infrastructure), validate before deployment.  
