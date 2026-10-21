# Data provenance

All frozen inputs in `data/` derive from one Monarch KG dev build:

- **Build:** `monarch-kg-dev / 2025-04-16-treatment-experimental`
- **Source:** https://data.monarchinitiative.org/monarch-kg-dev/2025-04-16-treatment-experimental/
- **Built from:** monarch-ingest PR #632, branch `multiomics-approvals-and-trials-edges`
  (experimental `closurizer` fork `fix_node_joins`; multiomics clinical-trials
  KP v2.7.2 and drug-approvals KP v0.3.7)

| local file | upstream artifact |
|---|---|
| `data/mondo_rare_report.csv` | `qc/mondo_rare_report.tsv` (comma-delimited despite the `.tsv` name) |
| `data/reference_score.csv` | `qc/mondo_rare_report_treatment_plus_breadth_score.tsv` |
| `data/hp_ics.tsv` | `qc/hp.ics.tsv` |
| `data/ada_rescue_mondo_curies.txt` | `mondoCURIE` column of `ada rescue - mondo.tsv` (hand-curated) |

The full `monarch-kg.duckdb` (~4.7 GB) from the same build is **not** committed.
For reproducing the frozen score it is not needed. To re-derive the component
metrics themselves from scratch, download it and run `sql/` against it.

## For archival / DOI

To mint a citable DOI, tag a release and let Zenodo archive it. The `data/`
files total ~6 MB and travel inside the repo; the duckdb, if needed for the
record, should be a separate Zenodo data deposit referenced by URL, not committed
to git.
