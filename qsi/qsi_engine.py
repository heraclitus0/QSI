# qsi_engine.py
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, Any, Tuple, Optional, List
import numpy as np
import pandas as pd


_USE_COGNIZE = False
try:
    from cognize import (
        EpistemicState, PolicyManager, PolicyMemory, ShadowRunner, SAFE_SPECS,
        EpistemicGraph, make_simple_state
    )
    from cognize.policies import threshold_adaptive, realign_tanh, collapse_soft_decay
    _USE_COGNIZE = True
except Exception:
    _USE_COGNIZE = False


# ----------------------------- Config -----------------------------
@dataclass
class QSIConfig:
    # Column names
    col_date: str = "Date"
    col_fc: str = "Forecast"
    col_ac: str = "Actual"
    col_cost: str = "Unit_Cost"
    col_segment: Optional[str] = None  # e.g., "SKU" or "Region"

    # Native policy knobs
    base_threshold: float = 120.0
    a: float = 0.02           # Θ sensitivity to memory E
    c: float = 0.25           # memory accumulation factor
    sigma: float = 5.0        # Gaussian noise on Θ
    seed: int = 123

    # EWMA alternative
    use_ewma: bool = False
    ewma_alpha: float = 0.2
    ewma_k: float = 3.0

    # Rupture probability calibration (logistic on margin = drift-Θ)
    prob_k: float = 6.0
    prob_mid: float = 0.0

    # Engine switches
    use_cognize: bool = True          # allow turning OFF Cognize even if available
    use_graph: bool = False           # multi-node coupling by segment (Cognize only)
    graph_damping: float = 0.5
    max_graph_depth: int = 1

    # Cognize meta-policy (only used when Cognize path active)
    epsilon: float = 0.10
    promote_margin: float = 1.02
    cooldown_steps: int = 20


