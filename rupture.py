import pandas as pd
import numpy as np

def generate_dummy(days: int = 30, seed: int = 42, unit_cost: float = 40.0) -> pd.DataFrame:
    """Return a dummy forecast vs. actual DataFrame with unit costs."""
    rng = np.random.default_rng(seed)
    dates = pd.date_range(end=pd.Timestamp.today(), periods=days)
    forecast = rng.normal(1000, 100, days).astype(int)
    actual   = forecast - rng.normal(0, 150, days).astype(int)
    cost     = np.full(days, unit_cost)
    return pd.DataFrame({
        "Date": dates,
        "Forecast": forecast,
        "Actual": actual,
        "Unit_Cost": cost
    })

def compute_drift_thresholds(df: pd.DataFrame, c: float, a: float, base_threshold: float, noise_level: float, seed: int = 0):
    """Compute drift scores, adaptive thresholds, rupture points, and preventable loss."""
    rng = np.random.default_rng(seed)
    df = df.copy().sort_values("Date").reset_index(drop=True)
    
    drift = (df["Forecast"] - df["Actual"]).abs().to_numpy()
    accumulated_drift = np.zeros_like(drift)
    adaptive_threshold = np.zeros_like(drift)
    rupture = np.full(len(drift), False)
    loss = np.zeros_like(drift, dtype=float)
    noise = rng.normal(0, noise_level, size=len(drift))

    drift_memory = 0.0
    for i in range(len(drift)):
        threshold = base_threshold + a * drift_memory + noise[i]
        adaptive_threshold[i] = threshold
        if drift[i] > threshold:
            rupture[i] = True
            loss[i] = drift[i] * df.loc[i, "Unit_Cost"]
            drift_memory = 0.0
        else:
            drift_memory += c * drift[i]
        accumulated_drift[i] = drift_memory

    df["Delta"] = drift
    df["DriftMemory"] = accumulated_drift
    df["Threshold"] = adaptive_threshold
    df["Rupture"] = rupture
    df["Loss"] = loss

    ruptures = df[df["Rupture"]].copy()
    total_loss = loss.sum()
    return df, ruptures, total_loss

def compute_ewma_threshold(df: pd.DataFrame, alpha: float = 0.2, k: float = 3.0) -> pd.DataFrame:
    """Compute EWMA-based adaptive threshold for drift."""
    df = df.copy()
    if "Delta" not in df.columns:
        df["Delta"] = (df["Forecast"] - df["Actual"]).abs()

    ewma_mean = df["Delta"].ewm(alpha=alpha).mean()
    ewma_var  = df["Delta"].ewm(alpha=alpha).var()
    ewma_std  = np.sqrt(ewma_var.fillna(0))
    
    df["Threshold_EWMA"] = ewma_mean + k * ewma_std
    return df
