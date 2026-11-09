## 2026-11-09 - Avoid DataFrame filtering loops in Streamlit re-renders

**Learning:** Streamlit re-runs the entire Python script on every user interaction (slider change, multiselect toggle). Inside the metric card rendering loop, doing boolean DataFrame filtering like `df[df['col'] == val]['target'].iat[0]` executes an O(N) linear filter for each item (O(k * N)). By pre-indexing into a Series with `df.set_index('col')['target']` before the loop, lookups become O(1) hash lookups, reducing metric calculation overhead by ~73% for standard selections (from ~9.0 ms to ~2.5 ms) and by ~98% when viewing all items (~360 ms down to ~4 ms).

**Action:** Whenever iterating over items to display Streamlit metrics or cards from a DataFrame, convert or index the slice into a Series or dictionary outside the loop rather than repeating DataFrame boolean filtering per iteration.
