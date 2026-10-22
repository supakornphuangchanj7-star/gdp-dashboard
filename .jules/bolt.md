## 2025-05-18 - Pre-filtering and Dictionary Lookups in Streamlit Render Loops

**Learning:** In Streamlit applications that re-execute top-to-bottom on every user interaction, repeatedly filtering large Pandas DataFrames inside loops (e.g., `df[df['Col'] == val]['Metric'].iat[0]`) introduces substantial O(N*M) overhead.
**Action:** Pre-filter DataFrames using already-filtered subsets (`filtered_df`) and construct dictionary lookup maps (`dict(zip(keys, values))`) prior to render loops for O(1) property access (~4x performance improvement on re-renders).
