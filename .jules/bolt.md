## 2026-03-31 - Pandas DataFrame repeated scalar lookup in Streamlit render loops
**Learning:** Filtering a Pandas DataFrame on every loop iteration inside a Streamlit render loop (`df[df['col'] == key]`) scales O(N * C) where N is total rows per group and C is loop iterations, causing significant re-render latency (~13ms to 365ms per rerun).
**Action:** Pre-index the Series (`df.set_index('key_col')['val_col']`) before the loop and use `.get(key, math.nan)` for O(1) lookups per iteration.
