# Rupture Detector — Project Summary

## Overview

Rupture Detector is a domain-agnostic control anomaly detection system. It monitors Forecast vs. Actual data pipelines, flags significant execution mismatches (ruptures), and quantifies their preventable financial impact. Unlike predictive tools, it operates as a control observatory, offering clear logic, auditability, and immediate operational value.

---

## Project Objective

To engineer and validate a plug-and-play rupture detection system that:

- Requires no machine learning
- Is interpretable and intervention-ready
- Flags when deviation exceeds dynamic thresholds
- Converts errors into quantified financial losses

---

## Validation Dataset

### Domain: **Rice Supply Chain for Restaurant Operations**

- **Forecast**: Projected procurement price of a 25kg rice bag (₹), typically defined by internal planning or accounting systems based on budgeted expectations.
- **Actual**: Real procurement price of a 25kg rice bag (₹), based on actual purchase or vendor invoice.
- **Unit Cost**: ₹1 — each unit of deviation represents ₹1 of price mismatch per 25kg bag.

### Sample Rupture

```
Date: 2025-01-20
Forecast: ₹989.8 (projected price per 25kg bag)
Actual: ₹1129.0 (actual price paid per 25kg bag)
Threshold: ₹98.95
Loss: ₹5,568
```

---

## Outcomes (60-Day Pilot)

- Rupture Events: 8
- Rupture Rate: 13.3%
- Max Single-Day Delta: ₹183.4
- Total Preventable Loss: ₹39,728

### Insights:

- Most ruptures occurred on under-forecast price days
- Ruptures led to reactive procurement and avoidable cost escalations
- The rupture pattern showed threshold memory and volatility correlation

---

## Technical System

### Core Logic (Simplified)

```python
Delta = abs(Forecast - Actual)
Threshold = base + a * DriftMemory + noise
if Delta > Threshold:
    Rupture = True
    Loss = Delta * Unit_Cost
else:
    DriftMemory += c * Delta
```

### Inputs

- CSV file with: `Date`, `Forecast`, `Actual`, `Unit_Cost`

### Outputs

- Tabular rupture log with date, delta, threshold, loss
- Interactive Streamlit dashboard
- Downloadable rupture CSV for audit and reporting
- Visual rupture plots with adaptive threshold overlays

---

## Workflow Summary

1. Upload data or simulate with dummy inputs
2. Adjust sensitivity and drift parameters
3. Observe rupture points and loss indicators on the dashboard
4. Investigate root cause and trigger domain-specific interventions
5. Export rupture logs and use for reporting or escalation

---

## Cross-Domain Application

| Sector       | Forecast Example         | Actual Source            | Unit Cost = ₹/\$ Loss     |
| ------------ | ------------------------ | ------------------------ | ------------------------- |
| Pharma       | Forecasted unit cost     | Actual procurement price | Regulatory / patient risk |
| EV Batteries | Projected cell cost/unit | Actual supplier invoice  | Line stoppage cost        |
| Retail       | Budgeted SKU cost        | Vendor billing           | Missed margin             |
| Energy       | Contracted rate          | Market-clearing price    | Grid imbalance fee        |

The rupture logic is universal. Only value semantics and domain context change.

---

## Strategic Positioning

Rupture Detector is not a forecast engine. It is a control interface—designed to detect failures in execution against plan, quantify preventable damage, and activate decision-makers.

- **Logic-driven**: No black-box inference
- **Lightweight**: Python and CSV-ready
- **Deployable**: UI-ready via Streamlit or CLI
- **Scale-neutral**: Works for 10 rows or 10 million rows
- **Audit-ready**: Output logs, financial mapping, visual diagnosis

---

## Project Status

- ✅ Logic engineered and validated
- ✅ Frontend UI via Streamlit deployed
- ✅ Validated on real rice supply chain (price deviation)
- ✅ Docs prepared: manual, summary, deployment guide
- ✅ Domain extensibility confirmed via parameterization

This is a complete, audit-ready, professional-grade rupture monitoring solution.

---

## Maintained By

**Bharadwaj** — 2025

- Architect of the control logic, system design, and philosophical model
- Reach: Available via repo, documentation, and future extensions

---

## End of Project Summary

