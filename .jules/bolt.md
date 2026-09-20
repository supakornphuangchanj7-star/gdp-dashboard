## 2026-09-20 - Avoid DataFrame filtering inside Streamlit render loops
**Learning:** Filtering a Pandas DataFrame inside a Streamlit UI loop (e.g., `df[df['col'] == val]['col2'].iat[0]`) scales linearly with the number of selected items and re-runs on every user interaction, causing latency (~22ms down to ~3ms for 14 countries).
**Action:** Pre-build dictionary mappings (`dict(zip(df_subset['key'], df_subset['val']))`) outside the render loop for $O(1)$ constant time lookups.
