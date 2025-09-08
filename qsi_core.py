from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, Any, Tuple, Optional, List
import numpy as np
import pandas as pd

_USE_COGNIZE = False
try:
    from cognize import EpistemicState, PolicyManager, PolicyMemory, ShadowRunner, SAFE_SPECS
    from cognize.policies import threshold_adaptive, realign_tanh, collapse_soft_decay
    from cognize import EpistemicGraph, make_simple_state, Perception
    _USE_COGNIZE = True
except Exception:
    _USE_COGNIZE = False


# ---------------- Public config ----------------
@dataclass
class QSIConfig:
    # Columns
    col_date: str = "Date"
    col_fc: str = "Forecast"
    col_ac: str = "Actual"
    col_cost: str = "Unit_Cost"
    col_segment: Optional[str] = None  # "SKU" or "Region"

    # Native (fallback) policy params
    base_threshold: float = 120.0
    a: float = 0.02
    c: float = 0.25
    sigma: float = 5.0
    use_ewma: bool = False
    ewma_alpha: float = 0.2
    ewma_k: float = 3.0

    # Probability calibration
    prob_k: float = 6.0
    prob_mid: float = 0.0

    # Engine
    seed: int = 123
    use_cognize: bool = True             # allow disabling Cognize even if installed
    use_graph: bool = False              # multi-node graph by segment (Cognize only)
    max_graph_depth: int = 1
    graph_damping: float = 0.5           # influence damping

    # Meta-policy (Cognize only)
    epsilon: float = 0.10                # exploration rate
    promote_margin: float = 1.02         # performance lift to promote
    cooldown_steps: int = 20             # avoid thrash


