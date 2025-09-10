<p align="left">
  <img src="QSI_logo.png" alt="QSI Logo" width="60"/>
</p>

<h1 align="center">Policy‑Calibrated Drift Intelligence for Franchise Procurement</h1>

## Table of Contents
1. Executive Summary
2. Business Problem Definition
3. Methodological Framework
4. Dataset Overview and Data Integrity Verification
5. Analytical Architecture and Statistical Logic
6. Field Findings: Drift, Loss, and Rupture Clusters
7. Scenario Modeling and Sensitivity Testing
8. Policy and Market Dynamics — Data‑Supported Alignment
9. Macro‑Economic Relevance — Theory‑to‑Field Validation
10. Strategic Business Impact Framework
11. Evidence Exhibits — Action, Facts, Decision
12. Scenario & Sensitivity (Policy‑Calibrated, Directional)
13. Operating Model (SOP) — Priced Exceptions, Policy‑Aware
14. Risks & Guardrails
15. Financial Impact
16. References and Data Provenance Appendix
17. Appendix — Data, Definitions, Parameters

---

## 1. Executive Summary
This study operationalizes **drift diagnostics and preventable loss quantification** using **QSI** within a **multi‑outlet rice procurement chain** during a **policy‑distorted market period** (May–June 2025).  
The system surfaced **₹31,009 preventable loss (1.0826% of spend)**, correctly identifying **internal execution drift** and **external policy‑induced ruptures**.  
All claims are backed by validated operational records and statistically rigorous drift‑rupture segmentation.

---

## 2. Business Problem Definition
Franchise operations frequently suffer from **silent forecast‑to‑actual divergences**, exacerbated by **macro policy shocks** (government ration releases, paddy bonus cycles).  
ERP systems lack visibility into **day‑level drift economics**, leading to **uncontrolled cumulative financial leakage**.

This system closes the gap by providing **daily ₹‑quantifiable rupture triggers**, operationalizing **cost governance and policy shock insulation**.

---

## 3. Methodological Framework
- **Rupture Flagging:** Forecast vs Actual divergence breaching adaptive threshold Θ (drift memory + operational noise).  
- **Financial Impact:** Loss = Drift × Unit Cost, calculated **only on rupture days**.  
- **Volatility Mapping:** EWMA applied to highlight trend shifts without contaminating core loss logic.  
- **Scenario Projections:** 50% rupture suppression scenarios modeled.  

---

## 4. Dataset Overview and Data Integrity Verification
| Metric | Source Validation |
|---|---|
| Forecast, Actual | Daily franchise procurement records (internal logs) |
| Unit Cost | ₹46–₹48/kg (validated against TradeIndia, Napanta Telangana mandi prices) |
| Policy Intervention Window | Telangana public orders, May–June 2025 |
| Analytical Transparency | Full pipeline audit; no imputation; direct CSV computation |

---

## 5. Analytical Architecture and Statistical Logic
- **Mean Drift:** 32.3 units/day  
- **Std Dev Drift:** 36.5 units/day  
- **Rupture Frequency:** 7/61 days (**11.5%**)  
- **Cluster Skew:** 100% of losses occurred in 7/61 days (strong Pareto behavior)

**Statistical procedures:** weighted mean and standard deviation on `(Forecast − Actual)`; segment analysis via `Date.weekday()`; policy period as fixed binary classifier (May 10–30).

---

## 6. Field Findings: Drift, Loss, and Rupture Clusters
| Dimension | Observed Effect |
|---|---|
| **Total Preventable Loss** | ₹31,009 (validated via rupture triggers) |
| **Average Daily Spend** | ₹46,957 |
| **Leakage Rate** | 1.0826% of spend |
| **Max Single‑Day Drift** | 120 units |
| **High‑Drift Periods** | Policy weeks show a **2–3× right‑shifted** distribution; spikes are short, high‑amplitude |

---

## 7. Scenario Modeling and Sensitivity Testing
| Scenario | Annualized Loss Reduction |
|---|---|
| Status Quo | ~₹185,546/year preventable loss (1.08%) |
| 50% Rupture Suppression | ~₹92,773/year saved (≈0.54% EBITDA defense) |
| 60% Rupture Suppression | ~₹111,327/year saved (≈0.65% EBITDA defense) |
| Vendor Rotation Smoothing | Smoother supplier scheduling to reduce clustered spikes |

---

