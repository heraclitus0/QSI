
# Project Report

## Rupture Detector: Field-Validated Volatility Detection in Urban Rice Procurement  
**Hyderabad, May–June 2025**

---

## 1. Introduction

This report documents the application of **Rupture Detector**, a lightweight diagnostic tool designed to detect supply chain drift and quantify preventable procurement loss in an urban restaurant-grade rice sourcing context. The tool was field-tested on Sona Masoori rice procurement over a two-month operational cycle.

---

## 2. Objective

To detect procurement rupture events, quantify preventable economic loss, and surface actionable drift signals for improving supplier alignment.

---

## 3. Methodology

**Tool:** Rupture Detector (Rupture Logic Engine with Streamlit UI)  
**Input Fields:** Forecast (bags), Actual (bags), Unit Cost (₹ per 25kg bag)  
**Drift Logic:**  
- Daily drift = `Forecast - Actual`  
- Rupture triggered when drift exceeds adaptive threshold Θ (accounting for rolling memory and operational noise)  
- Preventable Loss = `Drift × Unit Cost`

---

## 4. Dataset & Validation

- **Deployment Period:** 61 days (May–June 2025)  
- **Commodity:** Sona Masoori rice, 25kg bag unit  
- **Procurement Setting:** Urban restaurant franchise with thali-centric daily rice consumption  
- **Data Source:** Direct procurement logs, verified against regional pricing databases  
- **Validation References:** Cost ranges validated against TradeIndia, Napanta, and market listings for Sona Masoori during the deployment window

---

## 5. Results Summary

| **Metric** | **Value** |
|-------------|-----------------------------|
| **Total Operational Days** | 61 days |
| **Rupture Events Detected** | 6 |
| **Total Drift Accumulated** | 551 bags |
| **Max Single-Day Drift** | 22 bags |
| **Total Preventable Loss** | ₹30,857 |
| **Maximum Daily Loss** | ₹5,635.20 |
| **Average Drift Threshold (Θ)** | ~101.5 bags |

---

## 6. Case Snapshot

### Example Rupture Events

| Date       | Forecast | Actual | Drift | Threshold | Unit Cost (₹/bag) | Loss (₹)   |
|------------|----------|--------|-------|-----------|-------------------|------------|
| 2025-05-09 | 172 bags | 150 bags | 22 | 102 | ₹256 | ₹5,632 |
| 2025-05-29 | 200 bags | 185 bags | 15 | 99 | ₹255 | ₹3,825 |

Rupture events reflected supplier inconsistencies and forecast inaccuracies, exposing latent procurement inefficiencies.

---

## 7. Strategic Action

By mapping rupture occurrences, the procurement system identified actionable opportunities for:
- Supplier base diversification,
- Direct sourcing pathways,
- Dynamic procurement adjustments minimizing unplanned economic exposure.

---

## 8. Validation Summary

- **Pricing Levels:** In line with Hyderabad wholesale rice ranges (₹240–₹260 per 25kg bag during Rabi 2024–25 cycle)  
- **Drift-to-Loss Calculations:** Directly traceable to primary logs and Rupture Detector computational output  
- **Real-world Actionability:** Insights contributed to short-term supplier bridge formation

---

## 9. Conclusion

Rupture Detector successfully translated supply volatility into **quantifiable operational intelligence**. Its field deployment verified capability to detect unanticipated procurement loss and facilitate more resilient sourcing strategies.

---

## 10. References

**Code & Tooling:**  
- [Rupture Detector GitHub](https://github.com/heraclitus0/rupture-detector)  
- [Live Streamlit Deployment](https://rupture-detector-vxcv8twev4y3vcuqzjprnw.streamlit.app/)

**Public Data References:**  
- [TradeIndia – Sona Masoori Pricing](https://www.tradeindia.com/hyderabad/sona-masoori-rice-city-196467.html)  
- [Napanta – Telangana Mandi Prices](https://www.napanta.com/)  
