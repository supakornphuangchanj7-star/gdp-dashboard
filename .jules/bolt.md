## 2026-03-30 - Pandas repeated boolean indexing inside loops in Streamlit re-renders
**Learning:** Performing boolean indexing on large DataFrames (`df[df['col'] == val]`) repeatedly inside UI component rendering loops causes cumulative latency (O(N * M)) during Streamlit re-runs. Pre-mapping data to a dictionary (`dict(zip(df['key'], df['val']))`) or indexing before looping achieves O(1) lookups and speeds up rendering significantly (~4x faster metric computation).
**Action:** Always pre-compute dictionary mappings for lookup keys before rendering loops in Streamlit scripts.
