# Bolt's Journal - Critical Learnings

## 2026-03-31 - Pre-index DataFrames Before Rendering Loops in Streamlit Reruns

**Learning:** In Streamlit applications that execute on every user interaction (rerun), performing repeated DataFrame slicing/filtering inside a loop (e.g. `df[df['col'] == x]['val'].iat[0]` for each item in a UI list) causes O(N * M) repeated full scans of the DataFrame. By pre-indexing the DataFrame into a Series or Dictionary indexed by the key (`df.set_index('Key')['Column']`), lookup inside the loop becomes O(1) hash table lookup.

**Action:** When rendering repetitive UI elements (like metric cards or list items) from tabular data, always pre-index the DataFrame outside the loop.
