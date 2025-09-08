from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict, Any, Tuple
import numpy as np
import pandas as pd


# ----------------------------- Config -----------------------------
@dataclass
class EpistemicConfig:
    # Baseline construction
    baseline_mode: str = "window"          # "window" | "file"
    baseline_window: int = 30              # first-N rows of series (after sort) if "window"
    baseline_file: Optional[str] = None    # CSV with 'drift' or 'Delta' column if "file"

    # Scope score quantile band (what we consider "in-scope")
    scope_q_lo: float = 0.05
    scope_q_hi: float = 0.95

    # PSI
    psi_bins: int = 10                     # requested number of bins
    psi_min_bins: int = 4                  # if fewer unique cut points, PSI -> 0.0
    psi_floor: float = 1e-6                # floor to avoid log(0)

    # Breach ETA
    expiry_k: int = 3                      # require k consecutive > 0 margins
    expiry_lookback: int = 28              # fit the margin trend on last N points
    min_points_for_trend: int = 10         # need at least this many to fit trend

    # Quality thresholds (domain friendly)
    on_target_pct: float = 0.05            # <= 5% relative error is "on–target"
    severe_pct: float = 0.20               # >= 20% relative error is "severe"

    # Recent slice to compare against baseline (default: same size as baseline)
    recent_window: Optional[int] = None    # if None, use len(baseline)

    # Optional reporting helpers
    groupby: Optional[str] = None          # segment column to summarize (if present)
    policy_col: Optional[str] = None       # boolean column; if present, emit policy/non-policy econ


