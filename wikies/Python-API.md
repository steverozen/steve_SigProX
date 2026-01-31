# Python API

## importdata

```python
from SigProfilerExtractor import sigpro as sig
path = sig.importdata("matrix")
```

## sigProfilerExtractor

```python
from SigProfilerExtractor import sigpro as sig
sig.sigProfilerExtractor(
    input_type="matrix",
    output="example_output",
    input_data=path,
    minimum_signatures=1,
    maximum_signatures=3,
)
```

## estimate_solution

```python
from SigProfilerExtractor import estimate_best_solution as ebs
ebs.estimate_solution(
    base_csvfile="All_solutions_stat.csv",
    All_solution="All_Solutions",
    genomes="Samples.txt",
    output="results",
)
```

