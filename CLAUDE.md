# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SigProfilerExtractor is a Python bioinformatics tool for de novo extraction of mutational signatures from genomic data. It uses Non-Negative Matrix Factorization (NMF) to identify operative mutational signatures, their activities per sample, and mutation type probabilities. Part of the SigProfilerSuite ecosystem.

## Build & Install

```bash
pip install .
```

A reference genome is required for VCF-based analyses:
```python
from SigProfilerMatrixGenerator import install as genInstall
genInstall.install('GRCh37')
```

## Running Tests

```bash
python3 test.py
```

This runs 7 test functions sequentially (SBS96, DBS78, ID83, CNV48, SV32, seg:BATTENBERG, VCF). Each test uses minimal NMF parameters (5 replicates, 100-1000 iterations) for speed. To run a single test, call the function directly:

```python
from test import run_matrix_96
run_matrix_96()
```

Test output directories (`test_*_output/`) are gitignored.

## CI

GitHub Actions (`.github/workflows/ci.yml`) runs tests on Python 3.10 and 3.12 against Ubuntu. On master push with Python 3.12, it also builds and pushes a Docker image to `ghcr.io/sigprofilersuite/sigprofileextractor`.

## Architecture

### Core Pipeline (NMF Signature Extraction)

1. **`sigpro.py`** — Main entry point. `sigProfilerExtractor()` orchestrates the full pipeline: input parsing, matrix generation, NMF decomposition across signature counts, solution selection, and COSMIC decomposition. `importdata()` provides paths to bundled example data.

2. **`subroutines.py`** — NMF execution engine. Handles bootstrap resampling (`BootstrapCancerGenomes`), parallel NMF dispatch (`pnmf`), signature clustering (`parallel_clustering`), convergence checking, similarity metrics (`cos_sim`, `cor_sim`), and result export (`export_information`).

3. **`nmf_cpu.py` / `nmf_gpu.py`** — NMF implementations using beta-divergence with multiplicative update rules. GPU version uses PyTorch CUDA. Selection is automatic based on `gpu` parameter.

4. **`nndsvd.py`** — NNDSVD initialization for NMF W/H matrices. Replaced the external `nimfa` dependency (v1.2.7) for NumPy 2.0 compatibility.

5. **`estimate_best_solution.py`** — Selects optimal signature count using stability and mean sample cosine distance thresholds.

### Input/Output

- **Input types**: `"vcf"`, `"matrix"`, `"bedpe"`, `"seg:TYPE"` (where TYPE is a CNV caller like BATTENBERG, ASCAT, etc.), `"csv"`, `"matobj"`
- **Mutation contexts**: SBS96, SBS288, SBS1536, DBS78, ID83, CNV48, SV32
- **Output**: Signature matrices (W, H), activity matrices, stability plots, COSMIC decomposition — written to the specified output directory

### Key Dependencies

- **SigProfilerMatrixGenerator**: Converts VCF/bedpe/seg inputs into mutation count matrices
- **SigProfilerAssignment**: Decomposes extracted signatures against COSMIC references
- **sigProfilerPlotting**: Generates signature and activity plots
- **PyTorch**: Powers GPU-accelerated NMF

### CLI

```bash
SigProfilerExtractor sigprofilerextractor <input_type> <output> <input_data> [options]
```

Implemented in `sigprofilerextractor_cli.py` → `controllers/cli_controller.py`.

## Key Constraints

- Requires NumPy >= 2.0.0 and pandas >= 2.0.0
- Python >= 3.9
- GPU mode requires CUDA-capable PyTorch; reduce `cpu` parameter if CUDA OOM errors occur
- Reference genomes must be pre-installed for VCF input processing
