## 2026-09-19 - Fast Pandas Lookups in Streamlit Metric Loops

**Learning:** Pre-indexing pandas Series by key (`df.set_index('KeyCol')['ValueCol']`) before loops avoids repeated $O(N)$ boolean mask scanning (`df[df['KeyCol'] == key]`) on every Streamlit rerun. In multi-country metric views, indexing provided a 10x to 41x speedup per render (e.g. reducing metric evaluation time from ~30ms to ~3ms for 20 countries).

**Action:** Whenever calculating per-item metrics inside Streamlit layout loops (e.g., `st.metric`), convert the lookup slice to an indexed Series or dict prior to iteration.
