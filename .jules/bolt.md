## 2026-03-31 - Indexed Series Lookup for Streamlit Iterative Calculations

**Learning:** In Streamlit app reruns, performing repeated DataFrame filtering (e.g. `df[df['col'] == key]['val'].iat[0]`) inside loops is O(N * M) and creates unnecessary intermediary DataFrame slice objects on each iteration. Setting an index once before the loop (e.g. `df.set_index('col')['val']`) allows O(1) indexed lookups with `.get()`, reducing calculation overhead by ~3.6x (~9.0ms down to ~2.5ms).

**Action:** Whenever iterating over a list of items to calculate metrics or render UI components in Streamlit, pre-index the DataFrame by the key column outside the loop and use `.get(key)` for efficient item retrieval.
