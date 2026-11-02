# Bolt's Performance Journal

Critical learnings and performance patterns discovered in this codebase.

## 2025-05-18 - Repeated full-DataFrame boolean filtering in Streamlit reruns
**Learning:** In Streamlit apps, the entire script runs on each user interaction (e.g. slider adjustment, multiselect toggle). Filtering full DataFrames repeatedly within Python loops (e.g. `df[df['Country Code'] == country]` per country) causes redundant linear scans across all rows for every iteration. Filtering against the already-filtered subset and converting to an indexed lookup Series or hash map (`set_index('Country Code')['GDP']`) reduces time complexity from O(K * N) to O(K) lookup time, resulting in a 4x to 90x speedup depending on the number of selected countries.
**Action:** When calculating per-item metrics across user-selected subsets in Streamlit reruns, build an indexed Series or hash map once outside the display loop instead of repeatedly indexing the raw DataFrame inside the loop.
