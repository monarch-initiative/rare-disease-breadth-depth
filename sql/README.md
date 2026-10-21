# Vendored provenance SQL

These two scripts are the **provenance** of `data/mondo_rare_report.csv` — they
are how the component table was computed inside the Monarch KG build (PR
[monarch-ingest#632](https://github.com/monarch-initiative/monarch-ingest/pull/632),
branch `multiomics-approvals-and-trials-edges`). They are vendored verbatim so
the derivation is citable and inspectable.

They are **not** on the runtime path of this repo. Reproducing the score uses
only the frozen `data/*.csv`; see the top-level README.

Re-running these requires the full 2025-04-16 treatment-experimental
`monarch-kg.duckdb` (~4.7 GB, available from the Monarch dev data server) plus
the experimental `closurizer` fork (`fix_node_joins`) and the multiomics KP
downloads — i.e. the exact fragile environment this repo exists to freeze away.

- `extend_denormalized_nodes.sql` — rolls the multiomics `treats` /
  `applied_to_treat` / `in_clinical_trials_for` edges up onto disease nodes.
- `generate_mondo_reports.sql` — builds the HistoPheno per-system IC breadth
  tables, the descendant-IC table, `mondo_rare_report`, and the final
  `treatment_plus_breadth_score`.
