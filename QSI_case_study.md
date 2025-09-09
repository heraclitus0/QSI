# QSI: Quantifying and Reducing Operational Drift in a Restaurant Supply Chain
*Hyderabad franchise network · May–June 2025 (61 operational days)*

---

## Executive Summary — Answer First
QSI converts day‑level procurement noise into **priced, stoppable events**. In this 61-day deployment, QSI surfaced **₹31,009** of **preventable loss**, concentrated in **7 rupture days (11.5%)**. Average daily spend was **₹46,957** (total **₹2,864,379.50**), so leakage equals **1.0826% of spend**. The distribution is **heavy‑tailed**: fix a few **spike days**; leave normal operations untouched.

**Do now:** keep **Base Θ = 98** in normal weeks; in policy windows run the **Policy profile** (Θ **83–85**, cooldown **10**, ₹ floor **3,000**) and execute the five‑step rupture SOP.

---

## 1) Situation · Complication · Objective
- **Situation:** Daily volatility plus periodic government interventions (ration/bonus) distort the local rice market.  
- **Complication:** Leakage hides in **punctuated spikes** that monthly averages and ERPs smooth away; managers lack day‑level ₹ accountability.  
- **Objective:** **Detect and price day‑level drift**, alert only on **true rupture** (drift > Θ), and quantify **₹ loss** per event to trigger action.

---

## 2) Deployment & Data
| Parameter | Value |
|---|---|
| Commodity | Sona Masoori rice (25 kg unit bags) |
| Location | Hyderabad (franchise‑level procurement) |
| Period | May–June 2025 (**61 days**) |
| Policy window (calibration) | **May 10–30** |
| Data fields | Date, Forecast, Actual, Unit_Cost |
| Stack | CSV backend → QSI engine → lightweight UI |

**Spend model:** `daily_spend = Actual × Unit_Cost`  
**Loss model:** `loss = |Forecast − Actual| × Unit_Cost` **only on rupture days** (`drift > Θ`).

---

## 3) QSI Method (how it works)
- **Adaptive threshold (Θ):** learned from misalignment memory **E** and noise **σ**.  
- **Trigger:** raise an event only when `drift > Θ`.  
- **Pricing:** book ₹ **only** on triggers—no penalties on normal days (minimizes false positives).  
- **Policy‑aware:** switch to a tighter **Policy profile** in defined windows to capture economically material spikes.

Run snapshot (Normal profile): **Θ=98**, **α=0.02**, **c=0.25**, **σ=5**, **vol=7d**; **ε=0.10**, **cooldown=20**, **prob‑slope b=6.0**.

---

## 4) Results & Operational Findings
**Key metrics (validated)**  
- **Preventable loss:** **₹31,009**  
- **Avg daily spend:** **₹46,957** (total **₹2,864,379.50**)  
- **Leakage:** **1.0826%** of spend  
- **Rupture days:** **7** (all loss concentrated here; **11.5%** of days)  
- **Drift distribution:** mean **32.30**, σ **36.53**, P50 **10**, P75 **50**, P90 **100**, max **120**  

**Clustering & policy effect**  
- Ruptures are **short, sharp shocks** (1–2 days).  
- Policy shifts the distribution **2–3× right** *(non‑policy → policy: median **10 → 50**, P75 **30 → 80**, mean **21.0 → 53.8**).*  
- **Loss concentration:** **100%** of loss occurs on **7/61** days—stronger than simple 80/20.

---

## 5) Evidence Exhibits (described, no attachments)
**Exhibit A — ECDF (Policy vs Non‑Policy)**  
*Read:* the policy ECDF sits to the **right** at all quantiles → higher drift everywhere.  
*Implication:* pre‑schedule the **Policy profile** for announced windows.

**Exhibit B — Violin (Policy vs Non‑Policy)**  
*Read:* thicker body and longer tails under policy.  
*Implication:* expect **short, sharp spikes**; reduce **cooldown 20 → 10** in policy weeks.

**Exhibit C — ECDF (Weekday vs Weekend)**  
*Read:* this run shows **weekdays** with higher central drift.  
*Implication:* bias staffing and lanes to weekday resilience; **re‑check quarterly**.