# ----------------------------- Engine -----------------------------
class QSIEngine:
    """
    QSI — Quantitative Stochastic Intelligence.
    Analyze a time series (optionally segmented) and emit drift, memory, thresholds, rupture flags, loss.

    API:
        df_out, report = QSIEngine(cfg).analyze(df, groupby=None or "SKU")
    """

    def __init__(self, config: Optional[QSIConfig] = None):
        self.cfg = config or QSIConfig()

    # ----------------- Public entrypoint -----------------
    def analyze(self, df: pd.DataFrame, groupby: Optional[str] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        df = self._prep(df)
        use_cog = _USE_COGNIZE and self.cfg.use_cognize

        if groupby and use_cog and self.cfg.use_graph:
            return self._analyze_cognize_graph(df, groupby)

        if groupby:
            parts: List[pd.DataFrame] = []
            by_seg: Dict[str, Any] = {}
            for seg, sub in df.groupby(groupby, sort=True):
                out, rep = (self._analyze_cognize(sub) if use_cog else self._analyze_native(sub))
                out[groupby] = seg
                parts.append(out)
                by_seg[str(seg)] = {
                    "n": int(len(out)),
                    "ruptures": int(out["rupture"].sum()),
                    "loss": float(out["loss"].sum()),
                }
            merged = pd.concat(parts, ignore_index=True)
            overall = self._make_report(merged, engine=("cognize" if use_cog else "native"), by_segment=by_seg)
            return merged, overall

        # single stream
        return (self._analyze_cognize(df) if use_cog else self._analyze_native(df))

    # ----------------- Validation / prep -----------------
    def _prep(self, df: pd.DataFrame) -> pd.DataFrame:
        c = self.cfg
        need = [c.col_date, c.col_fc, c.col_ac, c.col_cost]
        miss = [x for x in need if x not in df.columns]
        if miss:
            raise ValueError(f"Missing columns: {miss}. Required: {need}")
        out = df.copy()
        if not np.issubdtype(out[c.col_date].dtype, np.datetime64):
            out[c.col_date] = pd.to_datetime(out[c.col_date], errors="raise")
        if out[[c.col_fc, c.col_ac]].isna().any().any():
            raise ValueError("NaNs in Forecast/Actual.")
        if (out[c.col_cost] < 0).any():
            raise ValueError("Unit_Cost must be >= 0.")
        return out.sort_values(c.col_date).reset_index(drop=True)

    # ----------------- Shared helpers -----------------
    def _sigmoid(self, x: np.ndarray | float) -> np.ndarray | float:
        k, mid = float(self.cfg.prob_k), float(self.cfg.prob_mid)
        return 1.0 / (1.0 + np.exp(-k * (np.asarray(x) - mid)))

    def _theta_ewma(self, delta: pd.Series) -> pd.Series:
        mu = delta.ewm(alpha=self.cfg.ewma_alpha).mean()
        var = delta.ewm(alpha=self.cfg.ewma_alpha).var()
        std = np.sqrt(var.fillna(0.0))
        return (mu + self.cfg.ewma_k * std).astype(float)

    # ----------------- Native path -----------------
    def _analyze_native(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        c, rng = self.cfg, np.random.default_rng(self.cfg.seed)
        fc = df[c.col_fc].to_numpy(float)
        ac = df[c.col_ac].to_numpy(float)
        cost = df[c.col_cost].to_numpy(float)
        drift = np.abs(fc - ac)

        E = np.zeros_like(drift)
        Theta = np.zeros_like(drift)
        rupture = np.zeros_like(drift, dtype=bool)
        loss = np.zeros_like(drift, dtype=float)

        if c.use_ewma:
            Theta = self._theta_ewma(pd.Series(drift)).to_numpy(float)
            mem = 0.0
            for i, d in enumerate(drift):
                if d > Theta[i]:
                    rupture[i] = True; loss[i] = d * cost[i]; mem = 0.0
                else:
                    mem = mem + c.c * d
                E[i] = mem
        else:
            mem = 0.0
            for i, d in enumerate(drift):
                eps = float(rng.normal(0.0, c.sigma)) if c.sigma > 0 else 0.0
                th = max(0.0, c.base_threshold + c.a * mem + eps)
                Theta[i] = th
                if d > th:
                    rupture[i] = True; loss[i] = d * cost[i]; mem = 0.0
                else:
                    mem = mem + c.c * d
                E[i] = mem

        margin = drift - Theta
        p = self._sigmoid(margin)

        out = df.copy()
        out["drift"], out["E"], out["Theta"] = drift, E, Theta
        out["rupture"], out["rupture_prob"], out["loss"] = rupture, p, loss
        report = self._make_report(out, engine="native")
        return out, report

    # ----------------- Cognize single-stream -----------------
    def _analyze_cognize(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        c = self.cfg
        # Base state with safe policies; PolicyManager handles meta-policy selection.
        s = EpistemicState(V0=0.0, threshold=c.base_threshold, realign_strength=c.c)
        s.inject_policy(threshold=threshold_adaptive, realign=realign_tanh, collapse=collapse_soft_decay)
        s.policy_manager = PolicyManager(
            base_specs=SAFE_SPECS, memory=PolicyMemory(), shadow=ShadowRunner(),
            epsilon=c.epsilon, promote_margin=c.promote_margin, cooldown_steps=c.cooldown_steps
        )

        rows = []
        for _, r in df.iterrows():
            # Drift = |Forecast - Actual|
            V = float(abs(r[c.col_fc] - r[c.col_ac]))
            s.receive(V)                      # runs threshold/realign/collapse & meta-policy
            last = s.last() or {}

            # SAFE Θ extraction (Cognize keys may vary)
            theta_val = last.get("Θ")
            if theta_val is None:
                theta_val = last.get("threshold")
            if theta_val is None:
                theta_val = getattr(s, "threshold", 0.0)
            theta_val = float(theta_val)

            margin = float(last.get("∆", V) - theta_val)
            p = float(self._sigmoid(margin))
            rupt = bool(last.get("ruptured", margin > 0.0))
            loss = V * float(r[c.col_cost]) if rupt else 0.0

            rows.append({
                c.col_date: r[c.col_date],
                c.col_fc: r[c.col_fc],
                c.col_ac: r[c.col_ac],
                c.col_cost: r[c.col_cost],
                "drift": V,
                "E": float(last.get("E", s.E)),
                "Theta": theta_val,
                "rupture": rupt,
                "rupture_prob": p,
                "loss": float(loss),
            })

            # Keep semantics aligned with native: reset memory on rupture.
            if rupt:
                s.E = 0.0

        out = pd.DataFrame(rows)
        report = self._make_report(out, engine="cognize")
        return out, report

    # ----------------- Cognize graph (segments coupling) -----------------
    def _analyze_cognize_graph(self, df: pd.DataFrame, groupby: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        c = self.cfg
        if groupby not in df.columns:
            raise ValueError(f"groupby '{groupby}' not found in DataFrame.")

        G = EpistemicGraph(damping=c.graph_damping, max_depth=c.max_graph_depth)
        segments = sorted(df[groupby].dropna().unique().tolist())
        for seg in segments:
            st = make_simple_state(0.0)
            st.threshold = c.base_threshold
            G.add(str(seg), st)

        # weak ring coupling (pressure only when upstream ruptures)
        for i in range(len(segments) - 1):
            G.link(str(segments[i]), str(segments[i + 1]), mode="pressure", weight=0.2, decay=0.9, cooldown=3)

        frames: List[pd.DataFrame] = []
        for ts, frame in df.groupby(c.col_date, sort=True):
            # drive each node by its segment drift
            for seg, r in frame.groupby(groupby):
                V = float(abs(r.iloc[0][c.col_fc] - r.iloc[0][c.col_ac]))
                G.step(str(seg), V)

            # collect a snapshot for all segments
            snap = []
            for seg in segments:
                st = G.nodes[str(seg)]
                post = st.last() if hasattr(st, "last") else {}
                theta_val = post.get("Θ") or post.get("threshold") or getattr(st, "threshold", 0.0)
                theta_val = float(theta_val)
                delta_val = float(post.get("∆", 0.0))
                margin = delta_val - theta_val
                p = float(self._sigmoid(margin))
                rupt = bool(post.get("ruptured", margin > 0.0))

                row = frame[frame[groupby] == seg].iloc[0]
                V = float(abs(row[c.col_fc] - row[c.col_ac]))
                loss = V * float(row[c.col_cost]) if rupt else 0.0

                snap.append({
                    c.col_date: ts,
                    groupby: seg,
                    c.col_fc: row[c.col_fc],
                    c.col_ac: row[c.col_ac],
                    c.col_cost: row[c.col_cost],
                    "drift": V,
                    "E": float(post.get("E", 0.0)),
                    "Theta": theta_val,
                    "rupture": rupt,
                    "rupture_prob": p,
                    "loss": float(loss),
                })
            frames.append(pd.DataFrame(snap))

        out = pd.concat(frames, ignore_index=True)

        # optional graph telemetry (best-effort)
        graph_meta = {}
        try:
            if hasattr(G, "stats"):
                graph_meta["stats"] = G.stats()
            if hasattr(G, "last_cascade"):
                lc = G.last_cascade(10)
                if isinstance(lc, list):
                    graph_meta["last_cascade"] = lc
        except Exception:
            pass

        rep = self._make_report(
            out, engine="cognize-graph",
            by_segment=out.groupby(groupby)["loss"].sum().to_dict()
        )
        if graph_meta:
            rep["graph"] = graph_meta
        return out, rep

    # ----------------- Reporting -----------------
    def _make_report(self, df_out: pd.DataFrame, engine: str, by_segment: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        summary = {
            "n": int(len(df_out)),
            "ruptures": int(df_out["rupture"].sum()),
            "total_loss": float(df_out["loss"].sum()),
            "mean_drift": float(df_out["drift"].mean()),
            "median_drift": float(df_out["drift"].median()),
            "max_drift": float(df_out["drift"].max()),
            "engine": engine,
            "config": asdict(self.cfg),
        }
        events_cols = [self.cfg.col_date, "drift", "Theta", "rupture_prob", "loss"]
        if self.cfg.col_segment and self.cfg.col_segment in df_out.columns:
            events_cols.insert(1, self.cfg.col_segment)
        events = df_out.loc[df_out["rupture"], events_cols].reset_index(drop=True)
        rep = {"summary": summary, "events": events}
        if by_segment is not None:
            rep["by_segment"] = by_segment
        return rep


# ----------------- Convenience: demo data -----------------
def generate_dummy(days: int = 60, seed: int = 42, unit_cost: float = 40.0, segments: Optional[List[str]] = None) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=days)
    if segments:
        rows = []
        for seg in segments:
            fc = rng.normal(1000, 100, days).round().astype(int)
            ac = fc - rng.normal(0, 150, days).round().astype(int)
            for i in range(days):
                rows.append({
                    "Date": dates[i],
                    "Forecast": fc[i],
                    "Actual": ac[i],
                    "Unit_Cost": unit_cost,
                    "Segment": seg
                })
        return pd.DataFrame(rows)
    else:
        fc = rng.normal(1000, 100, days).round().astype(int)
        ac = fc - rng.normal(0, 150, days).round().astype(int)
        return pd.DataFrame({
            "Date": dates,
            "Forecast": fc,
            "Actual": ac,
            "Unit_Cost": unit_cost
        })
