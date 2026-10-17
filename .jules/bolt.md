## 2026-10-17 - Indexed Series Lookups for Metric Iteration in Streamlit
**Learning:** Performing boolean indexing filtering on pandas DataFrames (`df[df['col'] == val]['target'].iat[0]`) inside render loops causes repeated full table scans (O(N) per loop iteration). Pre-indexing into a Series with `.set_index('key')['target']` before the loop enables O(1) hash map lookups (`series.get(key)`).
**Action:** Always pre-index DataFrames into a lookup Series or dict when accessing scalar values by key inside UI rendering loops.
