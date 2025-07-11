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

- **Forecast**: Daily projected rice usage (kg)
- **Actual**: Rice consumed or dispatched
- **Unit Cost**: ₹40/kg (cost of stockout or oversupply)

### Sample Rupture

```
Date: 2025-01-20
Forecast: 989.8
Actual: 1129.0
Threshold: 98.95
Loss: ₹5,568
```

---

## Outcomes (60-Day Pilot)

- Rupture Events: 8
- Rupture Rate: 13.3%
- Max Single-Day Delta: 183.4 kg
- Total Preventable Loss: ₹39,728

### Insights:

- Most ruptures occurred on under-forecast days
- Ruptures led to either emergency sourcing or excess idle stock

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

---

## Workflow Summary

1. Upload data or simulate with dummy inputs
2. Adjust sensitivity and drift parameters
3. Observe ruptures and loss indicators
4. Investigate cause and apply interventions
5. Export rupture logs for further review

---

## Cross-Domain Application

| Sector       | Forecast Example     | Actual Source          | Unit Cost = ₹/\$ Loss     |
| ------------ | -------------------- | ---------------------- | ------------------------- |
| Pharma       | Daily doses required | Dispensed records      | Regulatory / patient risk |
| EV Batteries | Cell need forecast   | Inbound inventory logs | Line stoppage cost        |
| Retail       | SKU sales projection | POS scanner data       | Missed margin             |
| Energy       | Load estimation      | Real generation draw   | Grid imbalance fee        |

The rupture logic is universal. Only labels and cost values change.

---

## Strategic Positioning

Rupture Detector is not a forecast engine. It is a control interface—designed to detect failures in execution against plan, quantify preventable damage, and activate decision-makers.

- **Logic-driven**: No black-box inference
- **Lightweight**: Python and CSV-ready
- **Deployable**: UI-ready via Streamlit or CLI
- **Scale-neutral**: Works for 10 rows or 10 million rows

---

## Project Status

- ✅ Logic engineered and validated
- ✅ Frontend UI via Streamlit deployed
- ✅ Validated on real rice supply chain
- ✅ Docs prepared: manual, summary, deployment guide

This is a complete, audit-ready, professional-grade rupture monitoring solution.

---

## Maintained By

**Bharadwaj** — 2025

- Architect of the control logic, system design, and philosophical model
- Reach: Available via repo, documentation, and future extensions

---

## End of Project Summary

