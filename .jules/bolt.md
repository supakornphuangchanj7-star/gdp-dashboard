## 2025-05-18 - Pre-indexing Pandas DataFrames for iterative lookup in Streamlit reruns
**Learning:** In Streamlit applications where the script executes from top-to-bottom on user interaction, doing $O(N)$ DataFrame filtering inside UI component loops (e.g. `df[df['col'] == key]`) adds measurable latency compared to pre-indexing into indexed Series or dicts outside the loop.
**Action:** Pre-index filtered DataFrames with `.set_index(key_col)[val_col]` before loop iterations for fast $O(1)$ lookups with `.get()`.
