# SigProfilerExtractor

SigProfilerExtractor performs *de novo* extraction of mutational signatures from mutation catalogues (SBS/DBS/ID/CNV/SV), and can optionally decompose extracted signatures into COSMIC reference signatures via SigProfilerAssignment.

## Quick start (Python)

```python
from SigProfilerExtractor import sigpro as sig

data = sig.importdata("matrix")
sig.sigProfilerExtractor(
    input_type="matrix",
    output="example_output",
    input_data=data,
    minimum_signatures=1,
    maximum_signatures=3,
)
```

## Quick start (CLI)

```bash
SigProfilerExtractor sigprofilerextractor matrix example_output /path/to/Samples_SBS.txt --minimum_signatures 1 --maximum_signatures 3
```

