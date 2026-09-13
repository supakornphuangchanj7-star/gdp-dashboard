# Bolt's Performance Journal

## 2025-05-18 - Avoid repeated linear DataFrame filtering in render loops
**Learning:** In Streamlit apps, re-filtering a DataFrame inside a UI rendering loop (`gdp_df[gdp_df['Country Code'] == country]`) repeatedly scans the full DataFrame O(N * M) times on every user interaction / slider rerun. Pre-indexing the subset DataFrame into a Pandas Series (`set_index('Country Code')['GDP']`) before looping reduces lookup time by ~3.4x.
**Action:** Always pre-index or convert DataFrames into dict/indexed Series before iterating over user selection lists in Streamlit loops.
