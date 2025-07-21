# Code Logic Document: Rupture Detector System

## 1. System Overview

The Rupture Detector is designed to identify significant deviations between **Forecast** and **Actual** operational data streams. It quantifies preventable losses by applying **adaptive thresholding** and **volatility-based statistical controls**. The tool is structured around:

- **Adaptive Memory-Driven Rupture Detection** (Theta-based),
- **Volatility Smoothing via EWMA Thresholding**,
- **Financial Impact Quantification** linked to drift events.

---

## 2. Pipeline Flow Structure

**Data Flow:**

```
[Input CSV] → [Delta Calculation] → [Drift Memory Calculation] → [Adaptive Thresholding] → [Rupture Classification] → [Loss Calculation] → [EWMA Smoothing] → [Exportable Outputs]
```

**Modules Used:**

- Dummy data generation.
- Core rupture detection engine.
- Statistical smoothing layer.

---

## 3. Module-by-Module Breakdown

### 3.1 `generate_dummy()`

- **Purpose**: Create synthetic datasets simulating Forecast vs Actual drift.
- **Key Mechanics**:
  - Forecast: Normally distributed around 1000 ± 100.
  - Actual: Perturbed from forecast by normal noise ±150.
  - Output Columns: `Date`, `Forecast`, `Actual`, `Unit_Cost` (constant).

---

### 3.2 `compute_drift_thresholds()`

- **Purpose**: Apply adaptive drift memory logic to classify ruptures.
- **Mathematical Flow**:
  - **Delta (|F - A|)**: Core deviation metric.
  - **Drift Memory E(t)**: `E(t) = c * drift + E(t-1)` (decay memory accumulation).
  - **Adaptive Threshold Θ(t)**: `Θ(t) = base_threshold + a * E(t) + ε`, where ε \~ N(0, σ).
  - **Rupture Trigger**: If `Delta > Θ(t)`, rupture = True, drift memory reset.
  - **Loss**: Only accumulated when rupture triggers → `Loss = Delta * Unit_Cost`.
- **Key Parameters**:
  - `c`: Drift memory scaling factor.
  - `a`: Sensitivity of threshold to accumulated drift.
  - `base_threshold`: Minimum tolerance before accounting for drift memory.
  - `sigma`: Noise term injecting stochasticity.

---

### 3.3 `compute_ewma_threshold()`

- **Purpose**: Calculate Exponential Weighted Moving Average (EWMA) threshold for volatility reference.
- **Mathematical Flow**:
  - **EWMA Mean (μ)**: Recent drift weighted more heavily.
  - **EWMA Std (σ)**: Smoothed standard deviation.
  - **Threshold\_EWMA**: `μ + k * σ` → purely statistical threshold, **not tied to rupture triggering**.
- **Parameters**:
  - `alpha`: Smoothing constant (0 < α ≤ 1).
  - `k`: Standard deviation multiplier.

---

## 4. Data Output Logic

| Column          | Description                                            |
| --------------- | ------------------------------------------------------ |
| Delta           | Absolute daily forecast error.                         |
| DriftMemory     | Cumulative misalignment memory.                        |
| Threshold       | Dynamic rupture threshold (Theta).                     |
| Rupture         | Binary rupture flag (True/False).                      |
| Loss            | Financial loss incurred during ruptures.               |
| Threshold\_EWMA | Reference-only threshold for volatility visualization. |

---

## 5. Economic Logic Explanation

- **Loss Accumulation Rule**: Only deltas surpassing the **Theta threshold** trigger recorded loss.
- **EWMA**: Does **not influence financial calculations**; serves as secondary volatility lens.
- **Total Preventable Loss** = Σ (Delta \* Unit\_Cost) for all days where rupture = True.

---

## 6. Known Limitations

- EWMA thresholds may remain inactive in low-variance environments.
- Current system lacks positive vs negative drift separation.
- No rolling window drift aggregation (e.g., 3-day rolling ruptures).

---

## 7. Planned Expansion

- **Dual-rupture detection (Theta OR EWMA rupture trigger)**.
- **Rolling rupture detection logic** (e.g., cumulative drift rupture triggers).
- **API-ready microservice restructuring**.
- **Multi-sector config presets (Agri, Retail, Energy)**.

---

## 8. Reference Equations (Summary)

```
Delta(t) = |Forecast - Actual|
E(t) = E(t-1) + c * Delta(t) [Reset to 0 if rupture triggered]
Θ(t) = base_threshold + a * E(t) + ε
Rupture = True if Delta(t) > Θ(t)
Loss = Delta * Unit_Cost when Rupture = True
EWMA Threshold = μ + k * σ
```

---

**End of Logic Document**

