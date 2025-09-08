from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict, Any
import numpy as np
import pandas as pd

@dataclass
class EpistemicConfig:
    baseline_mode: str = "window"         # "window" | "file"
    baseline_window: int = 30
    baseline_file: Optional[str] = None
    scope_q_lo: float = 0.05
    scope_q_hi: float = 0.95
    psi_bins: int = 10
    expiry_k: int = 3
    expiry_lookback: int = 28
    min_points_for_trend: int = 10

class EpistemicAnalytics:
    @staticmethod
    def _load_baseline(df_out: pd.DataFrame, cfg: EpistemicConfig) -> pd.Series:
        if cfg.baseline_mode == "file" and cfg.baseline_file:
            base = pd.read_csv(cfg.baseline_file)
            for k in ("drift","Delta"):
                if k in base.columns: return base[k].astype(float)
            raise ValueError("Baseline file must include 'drift' or 'Delta'.")
        n = min(cfg.baseline_window, len(df_out))
        return df_out["drift"].iloc[:n].astype(float)

    @staticmethod
    def _psi(actual: pd.Series, expected: pd.Series, bins: int = 10) -> float:
        q = np.linspace(0.0, 1.0, bins + 1)
        cuts = np.unique(np.quantile(expected, q))
        if len(cuts) < 3: return 0.0
        e_hist, _ = np.histogram(expected, bins=cuts)
        a_hist, _ = np.histogram(actual,   bins=cuts)
        e_pct = np.maximum(e_hist / max(e_hist.sum(), 1), 1e-6)
        a_pct = np.maximum(a_hist / max(a_hist.sum(), 1), 1e-6)
        return float(np.sum((a_pct - e_pct) * np.log(a_pct / e_pct)))

    @staticmethod
    def _scope_score(actual: pd.Series, baseline: pd.Series, lo: float, hi: float) -> float:
        L, H = np.quantile(baseline, lo), np.quantile(baseline, hi)
        return float(((actual >= L) & (actual <= H)).mean())

    @staticmethod
    def _eta_to_breach(margin: pd.Series, k: int, lookback: int, min_points: int) -> Optional[int]:
        m = margin.dropna()
        if len(m) < min_points: return None
        m = m.iloc[-lookback:] if len(m) > lookback else m
        x = np.arange(len(m), dtype=float); y = m.to_numpy(float)
        b1, b0 = np.polyfit(x, y, deg=1)   # slope, intercept
        if (m > 0).tail(k).all(): return 0
        start = len(m)
        for t in range(start, start + 365):
            if all(b0 + b1 * (t + j) > 0 for j in range(k)): return t - start
        return None

    @staticmethod
    def enrich(df_out: pd.DataFrame, cfg: EpistemicConfig) -> Dict[str, Any]:
        eps = 1e-9
        pct_err = (df_out["drift"] / (df_out["Actual"].abs() + eps)).replace([np.inf, -np.inf], np.nan).fillna(0.0)
        on_target = pct_err <= 0.05
        over = (df_out["Forecast"] > df_out["Actual"]) & ~on_target
        under = (df_out["Forecast"] < df_out["Actual"]) & ~on_target
        severe = pct_err >= 0.20

        econ = {
            "total_loss": float(df_out["loss"].sum()),
            "loss_per_unit_mean": float((df_out["loss"] / (df_out["Actual"].abs() + eps)).replace([np.inf, -np.inf], np.nan).fillna(0.0).mean()),
            "overforecast_count": int(over.sum()),
            "underforecast_count": int(under.sum()),
            "on_target_count": int(on_target.sum()),
            "severe_miss_count": int(severe.sum()),
            "severe_miss_rate": float(severe.mean()),
        }

        baseline = EpistemicAnalytics._load_baseline(df_out, cfg)
        recent = df_out["drift"].iloc[-max(len(baseline), 1):]
        scope = EpistemicAnalytics._scope_score(recent, baseline, cfg.scope_q_lo, cfg.scope_q_hi)
        psi = EpistemicAnalytics._psi(recent, baseline, cfg.psi_bins)

        margin = (df_out["drift"] - df_out["Theta"]).astype(float)
        eta_days = EpistemicAnalytics._eta_to_breach(margin, cfg.expiry_k, cfg.expiry_lookback, cfg.min_points_for_trend)
        expiry_date = None
        if eta_days is not None:
            expiry_date = str((pd.Timestamp.today().normalize() + pd.Timedelta(days=int(eta_days))).date())

        epistemic = {
            "scope_score_0to1": float(scope),
            "psi": float(psi),
            "eta_days_to_persistent_breach": (None if eta_days is None else int(eta_days)),
            "expiry_estimate_date": expiry_date,
        }
        return {"economics": econ, "epistemic": epistemic}
