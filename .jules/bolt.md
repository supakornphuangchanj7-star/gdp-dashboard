## 2026-03-31 - O(N) DataFrame filtering in rendering loop
**Learning:** In Pandas / Streamlit apps, querying a DataFrame inside a display loop (`df[df['col'] == val]`) creates full linear scans on every iteration, leading to O(N^2) complexity.
**Action:** Pre-index or convert DataFrames to dictionaries (`df.set_index('col')['target'].to_dict()`) before rendering loops for O(1) hash map lookups.