## 8. Policy and Market Dynamics — Data-Supported Alignment
- **Telangana Government Incentives**: ₹500/quintal bonus + ration bulk dump → caused **8.3% price suppression** but **2.5× drift amplification** ([Deccan Chronicle](https://www.deccanchronicle.com/))
- **Empirical Data Link**: Drift variance during policy = **61.7 kg/day**, non-policy = **19.8 kg/day**
- **Net Outcome**: Price reductions **failed to translate into actual efficiency**, validating systemic market misalignment.
  
**Graphical Evidence — Policy vs Non‑Policy Drift**
![Violin — Policy vs Non-Policy](graphs/violin_policy_vs_nonpolicy_clean.png)

---

## 9. Macro‑Economic Relevance — Theory‑to‑Field Validation
| Supply Chain Principle | Field Validation |
|---|---|
| **Bullwhip Amplification (proxy)** | Higher variance/CoV in policy weeks |
| **Demand Decoupling** | Weekday central drift > weekend |
| **Profitability Drainage** | ₹‑denominated rupture tickets expose micro‑leakage |
| **Correctable Drift Vectors** | Majority of loss recoverable by targeting spike days |

---

## 10. Strategic Business Impact Framework
- ₹‑linked **daily drift‑to‑loss visibility**.  
- **Ration cycle protection** via policy‑aware profile.  
- Scalability to **non‑rice commodities** (vegetable, dairy).  
- Alignment with **managerial KPIs** and finance accruals.  
- Validation through **operational records** and **market context**.

---

## 11. Evidence Exhibits — Action, Facts, Decision

### Distribution Shift — Policy vs Non‑Policy
![ECDF — Policy vs Non-Policy](graphs/ecdf_policy_vs_nonpolicy_clean.png)

**Facts:** Median **10 → 50**, P75 **30 → 80**, mean **21.0 → 53.8**.  
**Decision:** Pre‑schedule a **Policy profile** (Θ ≈ 83–85).

---

### Loss Concentration
![Lorenz — Loss Concentration](graphs/lorenz_loss_concentration_clean.png)

**Facts:** **100%** of preventable loss sits in **7/61** days.  
**Decision:** Focus management on **spike days**; score vendors on **breach × ₹ loss**.

---

### Operational Timeline
![Rupture Timeline — Drift vs Θ](graphs/rupre_plot.png)

**Facts:** Normal weeks are quiet at Θ=98; policy weeks show short, high‑amplitude spikes.  
**Decision:** Run SOP only on rupture tickets; **no broad process change** required.

---

### Rupture‑Day Loss Tickets
![Rupture-Day Loss Tickets](graphs/bar_rupture_losses_clean.png)

---

## 12. Scenario & Sensitivity (Policy‑Calibrated, Directional)
*Static‑threshold “what‑if” (for intuition only; QSI is adaptive with UI toggles).*

| Θ (static) | Triggered days | ₹ captured if all ≥ Θ | Read |
|---:|---:|---:|---|
| **98** | **8** | **₹40,162** | Baseline capture of heavy tails |
| **80** | **11** | **₹50,679** | **+3 days**, ~**₹10,517** extra captured during policy |

**Implication:** Maintain **Base Θ=98**; in **policy windows**, dip to **80–85** to capture more without noise flood.

---

## 13. Operating Model (SOP) — Priced Exceptions, Policy‑Aware
**On breach:** (1) call vendor, (2) split order, (3) shift purchase window, (4) defer 1 day if stock buffer ≥ 1 day.  
**Policy overlay:** set Θ ≈ 83–85; cooldown 20 → 10; confirm secondary supplier capacity.

---

## 14. Risks & Guardrails
- **Sample breadth (61 days):** maintain ECDF monitors; review quarterly.  
- **Cost–drift co‑movement:** track drift × cost quantiles.  
- **Threshold gaming:** dual trigger = (drift ≥ Θ) OR (drift × cost ≥ ₹3,000).  
- **Strategic buys:** enforce post‑mortem tags (avoidable / strategic / glitch).  

---

## 15. Financial Impact
- **Baseline leakage (status quo):** **~₹185,546/year**.  
- **Policy profile + SOP (feasible):** **~50–60% reduction ⇒ ₹92,773–₹111,327/year saved**.  
- **Per ₹1 crore spend:** **₹54,129–₹64,954/year** uplift.  

---

## 16. References and Data Provenance Appendix
- Internal: hyderabad_saffron_rice_supply_may_june.csv; qsi_results.csv.  
- Market rates: TradeIndia; Napanta.  
- Policy signals: Telangana public orders; trade press.  
- Academic: Pareto clustering; bullwhip amplification.  

---

## 17. Appendix — Data, Definitions, Parameters
- **Data:** daily procurement CSV; QSI outputs.  
- **Definitions:** Drift = |Forecast−Actual|; Loss = Drift × Unit Cost when drift > Θ.  
- **Run settings (Normal profile):** Θ=98; α=0.02; c=0.25; σ=5; vol=7d; ε=0.10; cooldown=20.  

---

