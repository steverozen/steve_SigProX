# CLI Usage

SigProfilerExtractor provides a CLI entrypoint:

```bash
SigProfilerExtractor sigprofilerextractor <input_type> <output> <input_data> [options]
```

Examples:

```bash
SigProfilerExtractor sigprofilerextractor matrix example_output /path/to/Samples_SBS.txt --minimum_signatures 1 --maximum_signatures 3
```

```bash
SigProfilerExtractor sigprofilerextractor vcf example_output /path/to/vcf_folder --reference_genome GRCh37 --minimum_signatures 1 --maximum_signatures 3
```

For full flags:

```bash
SigProfilerExtractor sigprofilerextractor --help
```

