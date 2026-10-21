"""Rare-disease treatment + breadth/depth scoring — reproducible core.

Operates on the frozen `data/mondo_rare_report.csv` (the per-disease component
table published with the 2025-04-16 treatment-experimental monarch-kg build) and
reproduces the published `treatment_plus_breadth_score` exactly:

    score = 100 * (any_treatment_count > 0) + histopheno_sum_of_mean_ic_across_systems
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

DATA = Path(__file__).parent / "data"
REPORT_CSV = DATA / "mondo_rare_report.csv"
REFERENCE_CSV = DATA / "reference_score.csv"

TREATMENT_WEIGHT = 100


def load_report(path: Path = REPORT_CSV) -> pd.DataFrame:
    return pd.read_csv(path)


def _num(df: pd.DataFrame, col: str) -> pd.Series:
    return pd.to_numeric(df[col], errors="coerce").fillna(0.0)


def score(df: pd.DataFrame) -> pd.DataFrame:
    """Reproduce the published score; return id, name, score, rank, percent_rank.

    The published reference includes only diseases with breadth > 0 (n=9100);
    we match that cohort so the reproduction is exact.
    """
    breadth = _num(df, "histopheno_sum_of_mean_ic_across_systems")
    treatment = (_num(df, "drug_any_treatment_count") > 0).astype(float)
    s = TREATMENT_WEIGHT * treatment + breadth

    out = pd.DataFrame({"id": df["id"], "name": df["name"], "score": s})
    out = out[breadth > 0].copy()
    out = out.sort_values("score", ascending=False).reset_index(drop=True)
    out["rank"] = out["score"].rank(ascending=False, method="min").astype(int)
    out["percent_rank"] = out["score"].rank(ascending=True, method="average", pct=True)
    return out


def validate_against_reference(df: pd.DataFrame | None = None,
                               ref_path: Path = REFERENCE_CSV) -> float:
    """Return max abs diff between the reproduced score and the frozen reference."""
    df = load_report() if df is None else df
    got = score(df)
    ref = pd.read_csv(ref_path)
    m = got[["id", "score"]].merge(
        ref[["id", "treatment_plus_breadth_score"]], on="id", how="inner")
    if len(m) != len(ref):
        raise AssertionError(f"cohort mismatch: reproduced {len(m)} of {len(ref)} reference rows")
    return float((m["score"] - m["treatment_plus_breadth_score"]).abs().max())