**Exhibit D — Lorenz (Loss concentration)**  
*Read:* strong bow; **all loss** in **7 of 61** days.  
*Implication:* optimize for **precision**—focus only on spike days.

**Exhibit E — Rupture ticket sizes**  
*Read:* typical ticket **₹4.6k–₹5.6k**; total **₹31,009**.  
*Implication:* use tickets for operator debriefs, vendor negotiations, and finance accruals.

**Context Exhibit — Bullwhip proxy (optional)**  
*Read:* variance and CoV ratios rise in policy weeks—consistent with amplification.  
*Caveat:* full bullwhip proof needs upstream order/inventory traces.

---

## 6) Policy Profile — UI‑Native (no code)
**Intent:** in government‑distorted weeks, switch to a **tighter detection profile** to capture the expensive middle of the distribution, then **auto‑restore**.

**Control sheet (matches the UI)**  
- **Threshold (Θ):** **98** → **83–85** in policy weeks (≈15% dip)  
- **Cooldown:** **20** → **10** in policy weeks  
- **Probability shaping:** mid **0.0**, slope **b=6.0** → mid **0.5** or **b=4–5** in policy weeks  
- **₹ Loss floor (toggle):** **On @ ₹3,000** in policy weeks  
- **Alert budget:** **≤5/week** in policy weeks  
- **Auto‑restore:** back to Normal **+2 days** after policy end

**Activation (rules, not scripts)**  
- **Primary:** switch on pre‑announced ration/MSP/bonus/festival windows.  
- **Secondary (optional):** if mandi price rises **>5% d/d** and ECDF median lifts, run Policy for **7–14 days**.  
- **Deactivation:** end of window **+2 days**, then restore to Normal.

**Guardrails**  
- **Minimum sensitivity:** do not set Policy Θ below the **80th percentile** of policy‑week drift.  
- **Budget backstop:** if **>5 alerts/week**, raise Θ by **+2** or increase the ₹ floor (e.g., **₹3,500**).  
- **Strategic buys:** tag and **exclude from vendor penalties**; keep for finance traceability.

**Operator checklist (60 seconds)**  
On breach → **call vendor → split order → shift purchase window → defer 1 day if buffer ≥1 day → tag cause (policy/vendor/demand/strategic)**.

---

## 7) EBITDA Lens (per outlet, annualized)
- **Leakage rate:** **1.0826%** of spend.  
- **Baseline at risk:** **₹185,546/year**.  
- **50–60% reduction (Policy profile + SOP):** **₹92,773–₹111,327/year** EBITDA uplift.  
- **Per ₹1 crore at 1.0826% leakage:** **₹54,129–₹64,954** uplift for **50–60%** reduction.

---

## 8) Risks & Neutralizers
- **Alert fatigue:** min‑percentile guardrail, weekly budget, auto‑restore.  
- **False “policy” flags:** calendar confirmation or two‑signal rule (price + ECDF).  
- **Over‑steer in normal weeks:** Normal profile stays **Θ=98**; no change outside policy.  
- **Data anomalies / strategic buys:** rupture tickets are line‑item auditable; tag strategic and exclude from penalties.

---

## 9) Conclusion
QSI exposes **~1.08%** spend leakage concentrated in a few **policy‑sensitive spike days**. Keep the system quiet at **Θ=98**; switch to the **Policy profile** only during distortion windows. Expect **~0.54–0.65%** EBITDA defense at **50–60%** reduction, with minimal operational load.

---

## Appendix — Data, Definitions, Provenance
- **Data files:** hyderabad_saffron_rice_supply_may_june (1).csv; qsi_results (3).csv; rupture_tickets_table.csv  
- **Definitions:** Drift = `|Forecast − Actual|`; Loss = `Drift × Unit_Cost` when **drift > Θ**; Policy window = **May 10–30**.  
- **Run settings (Normal):** Θ=98, α=0.02, c=0.25, σ=5, vol=7d; ε=0.10, promote=1.02, cooldown=20, prob‑slope=6.0; Scope=1.00, PSI=7.99.
