# QSI User Guide

This document provides a structured reference for operating the QSI platform.  
Every toggle, slider, and parameter is explained in practical terms for decision-makers and analysts.

---

## Getting Started

1. **Upload Data**: Provide a CSV with the required columns:
   - `Date`
   - `Forecast`
   - `Actual`
   - `Unit_Cost`

2. **Run Analysis**: QSI computes drift (the deviation between forecast and actual), evaluates thresholds, flags ruptures, and calculates losses.

3. **Interpret Outputs**:
   - **Economics**: Quantifies total loss, over-forecast vs under-forecast, severity, and per-unit efficiency.
   - **Epistemic**: Diagnostics such as scope score, PSI, and breach ETA.
   - **Visuals**: Interactive drift vs. threshold chart, volatility bands, rupture markers, and optional heatmaps for segments.

---

## Threshold Parameters

- **Base Threshold**  
  Initial sensitivity to drift. Higher values make the system less sensitive.

- **a (Sensitivity)**  
  Degree to which accumulated memory raises the threshold.  
  Controls how past deviations influence current tolerance.

- **c (Memory Accumulation)**  
  Rate at which drift compounds in memory. Higher values increase persistence.

- **sigma (Noise)**  
  Random fluctuation applied to the threshold to simulate uncertainty.  
  Lower = stable detection; higher = more variability.

**Interpretation**:  
The threshold defines when a deviation becomes a rupture.  
- Lower thresholds detect smaller deviations but may over-trigger.  
- Higher thresholds reduce false positives but may miss early warnings.

---

## EWMA (Exponentially Weighted Moving Average)

- **Enable EWMA**: Uses adaptive smoothing instead of static thresholds.  
- **Alpha (α)**: The smoothing factor. Lower values = longer memory; higher = faster reaction.  
- **k**: Multiplier for variability. Larger values make the threshold more tolerant.

Use EWMA when trends shift gradually and static thresholds would over-trigger.

---

## Cognize Meta-Policy

- **Enable Cognize**: Switch to adaptive intelligence mode.  
- **Epsilon (ε)**: Exploration rate. Higher values explore more candidate policies.  
- **Promote Margin**: How much better a candidate must be to replace the current policy.  
- **Cooldown Steps**: Steps before a newly promoted policy can change again.

Cognize allows self-tuning thresholds and policies during runtime.

---

## Graph Mode

- **Enable Graph**: Couple multiple segments (e.g., products, regions).  
- **Graph Damping**: Strength of influence between segments (0 = no influence, 1 = strong coupling).  
- **Max Graph Depth**: How far influence cascades through the network.

Graph mode models interdependencies across units.

---

## Rupture Probability

- **k (Slope)**: Sharpness of the probability curve.  
- **Midpoint**: Margin value where rupture probability is 50%.

This converts drift vs. threshold into a probability, useful for risk calibration.

---

## Epistemic Diagnostics

- **Baseline Window**: Number of days used to define “normal” drift.  
- **Recent Window**: Size of the recent comparison slice (default = baseline size).  
- **Scope Quantiles**: Defines the “in-scope” band of drift relative to baseline.  
- **PSI Bins**: Granularity for Population Stability Index (drift distribution shifts).  
- **ETA Parameters**:  
  - *Consecutive Breaches (k)*  
  - *Lookback Window*  
  - *Min Points for Trend*  

Diagnostics provide board-level insight into stability, breach risk, and systemic drift.

---

## Interpretation Framework

1. **Economics Panel**  
   Shows how much loss drift caused, broken into categories:
   - Over-forecast vs. under-forecast
   - On-target vs. severe deviations
   - Per-unit efficiency

2. **Epistemic Panel**  
   Shows systemic health:
   - Scope score (0–1)  
   - PSI (distribution shift)  
   - ETA to persistent breach  
   - Expiry date estimate  

3. **Charts**  
   - **Drift vs. Threshold**: Tracks deviations and rupture points.  
   - **Volatility Bands**: Show rolling variability.  
   - **Segment Heatmap**: Segment-level rupture probabilities.

---

## Practical Use Cases

QSI is domain-agnostic and applicable across industries:

- **Pharma Supply Chains**: Monitor forecast vs. actual drug demand.  
- **Manufacturing**: Detect deviations in production throughput.  
- **Finance**: Track risk breaches in portfolio models.  
- **Cybersecurity**: Detect anomalies in network traffic baselines.  
- **Retail**: Align demand forecasting with sales outcomes.  
