# 📄 Final Professional Project Report — Rupture Detector: Policy-Aware Drift Diagnostics in Franchise Procurement Systems

## Table of Contents
1. Executive Summary
2. Business Problem Definition
3. Methodological Framework
4. Dataset Overview
5. Analytical Architecture
6. Field-Level Insights
7. Scenario and Sensitivity Simulations
8. Policy and Market Dynamics
9. Macro-Economic Alignment
10. Strategic Business Takeaways
11. Conclusion
12. References

---

## 1. Executive Summary

This report validates the **Rupture Detector System** as a strategic diagnostic tool for **franchise-level rice procurement networks**, effectively surfacing ₹30,857 of preventable loss across 61 days (1.15% of spend). Rupture Detector not only identifies **operational inefficiencies**, but critically captures **policy-triggered volatility distortions** through statistically rigorous **rupture-day detections**, enabling **real-time financial accountability** at an operational level.

---

## 2. Business Problem Definition

Modern procurement chains face hidden **forecast-to-actual divergences**, especially when external market distortions occur due to **government interventions**. Traditional ERP systems lack day-level resolution, leaving franchises vulnerable to **silent cumulative losses**.

**Key Gaps Addressed:**
- Lack of **day-to-day drift detection**.
- No **₹-denominated preventable loss traceability**.
- Absence of **policy-aware procurement correction tools**.

---

## 3. Methodological Framework

### 3.1 Core Calculations
- **Drift = Forecast – Actual** (kg/day).
- **Adaptive Threshold Θ** identifies rupture days dynamically.
- **Preventable Loss = Drift × Unit Cost**, computed only when **Drift > Θ**.

### 3.2 Volatility Visualization
- **EWMA (α=0.2)** overlays capture broader volatility trends.

### 3.3 Scenario Modeling
- Evaluated potential financial uplifts under **rupture suppression interventions**.

---

## 4. Dataset Overview

| Dimension | Value |
|------------|-------|
| Duration | 61 days (May–June 2025) |
| Location | Multi-outlet Hyderabad franchise |
| Daily Forecast Volume | ~944 kg/day |
| Unit Cost | ₹46.63/kg (market-aligned ₹45–₹50/kg) |
| Daily Spend | ₹44,073/day average |
| Policy Period Flagged | May 10–30 |

✅ **Clean, log-verified data** sourced from franchise records.

---

## 5. Analytical Architecture
- ✅ **Theta-logic rupture detection**.
- ✅ **EWMA-based volatility signaling**.
- ✅ **₹-based preventable loss mapping**.
- ✅ **CSV-pipeline, Streamlit UI**, **zero backend dependency**.

---

## 6. Field-Level Insights

| Metric | Value |
|---------|--------|
| Total Preventable Loss | ₹30,857 |
| Rupture Frequency | 9.8% (6/61 days) |
| Loss Concentration | 71% of loss in top 20% of days |
| Weekend Drift Uplift | 3× weekday drift |
| Price-Distortion Impact | –8.3% unit cost, +2.5× drift during policy period |

✅ High volatility days aligned with **policy incentives and ration dumps**.

---

## 7. Scenario and Sensitivity Simulations

| Scenario | Annualized Savings Potential |
|-----------|----------------------------|
| Current Drift | ₹180,000/year preventable loss |
| 50% Rupture Reduction | ₹90,000/year savings; +0.5–0.6% EBITDA buffer |

✅ **Partial rupture suppression leads to direct EBITDA protection**, validated by **₹-trackable field data**.

---

## 8. Policy and Market Dynamics
- Telangana **₹500/quintal paddy bonuses**, **bulk ration disbursement**, and **stock disposal schemes** created **forecast inflation and drift spikes**.
- ✅ Rupture Detector captured both **internal inefficiencies** and **external market distortions**.

---

## 9. Macro-Economic Alignment

✅ Maps directly to:
- **Bullwhip Effect** detection (drift volatility under policy distortion).
- **Demand decoupling visibility** (weekend/weekday asymmetry).
- **Operational-profitability linkages** via **₹-quantified rupture events**.

---

## 10. Strategic Business Takeaways
✅ **Low-overhead, rapid deployment**.
✅ **Cross-layer drift diagnostics**.
✅ **Real-time financial governance capability**.
✅ **Macro-aligned volatility detection**.
✅ Applicable across **retail, food services, agri-supply chains**.

---

## 11. Conclusion

Rupture Detector establishes **day-to-day financial accountability in procurement operations**, providing clarity amidst both **internal drift inefficiencies** and **external policy shocks**. It directly enables **profit leakage prevention** with **minimal operational disruption**, aligning frontline action with **board-level financial stewardship**.

---

## 12. References
✅ [GitHub Codebase](https://github.com/heraclitus0/rupture-detector)  
✅ [Streamlit Live Demo](https://rupture-detector-vxcv8twev4y3vcuqzjprnw.streamlit.app/)  
✅ [TradeIndia Sona Masoori Rates](https://www.tradeindia.com/hyderabad/sona-masoori-rice-city-196467.html)  
✅ [Telangana Mandi Prices — Napanta](https://www.napanta.com/)

---

