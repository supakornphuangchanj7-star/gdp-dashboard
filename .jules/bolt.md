## 2025-02-28 - Streamlit Metric Loop DataFrame Filtering

**Learning:** Filtering Pandas DataFrames repeatedly inside a Streamlit render loop (e.g. `df[df['col'] == val]`) causes significant execution overhead (~3.2x slower) on every app rerun.
**Action:** Set the index on sliced DataFrames (`set_index('Country Code')['GDP']`) before loops to allow O(1) `.get(key)` lookups.