class QSIEngine:
    """
    QSI — Quantitative Stochastic Intelligence (brand-pure).
    If Cognize is available and enabled, uses it under the hood; otherwise runs native logic.

    API:
        analyze(df, groupby=None) -> (df_out, report)
    """

    def __init__(self, config: Optional[QSIConfig] = None):
        self.cfg = config or QSIConfig()

    # --------------- Public ---------------
    def analyze(
        self,
        df: pd.DataFrame,
        groupby: Optional[str] = None,
    ) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        df = self._prep(df)
        use_cog = _USE_COGNIZE and self.cfg.use_cognize

        if groupby and use_cog and self.cfg.use_graph:
            return self._analyze_cognize_graph(df, groupby)

        if groupby:
            pieces, reports = [], {}
            for seg, sub in df.groupby(groupby, sort=True):
                out, rep = (self._analyze_cognize(sub) if use_cog else self._analyze_native(sub))
                pieces.append(out.assign(**{groupby: seg}))
                reports[str(seg)] = rep["summary"]
            merged = pd.concat(pieces, ignore_index=True)
            overall = self._make_report(merged, by_segment=reports)
            return merged, overall
        else:
            return (self._analyze_cognize(df) if use_cog else self._analyze_native(df))

    # --------------- Prep / validation ---------------
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

    # --------------- Native fallback ---------------
    def _sigmoid(self, x):  # margin -> prob
        return 1.0 / (1.0 + np.exp(-self.cfg.prob_k * (x - self.cfg.prob_mid)))

    def _theta_ewma(self, delta: pd.Series) -> pd.Series:
        mu = delta.ewm(alpha=self.cfg.ewma_alpha).mean()
        var = delta.ewm(alpha=self.cfg.ewma_alpha).var()
        std = np.sqrt(var.fillna(0.0))
        return (mu + self.cfg.ewma_k * std).astype(float)

    def _analyze_native(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        c = self.cfg
        rng = np.random.default_rng(c.seed)
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

    # --------------- Cognize (single stream) ---------------
    def _analyze_cognize(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        c = self.cfg
        rng = np.random.default_rng(c.seed)

        # Build state & policy manager (meta-policy with SAFE_SPECS)
        s = EpistemicState(V0=0.0, threshold=c.base_threshold, realign_strength=c.c)
        s.inject_policy(
            threshold=threshold_adaptive,       # adaptive Θ (uses state & params)
            realign=realign_tanh,               # smooth memory updates
            collapse=collapse_soft_decay,       # gentle cooldown
        )
        s.policy_manager = PolicyManager(
            base_specs=SAFE_SPECS, memory=PolicyMemory(), shadow=ShadowRunner(),
            epsilon=c.epsilon, promote_margin=c.promote_margin, cooldown_steps=c.cooldown_steps
        )

        rows = []
        for _, r in df.iterrows():
            V = float(abs(r[c.col_fc] - r[c.col_ac]))        # belief vs reality drift magnitude
            # optionally add perception / extra context
            s.receive(V)                                     # runs threshold/realign/collapse + meta-policy
            last = s.last()                                  # dict with Δ, Θ, E, ruptured, etc.

            # probability from margin (keep your sigmoid for continuity)
            margin = float(last.get("∆", V) - last.get("Θ", c.base_threshold))
            p = 1.0 / (1.0 + np.exp(-c.prob_k * (margin - c.prob_mid)))
            rupt = bool(last.get("ruptured", margin > 0.0))
            loss = V * float(r[c.col_cost]) if rupt else 0.0

            rows.append({
                c.col_date: r[c.col_date],
                c.col_fc: r[c.col_fc],
                c.col_ac: r[c.col_ac],
                c.col_cost: r[c.col_cost],
                "drift": V,
                "E": float(last.get("E", s.E)),
                "Theta": float(last.get("Θ", s.threshold)),
                "rupture": rupt,
                "rupture_prob": float(p),
                "loss": float(loss),
            })
            # reset memory on hard rupture (optional; Cognize will also cool via collapse)
            if rupt:
                s.E = 0.0

        out = pd.DataFrame(rows)
        report = self._make_report(out, engine="cognize")
        return out, report

    # --------------- Cognize (multi-node graph by segment) ---------------
    def _analyze_cognize_graph(self, df: pd.DataFrame, groupby: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        c = self.cfg
        if groupby not in df.columns:
            raise ValueError(f"groupby '{groupby}' not found.")
        G = EpistemicGraph(damping=c.graph_damping, max_depth=c.max_graph_depth)

        # Build one node per segment
        segments = sorted(df[groupby].dropna().unique().tolist())
        for seg in segments:
            st = make_simple_state(0.0)
            st.threshold = c.base_threshold
            G.add(str(seg), st)

        # (Optional) link segments to share pressure only when they rupture
        # Example: weak coupling across all segments
        for i in range(len(segments) - 1):
            G.link(str(segments[i]), str(segments[i+1]), mode="pressure", weight=0.2, decay=0.9, cooldown=3)

        # Step through time in lock-step
        by_seg_dfs: List[pd.DataFrame] = []
        for ts, frame in df.groupby(c.col_date, sort=True):
            # drive each node with that segment’s drift
            for seg, r in frame.groupby(groupby):
                V = float(abs(r.iloc[0][c.col_fc] - r.iloc[0][c.col_ac]))
                G.step(str(seg), V)   # propagation happens internally per links

            # collect snapshot
            snap_rows = []
            for seg in segments:
                # Each node keeps last; export minimal stats
                st = G.nodes[str(seg)]
                post = st.last() if hasattr(st, "last") else {}
                margin = float(post.get("∆", 0.0) - post.get("Θ", c.base_threshold))
                p = 1.0 / (1.0 + np.exp(-c.prob_k * (margin - c.prob_mid)))
                rupt = bool(post.get("ruptured", margin > 0.0))

                # fetch the row for this ts/seg to grab cost
                row = frame[frame[groupby] == seg].iloc[0]
                V = float(abs(row[c.col_fc] - row[c.col_ac]))
                loss = V * float(row[c.col_cost]) if rupt else 0.0

                snap_rows.append({
                    c.col_date: ts,
                    groupby: seg,
                    c.col_fc: row[c.col_fc],
                    c.col_ac: row[c.col_ac],
                    c.col_cost: row[c.col_cost],
                    "drift": V,
                    "E": float(post.get("E", 0.0)),
                    "Theta": float(post.get("Θ", c.base_threshold)),
                    "rupture": rupt,
                    "rupture_prob": float(p),
                    "loss": float(loss),
                })
            by_seg_dfs.append(pd.DataFrame(snap_rows))

        out = pd.concat(by_seg_dfs, ignore_index=True)
        report = self._make_report(out, engine="cognize-graph", by_segment=out.groupby(groupby)["loss"].sum().to_dict())
        return out, report

    # --------------- Report ---------------
    def _make_report(self, df_out: pd.DataFrame, engine: str = "", by_segment: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        s = {
            "n": int(len(df_out)),
            "ruptures": int(df_out["rupture"].sum()),
            "total_loss": float(df_out["loss"].sum()),
            "mean_drift": float(df_out["drift"].mean()),
            "median_drift": float(df_out["drift"].median()),
            "max_drift": float(df_out["drift"].max()),
            "engine": engine or ("cognize" if _USE_COGNIZE and self.cfg.use_cognize else "native"),
            "config": asdict(self.cfg),
        }
        events_cols = [self.cfg.col_date, "drift", "Theta", "rupture_prob", "loss"]
        if self.cfg.col_segment and self.cfg.col_segment in df_out.columns:
            events_cols.insert(1, self.cfg.col_segment)
        events = df_out.loc[df_out["rupture"], events_cols].reset_index(drop=True)
        rep = {"summary": s, "events": events}
        if by_segment is not None:
            rep["by_segment"] = by_segment
        return rep


# Convenience
def generate_dummy(days: int = 30, seed: int = 42, unit_cost: float = 40.0, segments: Optional[List[str]] = None) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=days)
    if segments:
        rows = []
        for seg in segments:
            fc = rng.normal(1000, 100, days).round().astype(int)
            ac = fc - rng.normal(0, 150, days).round().astype(int)
            for i in range(days):
                rows.append({"Date": dates[i], "Forecast": fc[i], "Actual": ac[i], "Unit_Cost": unit_cost, "Segment": seg})
        return pd.DataFrame(rows)
    else:
        fc = rng.normal(1000, 100, days).round().astype(int)
        ac = fc - rng.normal(0, 150, days).round().astype(int)
        return pd.DataFrame({"Date": dates, "Forecast": fc, "Actual": ac, "Unit_Cost": unit_cost})
