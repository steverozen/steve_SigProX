# Installation

## Install from PyPI

```bash
pip install SigProfilerExtractor
```

## Install from source

```bash
git clone https://github.com/SigProfilerSuite/SigProfilerExtractor.git
cd SigProfilerExtractor
pip install .
```

## Install reference genomes (SigProfilerMatrixGenerator)

SigProfilerExtractor uses SigProfilerMatrixGenerator to build mutation matrices from VCF (and other) inputs. Install at least one reference genome:

```python
from SigProfilerMatrixGenerator import install as genInstall
genInstall.install("GRCh37")
```

