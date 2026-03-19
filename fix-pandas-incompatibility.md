Title: Fix pandas 2.0+ compatibility in subroutines.py

## Summary

Three bugs in `SigProfilerExtractor/subroutines.py` cause crashes when running with
pandas 2.0+. These are straightforward API compatibility issues.

---

## Bug 1: TypeError when assigning float into int64 DataFrame (pnmf)

**Function:** `pnmf`
**Location:** subroutines.py, line ~446

**Error:**
```
TypeError: Invalid value '0.0001' for dtype 'int64'
```

**Cause:**
pandas 2.0+ no longer silently upcasts integer columns when a float is assigned via
boolean mask indexing. The `bootstrapGenomes` DataFrame can have int64 dtype (e.g.
when `resample=False`, where it is passed through directly from the original genomes
matrix).

**Fix:**
```python
# Before
bootstrapGenomes[bootstrapGenomes < 0.0001] = 0.0001

# After
bootstrapGenomes = bootstrapGenomes.astype(float)
bootstrapGenomes[bootstrapGenomes < 0.0001] = 0.0001
```

---

## Bug 2: TypeError in to_csv() calls — separator passed as positional argument (export_information)

**Function:** `export_information`
**Location:** subroutines.py, 6 calls

**Error:**
```
TypeError: NDFrame.to_csv() takes from 1 to 2 positional arguments but 3 positional
arguments (and 1 keyword-only argument) were given
```

**Cause:**
pandas 2.0+ removed support for passing the separator as the second positional
argument to `DataFrame.to_csv()`. Six calls pass `"\t"` positionally.

**Affected calls** (output files):
- `_Signatures.txt`
- `_NMF_Activities.txt`
- `_Signatures_SEM_Error.txt`
- `_NMF_Activities_SEM_Error.txt`
- `_Signatures_stats.txt`
- `_NMF_Convergence_Information.txt`

**Fix:** Change `"\t"` positional argument to `sep="\t"` keyword argument in all six
calls. Example:
```python
# Before
processes.to_csv(path, "\t", index_label=[processes.columns.name])

# After
processes.to_csv(path, sep="\t", index_label=[processes.columns.name])
```

---

## Bug 3: TypeError when assigning strings into float64 columns (stabVsRError)

**Function:** `stabVsRError`
**Location:** subroutines.py, line ~1948

**Error:**
```
TypeError: Invalid value '...' for dtype 'float64'
```

**Cause:**
pandas 2.0+ refuses to assign string values (e.g. `"10.25%"`) in-place into columns
with float64 dtype. The line appends `"%"` to stringified float columns and tries to
store the result back into the same iloc slice, which still has float64 dtype.

**Fix:**
Assign column-by-column, which replaces each column entirely (including its dtype)
rather than trying to write strings in-place into float64 columns:
```python
# Before
data.iloc[:, 3:7] = data.iloc[:, 3:7].astype(str) + "%"

# After
for col in data.columns[3:7]:
    data[col] = data[col].astype(str) + "%"
```

---

## Environment

- Python 3.14
- pandas 2.x
