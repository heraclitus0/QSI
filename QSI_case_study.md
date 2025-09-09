# QSI: Quantifying and Reducing Operational Drift in a Restaurant Supply Chain
*Hyderabad franchise network · May–June 2025 (61 operational days)*

---

## Executive Summary — Answer First
QSI converts day‑level procurement noise into **priced, stoppable events**. In this 61-day field deployment, QSI surfaced **₹31,009** of **preventable loss**, concentrated in **7 rupture days (11.5%)**. Average daily spend was **₹46,957** (total **₹2,864,379.50**), so leakage equals **1.0826% of spend**. The distribution is **heavy‑tailed**: fix a few **spike days**; leave normal operations untouched.

**Do now:** keep **Base Θ = 98** in normal weeks; in policy windows run the **Policy profile** (Θ **83–85**, cooldown **10**, ₹ floor **3,000**) and execute the 5‑step rupture SOP.

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
- **Leakage as % of spend:** **1.0826%**  
- **Rupture days:** **7** (all loss concentrated here; **11.5%** of days)  
- **Drift distribution:** mean **32.30**, σ **36.53**, P50 **10**, P75 **50**, P90 **100**, max **120**  
- **MAPE:** **3.52%**

**Clustering & policy effect**  
- Ruptures are **short, sharp shocks** (1–2 days).  
- Policy shifts the distribution **2–3× right** *(non‑policy → policy: median **10 → 50**, P75 **30 → 80**, mean **21.0 → 53.8**).*  
- **Loss concentration:** **100%** of loss occurs on **7/61** days—stronger than simple 80/20.

---

## 5) Evidence Exhibits (selected)
- **Policy vs Non‑Policy (ECDF):** `graphs/ecdf_policy_vs_nonpolicy_clean.png` — full‑distribution shift; policy weeks are risk‑dense.  
- **Policy vs Non‑Policy (Violin):** `graphs/violin_policy_vs_nonpolicy_clean.png` — heavier tails in policy weeks.  
- **Weekday vs Weekend (ECDF):** `graphs/ecdf_weekday_vs_weekend_clean.png` — this run: weekdays have higher central drift.  
- **Loss concentration (Lorenz):** `graphs/lorenz_loss_concentration_clean.png` — all loss in 7/61 days.  
- **Rupture tickets (₹):** `graphs/bar_rupture_losses_clean.png` — typical ticket **₹4.6k–₹5.6k**; total **₹31,009**.  
- **Rupture timeline (UI):** `graphs/rupre_plot.png` — short, high‑amplitude spikes against Θ=98.

*Bullwhip context (proxy):* policy amplification via variance/CV ratios — `graphs/bullwhip_proxy_rolling_var_ratio.png`, `graphs/bullwhip_proxy_segment_ratios.png`. *(True bullwhip needs upstream order/inventory traces.)*

---

## 6) Policy Profile — UI‑Native (no code)
**Intent:** In government‑distorted weeks, switch to a **tighter detection profile** to capture the expensive middle of the policy distribution, then **auto‑restore** to Normal.

### Control sheet (matches the UI)
| UI control | **Normal** | **Policy** | Why | Owner |
|---|---:|---:|---|---|
| **Threshold (Θ)** | **98** | **83–85** | Policy shifts drift **2–3× right**; ~15% dip catches ₹‑material spikes. | Ops Lead |
| **Cooldown** | **20** | **10** | Allow back‑to‑back spikes in distorted weeks. | Ops Lead |
| **Probability shaping** | mid **0.0**, slope **b=6.0** | mid **0.5** *or* **b=4–5** | Avoid near‑threshold saturation ≈1.0. | Analytics |
| **₹ Loss floor (toggle)** | **Off** | **On @ ₹3,000** | Catch medium drift that’s ₹‑material. | Finance |
| **Alert budget** | n/a | **≤5/week** | Capacity guardrail, preserves signal quality. | Ops Lead |
| **Auto‑restore** | n/a | **+2 days** after policy end | Prevent lingering “policy mode.” | Analytics |

### Activation (rules, not scripts)
- **Primary:** switch to **Policy** profile on **pre‑announced** ration/MSP/bonus/festival windows.  
- **Secondary (optional):** if **mandi price** jumps **>5% d/d** *and* ECDF median lifts, run Policy for **7–14 days**.  
- **Deactivation:** end of window **+2 days**, then restore to **Normal**.

### Guardrails
- **Min sensitivity:** Policy Θ must not drop below the **80th percentile** of policy‑week drift (prevents alert floods).  
- **Budget backstop:** if **>5 alerts/week**, raise Θ by **+2** points or increase the ₹ floor to **₹3,500**.  
- **Strategic buys:** tag and **exclude from vendor penalties**; keep for finance traceability.

### Operator checklist (60‑second routine)
On breach → **call vendor → split order → shift purchase window → defer 1 day if buffer ≥1 day → tag cause** *(policy/vendor/demand/strategic)*.

**What this buys you (your run):** Normal Θ=98 captured **₹31,009** over **7 days**. In policy weeks, Policy profile adds **≈3** high‑value alerts and **≈₹10,517** extra addressable leakage over 61 days, without exceeding the alert budget.

---

## 7) EBITDA Lens (per outlet, annualized)
- **Leakage rate:** **1.0826%** of spend.  
- **Baseline at risk:** **₹185,546/year**.  
- **50% reduction (Policy profile + SOP):** **₹92,773/year** EBITDA uplift.  
- **60% reduction:** **₹111,327/year** EBITDA uplift.  
- **Per ₹1 crore at 1.0826% leakage:** **₹54,129–₹64,954** uplift for **50–60%** reduction.

---

## 8) Risks & Neutralizers
- **Alert fatigue:** min‑percentile guardrail, weekly budget, auto‑restore.  
- **False “policy” flags:** calendar confirmation or two‑signal rule (price + ECDF).  
- **Over‑steer in normal weeks:** Normal profile stays **Θ=98**; no change outside policy.  
- **Data anomalies / strategic buys:** rupture tickets are line‑item auditable; tag strategic and exclude from penalties.

---

## 9) Conclusion
QSI exposes **~1.08%** spend leakage that concentrates in a few **policy‑sensitive spike days**. Keep **Normal** profile quiet at **Θ=98**; switch to the **Policy** profile only during distortion windows. Expect **~0.54–0.65%** EBITDA defense at **50–60%** reduction, with minimal operational load.

---

## Appendix — Data, Definitions, Provenance
- **Data files:** `hyderabad_saffron_rice_supply_may_june (1).csv`, `qsi_results (3).csv`, `rupture_tickets_table.csv`  
- **Definitions:** Drift = `|Forecast − Actual|`; Loss = `Drift × Unit_Cost` when **drift > Θ**; Policy window = **May 10–30**.  
- **Run settings (Normal profile):** Θ=98, α=0.02, c=0.25, σ=5, vol=7d; ε=0.10, promote=1.02, cooldown=20, prob‑slope=6.0; Scope=1.00, PSI=7.99.
