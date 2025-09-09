# Case Study — Rupture Detector: Quantifying and Reducing Operational Drift in an Agricultural Supply Chain

## Executive Summary
Using day-level procurement data from a Hyderabad rice supply chain over **61 days**, the Rupture Detector surfaced **₹31,009** in **preventable losses** clustered in **7 rupture days**. 
Average daily spend was **₹46,957**, with losses equal to **1.08% of total spend**. Drift is **heavy‑tailed**: all financial loss was concentrated in **7/61 days (11.5%)**.
The system enables **targeted intervention** on spike days while leaving normal operations untouched.

---

## 1) Business Context & Objective
- Procurement variability at the day level creates **silent leakage** that rarely appears in monthly averages.
- Objective: **detect and price day-level drift**, alert on **true rupture** (drift > Θ), and quantify **₹ loss** attributable to rupture events.

---

## 2) Deployment & Data
| Parameter | Value |
|---|---|
| Commodity | Sona Masoori rice (25kg unit bags) |
| Location | Hyderabad (franchise-level procurement) |
| Period | May–June 2025 (**61 days**) |
| Data fields | Forecast, Actual, Unit Cost |
| Stack | CSV backend + QSI processing + lightweight UI |

**Spend model:** `daily_spend = Actual × Unit_Cost`. Loss is computed **only on rupture days** as `loss = drift × Unit_Cost` with `drift = |Forecast − Actual|`.

---

## 3) System Logic (QSI)
- **Θ (Threshold) dynamics**: adaptive limit informed by accumulated misalignment memory **E**.
- **Rupture condition**: trigger when `drift > Θ`.
- **Loss accounting**: only on triggers; normal drift carries **no penalty** to avoid false positives.
- **Probability**: `rupture_prob` ≈ 1 on trigger days; ≈ 0 otherwise.

---

## 4) Results & Operational Findings
**Key metrics**
- **Total preventable loss:** ₹31,009
- **Avg daily spend:** ₹46,957 (total spend ₹2,864,380)
- **Loss as % of spend:** **1.08%**
- **Rupture days:** **7** (all loss concentrated here)
- **Forecast balance:** **30** over‑forecast vs **18** under‑forecast; **13** on‑target
- **Drift distribution:** mean **32.30**, std **36.53**, P50 **10**, P75 **50**, P90 **100**, max **120**
- **MAPE:** 3.52%

**Rupture clustering**
- Ruptures occur as **short, sharp shocks** (see rupture events table below).
- Loss concentration follows **Pareto** behavior: **100.00%** of total loss sits in the **top 13 days** by loss (**top 20% of the calendar**).

---

## 5) Rupture Events (Export)
A machine‑readable export of all rupture events with drift, Θ, probability, and priced loss is included:
- **File:** `rupture_events.csv`

---

## 6) Strategic Implications
1. **Targeted mitigation wins**: Focus playbooks on **spike days**—supplier calls, safety stock toggles, or order reslots only when drift breaches Θ.
2. **Price the risk**: Treat Θ breaches as **priced events** with clear ₹ accountability; fold into vendor scorecards and daily ops checklists.
3. **No disruption on normal days**: Because loss is only booked on triggers, the system **avoids over‑steering**.
4. **Scalable template**: The same Θ/E/rupture logic generalizes to perishables, retail replenishment, and logistics variability.

---

## 7) Conclusion
Rupture Detector converts day‑level misalignment into **actionable, priced events**. In this Hyderabad deployment, it revealed **₹31,009** of **preventable leakage** over **61 days**, concentrated in **7 shocks**, equating to **1.08%** of spend—precisely where focused interventions pay back.

---

*This report is auto‑generated from the supplied CSVs to ensure every figure is traceable to source data.*
