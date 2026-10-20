# Bolt's Journal - Critical Learnings

## 2026-03-29 - Repeated Pandas Boolean Indexing in UI Rendering Loops
**Learning:** In Streamlit apps that render metrics or cards per item in a loop, doing repeated DataFrame boolean indexing (`df[df['col'] == item]['val'].iat[0]`) inside the loop creates unnecessary overhead (re-allocating Series/DataFrames on every loop iteration). Pre-filtering the DataFrame and indexing it into a dictionary or Series by key prior to the loop improves lookup performance significantly (~2.5x speedup).
**Action:** When calculating metrics for a list of items/countries in Streamlit, always index or convert the dataset to a dictionary (`set_index('key')['val']`) before the loop.
