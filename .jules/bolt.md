## 2026-03-31 - Pandas DataFrame Indexing for Loop Lookups in Streamlit

**Learning:** Filtering a DataFrame repeatedly inside a loop (`df[df['col'] == key]['target_col'].iat[0]`) creates O(N * M) overhead due to full boolean mask evaluations on each iteration. Setting the index prior to the loop (`df.set_index('col')['target_col']`) and performing direct label-based indexing (`series.loc[key]`) turns repeated lookups into O(1) hash table accesses, achieving ~3.4x to 30x speedups for Streamlit widget re-renders.

**Action:** Whenever iterating over selected items to retrieve values from filtered Pandas DataFrames in Streamlit UI loops, set the lookup column as index once before the loop.
