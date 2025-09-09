# Case Study — QSI in the Wild
*Hyderabad franchise network · Restaurant supply chain · May–June 2025 (61 operational days)*

> **What this is:** a case narrative—**how** QSI was set up, **what changed operationally**, and **what we’d do differently**.  
> **What this is not:** a reprint of the full analytics. (Those exhibits live in the report.)

---

## 1) Executive Snapshot (one paragraph)
QSI was deployed to turn day‑level procurement noise into **priced, stoppable events**. Over 61 days it identified **seven rupture days** that explained **all preventable loss** (₹31,009; ~1.08% of spend). Normal weeks stayed quiet on **Θ=98**; during policy weeks, a **tighter profile** (Θ ~83–85, cooldown 10, ₹ floor 3,000) captured additional high‑value spikes **without flooding** operators. The value came not from “more alerts,” but from **clarity and discipline** around what to do **only** on spike days.

---

## 2) Case Background & Hypothesis
- **Context:** Franchise‑level procurement of Sona Masoori rice; periodic **policy shocks** (ration/bonus) distort local prices and availability.  
- **Known failure:** Monthly view hides leakage; ERP forecasts are **too smooth** for day‑level action.  
- **Hypothesis:** Loss is **heavy‑tailed** (a few spike days). If we price only **true ruptures** (drift > Θ) and execute a short SOP, we reduce leakage materially **without** burdening normal days.

---

## 3) Design & Setup (two days)
**Unit of analysis:** calendar day per outlet.  
**Signal:** drift = |Forecast − Actual|. **Price:** loss = drift × unit cost (only when drift > Θ).  
**Profiles:**  
- **Normal:** Θ=98, cooldown 20, prob slope b=6.0 (quiet, high SNR).  
- **Policy:** Θ≈83–85 (−15%), cooldown 10, ₹ floor 3,000 (surgical, time‑boxed).  
**Governance:** alert budget ≤5/week (policy); auto‑restore to Normal +2 days post‑policy.  
**Data:** CSV ingestion; no imputation; day‑level tickets generated for audit.

---

## 4) Intervention (what actually changed on the ground)
- **Before:** operators reacted variably; vendor calls and order splits were **ad‑hoc**.  
- **After:** a **breach ticket** triggered a 5‑step SOP:  
  1) Call vendor (check price & capacity)  
  2) Split order (primary/secondary)  
  3) Shift purchase window (intra‑day/time‑of‑day)  
  4) Defer 1 day if stock buffer ≥1 day  
  5) Tag root cause *(policy/vendor/demand/strategic)*  
- **Vendor scorecards** were built from rupture tickets (breach × ₹ loss) → **rate/volume reallocation** discussions moved from opinion to ledger.

---

## 5) What Happened (narrative, not charts)
- **Normal weeks:** QSI remained **quiet**; no alert fatigue. Θ=98 proved **well‑placed**—noise ignored, tails caught.  
- **Policy weeks:** the distribution **shifted right**; switching to the Policy profile produced **a handful of extra alerts**, each economically meaningful (₹‑material via floor).  
- **Clustering:** all preventable loss sat on **7 of 61 days**; spikes were **short and sharp** (1–2 days).  
- **Operator load:** contained within the **≤5/week** budget; no service disruption.

---

## 6) Decision Log (anonymized pattern, R1–R7)
- **R1–R2:** Vendor price check + split order → realized unit cost improvement next day.  
- **R3:** Shifted purchase window; avoided late‑day premium.  
- **R4–R5:** Deferred one day on buffer; avoided policy‑driven overpay.  
- **R6:** Strategic buy tagged; **excluded** from vendor penalty but kept for finance.  
- **R7:** Policy‑week doublet; cooldown 10 allowed back‑to‑back action.  
**Ticket economics:** typical **₹4.6k–₹5.6k** each; total **₹31,009** across the seven.

---

## 7) Economics (how finance read it)
- **Leakage rate (from tickets):** ~**1.0826% of spend**.  
- **EBITDA mapping:** every ₹ saved is **cost‑out** → **1:1 to EBITDA**.  
- **Program effect:** a realistic **50–60% reduction** yields **~0.54–0.65%** EBITDA defense.  
- **Per ₹1 crore spend:** **₹54k–₹65k** uplift at 50–60% reduction.

---

## 8) What Worked / What Didn’t
**Worked**  
- Quiet baseline; **no** operator fatigue.  
- **Policy profile** captured the “expensive middle” without drowning the team.  
- **Tickets** changed the vendor conversation (from anecdotes to numbers).

**Didn’t / Frictions**  
- Some **strategic buys** initially flagged as loss → solved with tags and exclusions for penalties.  
- **After‑policy lag** risk → fixed with **auto‑restore +2 days**.  
- **Bullwhip proof** limited by single‑tier data (we used a proxy; plan multi‑tier capture).

---

## 9) External Validity & Transfer
- **Where it ports well:** commodities with **policy cadence** (staples, fuel‑indexed inputs), retail replenishment, logistics day‑slots.  
- **Pre‑conditions:** day‑level records; a secondary supplier; minimal stock buffer (≥1 day) to enable deferral.  
- **Watch‑outs:** single‑source vendors, festival surges, and sudden supplier stockouts (use the ₹ floor trigger).

---

## 10) Replication Protocol (7‑day rollout)
**Day 0:** Load CSV; confirm Θ=98; define policy dates.  
**Day 1–2:** Shadow run; log would‑have alerts; set **alert budget ≤5/week**.  
**Day 3:** Go live; activate tickets; brief SOP to outlet managers.  
**Day 4–5:** Audit two tickets end‑to‑end; verify vendor actions & prices.  
**Day 6:** Review budget; if >5/week, raise Θ by +2 or ₹ floor to ₹3,500.  
**Day 7:** Confirm auto‑restore logic and policy calendar for next month.

---

## 11) Risk Register & Neutralizers
- **Alert fatigue** → guardrail (policy Θ ≥ policy‑week 80th percentile) + weekly budget + auto‑restore.  
- **False policy windows** → require calendar confirmation **or** two‑signal trigger (price jump + ECDF shift).  
- **Mis‑scoring strategic buys** → mandatory tag; excluded from vendor penalties.  
- **Data anomalies** → tickets retain raw quantities, costs, and timestamps for audit.

---

## 12) What We’d Change Next Run
1) Add **supplier‑side orders/inventory** to evidence true bullwhip and negotiate rate protections.  
2) Trial **weekday lane adjustments** (this run showed weekday‑heavy central drift).  
3) Pilot **probability mid 0.5** in policy weeks to prevent near‑threshold saturation.

---

## 13) Provenance (for audit)
- **Source files:** day‑level procurement CSV; QSI rupture tickets CSV.  
- **Computation:** direct from source; no imputation; losses priced only on **drift > Θ**.  
- **Settings used:** Normal Θ=98; Policy profile Θ≈83–85, cooldown 10, ₹ floor 3,000; alert budget ≤5/week; auto‑restore +2 days.

---

**Bottom line:** This case confirms the operating thesis—**a few policy‑sensitive spike days cause nearly all leakage**. QSI’s discipline is to **be quiet by default** and **surgical on those days**, converting noise into **priced decisions** that flow directly to **EBITDA**.
