## 2025-05-18 - Avoid repeated DataFrame filtering inside rendering loops during Streamlit re-renders

**Learning:** In Streamlit apps, the entire script re-executes on every user interaction. Performing repeated DataFrame filtering (`df[df['col'] == val]['GDP'].iat[0]`) inside a loop for UI components (like `st.metric`) creates significant overhead because Pandas builds boolean masks and sub-DataFrames on each iteration.
**Action:** Index the DataFrame/Series by key (`set_index('Country Code')['GDP']`) before the loop and perform direct key lookups (`series.get(key)`) to achieve up to 8x speedups for metric rendering.