# ----------------------------- Analytics -----------------------------
class EpistemicAnalytics:

    # ---------- Baseline ----------
    @staticmethod
    def _load_baseline(df_out: pd.DataFrame, cfg: EpistemicConfig) -> pd.Series:
        if cfg.baseline_mode == "file" and cfg.baseline_file:
            base = pd.read_csv(cfg.baseline_file)
            for k in ("drift", "Delta"):
                if k in base.columns:
                    s = pd.to_numeric(base[k], errors="coerce").dropna().astype(float)
                    if len(s) == 0:
                        raise ValueError("Baseline file parsed but contained no numeric drift values.")
                    return s
            raise ValueError("Baseline file must include 'drift' or 'Delta'.")
        # window mode
        n = max(1, min(int(cfg.baseline_window), len(df_out)))
        return df_out["drift"].iloc[:n].astype(float)

    # ---------- PSI ----------
    @staticmethod
    def _psi(actual: pd.Series, expected: pd.Series, bins: int, min_bins: int, floor: float) -> float:
        # Build cuts from expected quantiles; merge duplicates
        q = np.linspace(0.0, 1.0, max(2, int(bins)) + 1)
        cuts = np.unique(np.quantile(expected, q))
        if len(cuts) < max(3, min_bins):      # need at least 3 cut points to form >=2 bins
            return 0.0
        # Histograms across identical cuts
        e_hist, _ = np.histogram(expected, bins=cuts)
        a_hist, _ = np.histogram(actual,   bins=cuts)
        # Normalize with floor to avoid log(0)
        e_den = max(e_hist.sum(), 1)
        a_den = max(a_hist.sum(), 1)
        e_pct = np.maximum(e_hist / e_den, floor)
        a_pct = np.maximum(a_hist / a_den, floor)
        return float(np.sum((a_pct - e_pct) * np.log(a_pct / e_pct)))

    # ---------- Scope ----------
    @staticmethod
    def _scope_score(actual: pd.Series, baseline: pd.Series, lo: float, hi: float) -> float:
        L, H = np.quantile(baseline, lo), np.quantile(baseline, hi)
        return float(((actual >= L) & (actual <= H)).mean())

    # ---------- ETA to persistent breach ----------
    @staticmethod
    def _eta_to_breach(
        margin: pd.Series,
        k: int,
        lookback: int,
        min_points: int
    ) -> Tuple[Optional[int], str]:
        m = pd.to_numeric(margin, errors="coerce").dropna()
        if len(m) < max(1, min_points):
            return None, "insufficient_points"
        # Restrict to lookback tail
        if len(m) > lookback:
            m = m.iloc[-lookback:]
        # Linear trend
        x = np.arange(len(m), dtype=float)
        y = m.to_numpy(dtype=float)
        # Fit with simple polyfit (Theil–Sen would be nicer but adds deps)
        try:
            b1, b0 = np.polyfit(x, y, deg=1)  # slope, intercept
        except Exception:
            return None, "fit_failed"
        # If already above zero for k steps, ETA = 0
        if (m > 0).tail(k).all():
            return 0, "already_breaching"
        # Project forward until we get k consecutive > 0
        start = len(m)
        # Cap horizon to one year of steps
        for t in range(start, start + 365):
            if all((b0 + b1 * (t + j)) > 0 for j in range(k)):
                return t - start, "projected"
        return None, "no_breach_within_horizon"

    # ---------- Public: enrich ----------
    @staticmethod
    def enrich(df_out: pd.DataFrame, cfg: EpistemicConfig) -> Dict[str, Any]:
        """
        Compute board-level epistemic diagnostics on the processed output (df_out).
        df_out must contain: Date, Forecast, Actual, drift, Theta, loss, rupture.
        """
        if "drift" not in df_out.columns or "Theta" not in df_out.columns:
            raise ValueError("df_out must include columns: 'drift' and 'Theta'.")

        eps = 1e-9
        # Relative percent error (guarded)
        denom = (df_out["Actual"].abs() + eps)
        pct_err = (df_out["drift"] / denom).replace([np.inf, -np.inf], np.nan).fillna(0.0)

        on_target = pct_err <= float(cfg.on_target_pct)
        over = (df_out["Forecast"] > df_out["Actual"]) & ~on_target
        under = (df_out["Forecast"] < df_out["Actual"]) & ~on_target
        severe = pct_err >= float(cfg.severe_pct)

        econ = {
            "total_loss": float(df_out["loss"].sum()),
            "loss_per_unit_mean": float(
                (df_out["loss"] / denom).replace([np.inf, -np.inf], np.nan).fillna(0.0).mean()
            ),
            "overforecast_count": int(over.sum()),
            "underforecast_count": int(under.sum()),
            "on_target_count": int(on_target.sum()),
            "severe_miss_count": int(severe.sum()),
            "severe_miss_rate": float(severe.mean()),
        }

        # Baseline & recent windows
        baseline = EpistemicAnalytics._load_baseline(df_out, cfg)
        recent_len = int(cfg.recent_window) if cfg.recent_window else len(baseline)
        recent_len = max(1, min(recent_len, len(df_out)))
        recent = df_out["drift"].iloc[-recent_len:].astype(float)

        scope = EpistemicAnalytics._scope_score(recent, baseline, cfg.scope_q_lo, cfg.scope_q_hi)
        psi = EpistemicAnalytics._psi(
            actual=recent,
            expected=baseline,
            bins=int(cfg.psi_bins),
            min_bins=int(cfg.psi_min_bins),
            floor=float(cfg.psi_floor),
        )

        # Margin series for ETA
        margin = (df_out["drift"] - df_out["Theta"]).astype(float)
        eta_days, eta_note = EpistemicAnalytics._eta_to_breach(
            margin, cfg.expiry_k, cfg.expiry_lookback, cfg.min_points_for_trend
        )
        expiry_date = None
        if eta_days is not None:
            expiry_date = str((pd.Timestamp.today().normalize() + pd.Timedelta(days=int(eta_days))).date())

        epistemic = {
            "scope_score_0to1": float(scope),
            "psi": float(psi),
            "eta_days_to_persistent_breach": (None if eta_days is None else int(eta_days)),
            "eta_rationale": eta_note,  # helps explain why ETA is None/0/projected
            "expiry_estimate_date": expiry_date,
        }

        # Diagnostics: quantiles & window sizes (for auditability)
        diag = {
            "baseline_window_used": int(len(baseline)),
            "recent_window_used": int(len(recent)),
            "baseline_quantiles": {
                "q05": float(np.quantile(baseline, 0.05)),
                "q50": float(np.quantile(baseline, 0.50)),
                "q95": float(np.quantile(baseline, 0.95)),
            },
            "recent_quantiles": {
                "q05": float(np.quantile(recent, 0.05)),
                "q50": float(np.quantile(recent, 0.50)),
                "q95": float(np.quantile(recent, 0.95)),
            },
        }

        # Optional group breakdown (segment) if requested and present
        by_group: Optional[Dict[str, Any]] = None
        if cfg.groupby and (cfg.groupby in df_out.columns):
            by_group = {}
            for g, sub in df_out.groupby(cfg.groupby, sort=True):
                denom_g = (sub["Actual"].abs() + eps)
                pct_err_g = (sub["drift"] / denom_g).replace([np.inf, -np.inf], np.nan).fillna(0.0)
                on_t_g = (pct_err_g <= cfg.on_target_pct)
                severe_g = (pct_err_g >= cfg.severe_pct)
                by_group[str(g)] = {
                    "n": int(len(sub)),
                    "ruptures": int(sub["rupture"].sum()),
                    "loss": float(sub["loss"].sum()),
                    "on_target_rate": float(on_t_g.mean()),
                    "severe_rate": float(severe_g.mean()),
                }

        # Optional policy vs non-policy economics if a boolean column exists
        policy_breakdown: Optional[Dict[str, Any]] = None
        if cfg.policy_col and (cfg.policy_col in df_out.columns):
            pc = df_out[cfg.policy_col].astype(bool)
            def econ_slice(mask: pd.Series) -> Dict[str, Any]:
                sl = df_out[mask]
                d = (sl["loss"] / (sl["Actual"].abs() + eps)).replace([np.inf, -np.inf], np.nan).fillna(0.0)
                return {
                    "n": int(len(sl)),
                    "ruptures": int(sl["rupture"].sum()),
                    "total_loss": float(sl["loss"].sum()),
                    "loss_per_unit_mean": float(d.mean()),
                    "mean_drift": float(sl["drift"].mean()) if len(sl) else 0.0,
                }
            policy_breakdown = {
                "policy_true": econ_slice(pc),
                "policy_false": econ_slice(~pc),
            }

        out: Dict[str, Any] = {
            "economics": econ,
            "epistemic": epistemic,
            "diagnostics": diag,
        }
        if by_group is not None:
            out["by_group"] = by_group
        if policy_breakdown is not None:
            out["policy_breakdown"] = policy_breakdown
        return out
