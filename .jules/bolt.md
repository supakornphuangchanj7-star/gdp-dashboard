## 2026-03-31 - Pandas Filtering inside Streamlit Render Loops

**Learning:** Filtering Pandas DataFrames with boolean masks inside render loops (such as Streamlit metric loops per item) causes repeated full column scans on every script re-run (`O(N * M)` complexity). Pre-building O(1) dictionary lookups or using indexed Series before the loop reduces metric calculation time from ~10.5ms down to ~1.1ms (~10x speedup for typical selections) and from ~350ms to ~2.5ms (>140x speedup when all items are selected).

**Action:** When rendering loop components in Streamlit, always construct O(1) dictionary or indexed lookups outside the loop instead of executing `.loc[]` boolean expressions inside the loop.
