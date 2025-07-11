# Rupture Detector — User Manual

## Purpose

Rupture Detector is a domain-agnostic control monitoring system. It identifies executional mismatches in Forecast vs. Actual data pipelines, calculates the financial impact of deviation, and flags high-loss anomalies called ruptures. This manual explains how to use the system effectively—without needing to understand its internal code.

---

## Step 1: Upload Your Data

### Required Columns

Your input `.csv` must contain the following headers:

```
Date, Forecast, Actual, Unit_Cost
```

### Sample Row

```
2025-01-20, 989.8, 1129.0, 40
```

- **Forecast**: Your planned quantity (e.g. demand, dosage, energy)
- **Actual**: What was executed or measured
- **Unit\_Cost**: Value of deviation per unit (₹ or \$)

### Dummy Mode

If you want to test the system, activate “Use Dummy Data” to auto-generate inputs.

---

## Step 2: Set Your Parameters

Use the left sidebar panel to tune the system:

| Setting              | Role                                                      |
| -------------------- | --------------------------------------------------------- |
| Drift Scaling Factor | Memory rate of past deviations (suggested: 0.6–0.9)       |
| Rupture Sensitivity  | How sharply thresholds respond to memory buildup          |
| Base Threshold       | Minimum deviation tolerated before triggering rupture     |
| Noise Estimate       | Adds noise to threshold (defends against false positives) |
| EWMA Alpha (Visual)  | Smoothens threshold curve (for readability only)          |
| Sigma Multiplier     | Expands/shrinks tolerance band in EWMA overlay            |

All values update logic in real time.

---

## Step 3: Interpret Results

### Visual Graph

- **Blue Line**: Delta (|Forecast - Actual|)
- **Light Blue Line**: Adaptive Threshold
- **Red Dot**: Rupture (Delta > Threshold)

### Summary Panel

- **Total Preventable Loss**: Sum of all rupture-based losses
- **Rupture Table**: Date, Delta, Threshold, and ₹ Loss breakdown

---

## Step 4: Take Action

For each rupture flagged:

- Confirm: Was the deviation real or a data error?
- Investigate: Why did the plan fail?
- Mitigate: Adjust supply, notify vendors, reallocate resources

Every rupture includes its calculated financial loss, helping prioritize response.

---

## Step 5: Download Logs

Use the “Download Rupture Report (CSV)” button to export structured records for:

- Audit
- Reporting
- Intervention analysis

---

## Usage Summary

✅ No code needed\
✅ Runs on any structured Forecast–Actual data\
✅ Domain-neutral: rice, pharma, retail, energy, battery logistics\
✅ Built for professionals—not experiments

You are not predicting the future. You are controlling deviation.

---

## Authorship & Vision

Developed and maintained by **Bharadwaj** (2025)\
This system is part of a broader epistemic framework focused on rupture detection and control.\
It is designed to quantify operational loss, highlight intervention points, and reframe response from reactive to commanding.

---

## End of User Manual

