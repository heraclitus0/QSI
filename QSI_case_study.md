<p align="left">
  <img src="QSI_logo.png" alt="QSI Logo" width="60"/>
</p>

<h1 align="center">QSI in a Restaurant Supply Chain</h1>
<h3 align="center">Hyderabad franchise network · May–June 2025 (61 operational days)</h3>

---

## 1. Executive Summary
- **Preventable loss identified:** **₹31,009** across **7 rupture days** (**11.5%** of days).  
- **Total spend:** **₹2,864,379.50**; **average daily spend:** **₹46,957**; **leakage rate:** **1.0826% of spend**.  
- **Operating approach:** Maintain **Base Θ = 98** in normal weeks. In policy windows, apply a **Policy profile** (Θ **83–85**, cooldown **10**, ₹ loss‑floor **3,000**) to capture economically material spikes while containing alert volume.  
- **EBITDA effect (per outlet, annualized):** baseline at risk **~₹185,546/year**; reduction of **50–60%** yields **~₹92,773–₹111,327/year** EBITDA uplift.  
- **Concentration:** Preventable loss was concentrated in a small number of short, high‑amplitude spike days.

---

## 2. Context and Objectives
- **Context:** Day‑level procurement of Sona Masoori rice in a multi‑outlet franchise network. Periodic government interventions (ration and bonus cycles) distort local prices and availability.  
- **Problem:** Monthly aggregates and ERP smoothing obscure day‑level financial leakage; line managers lack priced, actionable triggers.  
- **Objective:** Detect and price only **true ruptures** (when `|Forecast − Actual| > Θ`), produce dated **rupture tickets** (₹ loss = drift × unit cost), and execute a concise operating response on those days.

---

## 3. Methodology
- **Signal:** `Drift = |Forecast − Actual|`.  
- **Trigger:** a day is a rupture when `Drift > Θ`.  
- **Pricing:** `Loss = Drift × Unit_Cost` **only on rupture days** (no penalties on normal days).  
- **Profiles:**  
  - **Normal:** Θ = 98; cooldown = 20; probability slope b = 6.0.  
  - **Policy (windowed):** Θ ≈ 83–85 (≈ −15%); cooldown = 10; ₹ loss‑floor = 3,000; alert budget ≤ 5/week; auto‑restore +2 days post‑window.

---

## 4. Operational Outcomes
- **Rupture days:** **7**; preventable loss fully concentrated in these days.  
- **Distribution shift in policy weeks:** non‑policy → policy medians **10 → 50**, P75 **30 → 80**, means **21.0 → 53.8**.  
- **Interpretation:** Base Θ = 98 is appropriate for normal weeks. A temporary ~15% tightening in policy weeks is justified to intercept the economically material middle of the shifted distribution while remaining within alert capacity.

### Figure 1. Rupture Timeline 
![Rupture timeline — Θ = 98 baseline](graphs/rupre_plot.png)
*Ruptures are brief and high‑amplitude; alerts are sparse in normal weeks.*

---

## 5. Policy Profile (UI‑Aligned)
**Purpose:** Apply a tighter detection profile only in government‑distorted weeks; automatically restore the normal profile after the window.

**Controls and ownership**

| Control | Normal | Policy (window only) | Rationale | Owner |
|---|---:|---:|---|---|
| Threshold (Θ) | 98 | 83–85 | Policy weeks shift drift 2–3× right; ~15% dip captures ₹‑material spikes. | Operations |
| Cooldown | 20 | 10 | Enable action on clustered spikes. | Operations |
| Probability shaping | mid 0.0; slope b=6.0 | mid 0.5 or b=4–5 | Avoid near‑threshold saturation at ~1.0. | Analytics |
| ₹ Loss floor | Off | On at ₹3,000 | Capture medium drift on high‑price days. | Finance |
| Alert budget | n/a | ≤ 5 per week | Capacity guardrail. | Operations |
| Auto‑restore | n/a | +2 days post‑window | Prevent lingering policy mode. | Analytics |

**Activation and deactivation**  
- **Activate** on pre‑announced ration/MSP/bonus/festival windows; optionally if mandi price > +5% d/d **and** ECDF median lifts (two‑signal rule).  
- **Deactivate** at window end **+2 days** (hysteresis), then restore the Normal profile.

**Guardrails**  
- Policy Θ not below the **policy‑week 80th percentile** of drift.  
- If alert volume exceeds budget, raise Θ by +2 points or increase the ₹ floor to ₹3,500.  
- Strategic purchases tagged and excluded from vendor penalties (retained for finance).

---

## 6. Operating Procedure on a Rupture Ticket
1. Call vendor (price and capacity confirmation).  
2. Split order (primary and secondary supplier).  
3. Shift purchase window (time‑of‑day).  
4. Defer one day if stock buffer ≥ one day.  
5. Tag root cause (policy / vendor / demand / strategic).

---

## 7. Financial Impact (EBITDA)
- **Leakage rate:** **1.0826%** of spend.  
- **Baseline at risk (annualized per outlet):** **~₹185,546/year**.  
- **EBITDA uplift (per outlet):** **~₹92,773–₹111,327/year** for a **50–60%** reduction.  
- **Per ₹1 crore of addressable spend:** **₹54,129–₹64,954/year** uplift for **50–60%** reduction.

---

## 8. Governance and Performance Management
- **KPIs:** prevented ₹ per rupture; alert conversion (SOP executed / rupture alerts); vendor breach × ₹ loss (scorecards); alert budget adherence; leakage reduction (rolling 90‑day); false‑positive rate.  
- **Decision rights:** operations own thresholds and cooldowns; analytics own probability shaping and auto‑restore; finance owns the ₹ floor and vendor scorecard consequences.

---

## 9. Risks and Controls
- **Alert fatigue:** minimum‑percentile guardrail, weekly alert budget, and auto‑restore.  
- **False identification of policy weeks:** calendar confirmation or two‑signal rule (price + ECDF).  
- **Over‑steer in normal weeks:** Normal profile remains at Θ = 98.  
- **Data anomalies / strategic purchases:** ticket‑level audit trail; strategic tags excluded from penalties.

---

## 10. Implementation Plan (7 Days)
- **Day 0:** Load data; confirm Base Θ = 98; define policy dates.  
- **Days 1–2:** Shadow mode; measure would‑have alerts; set alert budget (≤5/week).  
- **Day 3:** Go live; enable rupture tickets; brief SOP.  
- **Days 4–5:** Audit two tickets end‑to‑end (actions and pricing).  
- **Day 6:** If budget exceeded, raise Θ by +2 or increase the ₹ floor.  
- **Day 7:** Confirm auto‑restore and next policy calendar.

---

## 11. Provenance
- **Source files:** day‑level procurement CSV; QSI rupture tickets CSV.  
- **Computation:** direct from source; losses booked only on days with `Drift > Θ`.  
- **Run settings:** Normal profile as stated; Policy profile applied only within defined windows.

---

## 12. Conclusion
Preventable loss is concentrated in a small number of **policy‑sensitive spike days**. A **quiet baseline** (Θ = 98) combined with a **windowed Policy profile** delivers measurable cost control with limited operational load and a direct, transparent contribution to **EBITDA**.

