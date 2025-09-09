# Case Study — QSI: Quantifying and Reducing Operational Drift in a Restaurant Supply Chain
*Hyderabad franchise network · May–June 2025 (61 operational days)*

---

## Executive Summary — Answer First
QSI converts day‑level procurement noise into **priced, stoppable events**. In this 61‑day field deployment, QSI surfaced **₹31,009** of **preventable loss**, concentrated in **7 rupture days (11.5%)**. Average daily spend was **₹46,957** (total **₹2,864,379.50**), so leakage equates to **1.0826% of spend**. The distribution is **heavy‑tailed**: addressing a small number of **spike days** delivers most of the value while leaving normal operations untouched.

**What to do:** keep **Base Θ = 98** in normal weeks; during policy windows, use **Θ_policy ≈ 0.85× (≈ 83–85)** and run a short SOP on breach (call vendor → split order → shift window → defer 1 day if buffer ≥ 1 day → tag cause).

---

## 1) Situation · Complication · Objective
- **Situation:** Franchise procurement faces daily variability; government ration/bonus activity periodically distorts local markets.
- **Complication:** Leakage hides in **punctuated spikes** that monthly averages conceal; operators lack day‑level ₹ accountability.
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
**Loss model:** `loss = |Forecast − Actual| × Unit_Cost`, **only on rupture days** (`drift > Θ`).

---

## 3) QSI Method (how it works)
- **Adaptive threshold Θ:** learned limit informed by misalignment memory **E** and noise **σ**.  
- **Trigger rule:** raise an event only when `drift > Θ`.  
- **Loss pricing:** book ₹ **only** on triggers—no penalties on normal days (minimizes false positives).  
- **Policy aware:** allow a temporary **Θ dip** in defined policy windows to catch economically material spikes.

Run snapshot: **Θ = 98**, **α = 0.02**, **c = 0.25**, **σ = 5**, **vol = 7d**; **ε = 0.10**, **cooldown = 20**, **prob‑slope b = 6.0**.

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
- Ruptures occur as **short, sharp shocks** (1–2 days).  
- Policy window shifts the distribution **2–3× to the right** *(non‑policy → policy: median **10 → 50**, P75 **30 → 80**, mean **21.0 → 53.8**).*  
- **Loss concentration:** **100%** of loss occurred on **7 of 61 days**—stronger than a simple 80/20 pattern.

---

## 5) Evidence Exhibits (selected)
- **Policy vs Non‑Policy (ECDF):** `graphs/ecdf_policy_vs_nonpolicy_clean.png` — full‑distribution shift; policy weeks are risk‑dense.  
- **Policy vs Non‑Policy (Violin):** `graphs/violin_policy_vs_nonpolicy_clean.png` — heavier tails in policy weeks.  
- **Weekday vs Weekend (ECDF):** `graphs/ecdf_weekday_vs_weekend_clean.png` — this run: weekdays show higher central drift.  
- **Loss concentration (Lorenz):** `graphs/lorenz_loss_concentration_clean.png` — all loss in 7/61 days.  
- **Rupture‑day tickets (₹):** `graphs/bar_rupture_losses_clean.png` — typical ticket **₹4.6k–₹5.6k**; total **₹31,009**.  
- **Rupture timeline (UI):** `graphs/rupre_plot.png` — short, high‑amplitude spikes against Θ = 98.

*Bullwhip context (proxy):* policy‑period amplification illustrated via variance ratios —  
`graphs/bullwhip_proxy_rolling_var_ratio.png`, `graphs/bullwhip_proxy_segment_ratios.png`.  
(*Note:* full bullwhip proof needs upstream order/inventory traces.)

---

## 6) Policy Θ Hook — what it is, why it matters, how we use it
**Action:** During government‑driven distortion weeks, **temporarily lower Θ by ~15%** to catch the profitable middle of the policy distribution—then **auto‑restore** to baseline.

