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

def compute_rcc(df: pd.DataFrame, c: float, a: float, Theta0: float, sigma: float, seed: int = 0):
    """Compute recursive drift, thresholds, rupture points, and loss."""
    rng = np.random.default_rng(seed)
    df = df.copy().sort_values("Date").reset_index(drop=True)
    
    delta = (df["Forecast"] - df["Actual"]).abs().to_numpy()
    E = np.zeros_like(delta)
    Theta = np.zeros_like(delta)
    rupture = np.full(len(delta), False)
    loss = np.zeros_like(delta, dtype=float)
    noise = rng.normal(0, sigma, size=len(delta))

    e = 0.0
    for i in range(len(delta)):
        theta = Theta0 + a * e + noise[i]
        Theta[i] = theta
        if delta[i] > theta:
            rupture[i] = True
            loss[i] = delta[i] * df.loc[i, "Unit_Cost"]
            e = 0.0
        else:
            e += c * delta[i]
        E[i] = e

    df["Delta"] = delta
    df["E(t)"] = E
    df["Theta(t)"] = Theta
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
    
    df["Theta_EWMA"] = ewma_mean + k * ewma_std
    return df
