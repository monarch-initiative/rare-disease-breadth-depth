# Rare-disease treatment + breadth/depth scoring

A frozen, citable, reproducible extraction of the rare-disease prioritization
score developed in monarch-ingest
[PR #632](https://github.com/monarch-initiative/monarch-ingest/pull/632).

Each MONDO rare disease gets a score combining whether it has any treatment with
how broad/deep its HPO phenotype profile is:

```
score = 100 * (any_treatment_count > 0) + histopheno_sum_of_mean_ic_across_systems
```

then ranked. This repo reproduces that published score **exactly** from frozen
inputs, with no dependency on the live Monarch pipeline.

## Quick start

```sh
uv sync                  # or: pip install -e .
uv run python score.py   # reproduce + validate, write the ranked table
```

`score.py` reproduces the published `treatment_plus_breadth_score` to within
**max abs diff 5.7e-14** of the frozen reference (`data/reference_score.csv`).

## What's frozen here, and why

The original analysis depended on a freshly built 4.7 GB `monarch-kg.duckdb`, an
experimental `closurizer` fork, a runtime `oaklib` call pulling an unversioned HP
sqlite, several hand-run `gsed`/`grep` fixups, and a local `ada rescue - mondo.tsv`
that was never committed — none of which is reproducible later. Rather than
vendoring that fragile toolchain to *recompute* the metrics, this repo **freezes
the computed component table** and scores from it:

| file | what it is | tier |
|---|---|---|
| `data/mondo_rare_report.csv` | per-disease treatment counts + breadth/depth IC metrics — every score input (15,698 diseases) | **freeze** |
| `data/reference_score.csv` | the published score, for byte-level validation (9,100 diseases) | **freeze** |
| `data/hp_ics.tsv` | the HPO information-content table (would otherwise be an unversioned `oaklib` run) | **freeze** |
| `data/ada_rescue_mondo_curies.txt` | the hand-curated MONDO CURIEs that widened the rare cohort | **vendor** |
| `sql/*.sql` | the build SQL that produced `mondo_rare_report.csv`, verbatim | **vendor (provenance)** |
| `pyproject.toml` + `uv.lock` | exact pinned Python environment | **pin** |

Source build: Monarch KG dev `2025-04-16-treatment-experimental`. See
`DATA_PROVENANCE.md`.

## A reproducibility note worth surfacing

The published reference scores exactly 9,100 diseases (those with breadth > 0),
but the committed final SQL uses `coalesce(breadth,0)` over a left join, which
would score all ~15,698. The artifact and the committed SQL therefore diverge on
cohort inclusion; this repo matches the published 9,100-disease cohort so the
reproduction is exact, and `DATA_PROVENANCE.md` records the gap.

## Citing

Tag a release and let Zenodo archive it for a DOI; `CITATION.cff` carries the
metadata.
