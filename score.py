"""Reproduce the published rare-disease score and write the ranked table.

    uv run python score.py

Validates the reproduction against the frozen reference, then writes
output/mondo_rare_report_treatment_plus_breadth_score.csv.
"""
from __future__ import annotations

from pathlib import Path

from breadth_depth import load_report, score, validate_against_reference


def main() -> None:
    max_diff = validate_against_reference()
    status = "OK" if max_diff < 1e-6 else "MISMATCH"
    print(f"reproduction vs frozen reference: max abs diff = {max_diff:.2e}  [{status}]")

    out = score(load_report())
    dest = Path(__file__).parent / "output" / "mondo_rare_report_treatment_plus_breadth_score.csv"
    dest.parent.mkdir(exist_ok=True)
    out.to_csv(dest, index=False)
    print(f"wrote {dest}  ({len(out)} diseases)")
    print("\ntop 10:")
    print(out[["rank", "id", "name", "score"]].head(10).to_string(index=False))


if __name__ == "__main__":
    main()
