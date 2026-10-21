## 2026-03-23 - Avoid repeated DataFrame filtering inside Streamlit render loops
**Learning:** In Streamlit apps, code in the main script runs on every user interaction. Repeatedly filtering DataFrames with boolean indexing (`df[df['col'] == val]['col2'].iat[0]`) inside loops creates unnecessary sub-DataFrames and linear searches, adding significant latency on every rerun.
**Action:** Pre-index filtered DataFrames using `.set_index()` or build lookup dictionaries prior to rendering loops for O(1) attribute access.