**Definition**  
```
Θ_t = max( Q_policy(0.80), 0.85 × Θ_base )   if t ∈ policy_window
      Θ_base                                  otherwise
```
With **Θ_base = 98** (normal weeks). The `Q_policy(0.80)` guardrail prevents alert floods.

**Why (your data):** policy weeks shift drift **2–3× right**. Sensitivity: **Θ=98 → ₹40,162** potential (8 days) vs **Θ=80 → ₹50,679** (11 days) → **≈ ₹10,517** extra addressable from **~3** added alerts over 61 days. A **~15% dip (≈ 83–85)** captures most of that upside without flooding ops.

**Where it lives:** detection/threshold step (pre‑probability). Keep EWMA unchanged.

**How to run it (config):**  
```yaml
qsi:
  theta:
    base: 98
    policy_multiplier: 0.85          # Θ_policy ≈ 83–85
    policy_min_quantile: 0.80        # guardrail: Θ_policy ≥ 80th pct (policy days)
  meta:
    cooldown:
      base: 20
      policy: 10                     # allow back‑to‑back spikes
  economics:
    loss_floor_inr: 3000             # parallel ₹ trigger: drift×cost ≥ 3,000
  governance:
    alert_budget_per_week: 5         # cap in policy weeks
    auto_restore_after_policy_days: 2
```

**Operator playbook (policy window):** on breach → **call vendor → split order → shift purchase window → defer 1 day if buffer ≥ 1 day → tag cause** *(policy/vendor/demand/strategic)*. Keep **alerts ≤ 5/week**; if exceeded, raise **Θ_policy by +2** or increase the **₹ floor** (e.g., 3,000 → 3,500).

**Implications:** a few **extra high‑value alerts** only when markets distort; quiet in normal weeks. Every ₹ prevented flows **1:1 to EBITDA**. Rupture tickets (date, drift, Θ, ₹) provide line‑item traceability.

---

## 7) Strategic Implications
1. **Target the spikes, not the baseline:** act only on rupture days to avoid over‑steering.  
2. **Price the risk and govern it:** integrate rupture tickets into **vendor scorecards** (breach frequency × ₹ loss).  
3. **Policy‑aware tightening:** keep **Base Θ = 98**; during policy windows use **Θ_policy ≈ 0.85× (≈ 83–85)** with **cooldown 20 → 10**.  
4. **Economic floor:** add a parallel trigger `drift × Unit_Cost ≥ ₹3,000` to catch medium‑drift, high‑₹ days.  
5. **Minimal disruption:** no penalties on normal days; detection stays quiet outside of true spikes.

---

## 8) EBITDA Lens (per outlet, annualized)
- **Baseline leakage:** **₹185,546/year** (annualized from this run; leakage rate **1.0826%**).  
- **50% reduction (policy Θ dip + SOP):** **~₹92,773/year EBITDA uplift**.  
- **60% reduction:** **~₹111,327/year EBITDA uplift**.  
- **Rule of thumb:** per **₹1 crore** addressable spend at **1.0826% leakage**, EBITDA uplift ≈ **54,129–64,954** for **50–60%** reduction.

---

## 9) Conclusion
QSI turns day‑level misalignment into **actionable, priced exceptions**. In this Hyderabad deployment it uncovered **₹31,009** of preventable leakage across **7 spike days**, or **1.0826%** of spend. A **policy‑aware Θ hook** captures additional value precisely when markets distort—without burdening normal operations.

---

## Appendix — Data, Definitions, Provenance
- **Data files:** `hyderabad_saffron_rice_supply_may_june (1).csv`, `qsi_results (3).csv`, `rupture_tickets_table.csv`  
- **Definitions:** Drift = `|Forecast − Actual|`; Loss = `Drift × Unit_Cost` when **drift > Θ**; Policy window = **May 10–30**.  
- **Run settings:** Θ = 98, α = 0.02, c = 0.25, σ = 5, vol = 7d; ε = 0.10, promote = 1.02, cooldown = 20, prob‑slope = 6.0; Scope = 1.00, PSI = 7.99.
