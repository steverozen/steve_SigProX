# Output

SigProfilerExtractor writes results under the provided `output/` directory, grouped by mutation context (e.g. `SBS96/`, `DBS78/`, `ID83/`, `CNV48/`, `SV32/`).

Within each context folder you typically get:

- `All_Solutions/` per-rank outputs (signatures, activities, plots, stats)
- `Suggested_Solution/` the selected solution and (if enabled) COSMIC decomposition outputs
- `All_solutions_stat.csv` rank-selection statistics
- `Samples.txt` the input matrix used for extraction

