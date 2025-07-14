
# USER GUIDE – Rupture Detector

## 1. Overview
Rupture Detector is a domain-agnostic operational intelligence tool designed to detect forecast-actual drifts and surface preventable loss in real-world systems. It is applicable to any measurable quantity where planned values (forecasts) often diverge from realized outcomes (actuals), converting these deviations into actionable economic insights.

**Example Applications:**
- Supply Chain Logistics
- Manufacturing Output Tracking
- Energy Demand Management
- Workforce Planning
- Retail Inventory Dynamics
- Financial Forecast Monitoring

---

## 2. System Features
- Adaptive drift detection using rolling and memory-based thresholds.
- Dynamic visualization of operational volatility and rupture events.
- Quantification of preventable economic loss tied to detected ruptures.
- Configurable sensitivity parameters for multiple operational contexts.
- Streamlit-based interactive dashboard for non-technical end users.

---

## 3. Installation Guide

### Prerequisites:
- Python 3.9+
- pip

### Setup Steps:
```bash
git clone https://github.com/heraclitus0/rupture-detector.git
cd rupture-detector
pip install -r requirements.txt
streamlit run app.py
```

---

## 4. Data Input Format

### Required Columns:
| Column | Description |
|---------|-------------|
| `Date` | Date or timestamp (string) |
| `Forecast` | Projected/expected quantity |
| `Actual` | Realized quantity |
| `Unit_Cost` | Cost per unit of deviation (currency, resource, or time unit) |

### Example (CSV):
```csv
Date,Forecast,Actual,Unit_Cost
2025-05-01,1000,950,240
```

### Notes:
- Data granularity can be **daily**, **hourly**, or **transactional** depending on application.
- Higher temporal granularity increases sensitivity to micro-ruptures.

---

## 5. Interactive Dashboard – Controls Guide

### Parameter Controls:
| Control | Purpose |
|----------|---------|
| Drift Scaling Factor | Adjusts impact of accumulated drift on rupture threshold. |
| Rupture Sensitivity | Tunes detection strictness (lower = more sensitive). |
| Base Threshold | Minimum acceptable drift before adjustments. |
| Noise Estimate | Filters routine operational noise. |
| EWMA Alpha | Recent drift weighting (higher alpha = recent data dominance). |
| Sigma Multiplier | Volatility buffer based on standard deviation control. |

### Outputs:
- **Rupture Events**: Days flagged as rupture due to drift exceeding adaptive threshold.
- **Preventable Loss**: Quantified impact (currency or resource units) from unmitigated ruptures.
- **Drift & Rupture Graphs**: Visualize variance and rupture over time.

---

## 6. Interpretation Guidelines

| Output Metric | Interpretation |
|----------------|----------------|
| Drift (Forecast - Actual) | Direct measure of operational forecast error |
| Threshold (Adaptive Θ) | Dynamic tolerance level adjusted for recent volatility |
| Rupture (Binary Flag) | Indicates operational misalignment needing intervention |
| Preventable Loss | Economic/resource quantification of unmitigated ruptures |

---

## 7. Use Case Scenarios

| Sector | Example Use |
|---------|-----------------------------|
| Manufacturing | Compare scheduled vs produced units daily |
| Energy | Detect demand-response mismatches per hour |
| Supply Chain | Monitor daily order vs delivery gaps |
| Human Resources | Forecasted vs actual shift attendance |
| Retail | Predicted vs actual daily sales or inventory restocking |
| Financial Ops | Projected vs actual cash flows or expenses |

---

## 8. Best Practices
- Regularly recalibrate **Base Threshold** and **Noise Estimate** based on your operational norms.
- Use **Rupture Sensitivity** to toggle between conservative and aggressive detection modes.
- For volatile environments, adjust **EWMA Alpha** higher for responsiveness.
- Validate **Unit_Cost** per application domain to ensure meaningful preventable loss estimation.

---

## 9. Troubleshooting Guide

| Issue | Possible Cause | Recommended Fix |
|--------|----------------|-----------------|
| App does not start | Environment misconfiguration | Reinstall requirements, check Python version |
| File upload fails | Incorrect column naming or file format | Ensure column headers match: Date, Forecast, Actual, Unit_Cost |
| Unexpected zero loss | Drift not exceeding threshold | Lower sensitivity or review noise threshold |
| Excessive rupture events | Over-sensitivity or low threshold | Increase base threshold or adjust scaling factor |

---

## 10. References and Links

- **GitHub Repository**: [Rupture Detector](https://github.com/heraclitus0/rupture-detector)
- **Live Demo Deployment**: [Streamlit App](https://rupture-detector-vxcv8twev4y3vcuqzjprnw.streamlit.app/)
- **Theoretical References**:
    - Epistemic Control Concepts: RCC, Continuity Theory
    - Memory-based Drift Detection Literature
- **License**: MIT – free for academic, personal, and commercial use with attribution.

---

© 2025 Pulikanti Sashi Bharadwaj. All rights reserved under the open-source license.
